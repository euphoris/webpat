from flask.ext.login import LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from .db import db
from .models import User


class AccountException(Exception):
    pass


class MissingInfo(Exception):
    pass


login_manager = LoginManager()

@login_manager.user_loader
def load_user(userid):
    return db.query(User).get(userid)


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


def sign_in(username=None, email=None, password=None):
    user = user_query(username, email).one()

    password_correct = check_password_hash(user.password, password)
    if password_correct:
        login_user(user)
    else:
        raise AccountException('incorrect password')
