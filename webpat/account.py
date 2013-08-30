import functools

from flask import redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

from .db import db
from .models import User


class AccountException(Exception):
    pass


class MissingInfo(Exception):
    pass


def login_required(url):
    """
    Usage:

        @login_required('/signin')
        def view_func():
            ...

    :param url: redirect url

    """
    def decorator(f):
        @functools.wraps(f)
        def g(*args, **kwargs):
            if 'user' not in session:
                return redirect(url)
            return f(*args, **kwargs)
        return g
    return decorator


def user_query(username, email):
    """
    Find a user match with username and email
    :param username:
    :param email:
    :returns:
    """
    query = db.query(User)
    if username:
        query = query.filter_by(username=username)

    if email:
        query = query.filter_by(username=username)

    return query


def sign_up(username=None, email=None, password=None):
    if not ((username or email) and password):
        raise MissingInfo

    user_exists = user_query(username, email).count()
    if user_exists:
        raise AccountException('duplicated username or email')
    else:
        with db.begin():
            pw_hash = generate_password_hash(password)
            user = User(username=username, email=email, password=pw_hash)
            db.add(user)
        session['user'] = user


def sign_in(username=None, email=None, password=None):
    user = user_query(username, email).one()

    password_correct = check_password_hash(user.password, password)
    if password_correct:
        session['user'] = user
    else:
        raise AccountException('incorrect password')


def sign_out():
    session.pop('user', None)
