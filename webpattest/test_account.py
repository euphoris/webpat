from flask.ext.login import current_user, logout_user
import pytest
from sqlalchemy.orm.exc import NoResultFound

from webpat.account import AccountException, MissingInfo, sign_in, sign_up
from webpat.app import App
from webpat.db import db
from webpat.models import Base, User
from webpat.testing import generate_client_fixture


client = generate_client_fixture(App, Base)
pytest.fixture(client)


def test_sign_up(client):
    sign_up(username='testuser', password='1234')
    assert db.query(User).filter_by(username='testuser').one()

    with pytest.raises(AccountException) as acc_exc:
        sign_up(username='testuser', password='1234')

    assert acc_exc.value.args == ('duplicated username or email',)


def test_sign_up_without_password(client):
    with pytest.raises(MissingInfo) as exc:
        sign_up(username='testuser')


def test_sign_up_without_username_or_email(client):
    with pytest.raises(MissingInfo) as exc:
        sign_up(password='1234')


def test_sign_in(client):
    with pytest.raises(NoResultFound) as exc:
        sign_in(username='testuser', password='1234')

    sign_up(username='testuser', password='1234')
    with client:
        sign_in(username='testuser', password='1234')
        assert current_user.is_active()
        assert not current_user.is_anonymous()
        assert current_user.username == 'testuser'


def test_sign_out(client):
    sign_up(username='testuser', password='1234')
    with client:
        sign_in(username='testuser', password='1234')
        logout_user()
        assert not current_user.is_active()
        assert current_user.is_anonymous()
