from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pytest

from webpat.app import App
from webpat.db import db, init_db
from webpat.models import Base, User
from webpat.testing import generate_client_fixture


@pytest.fixture
def db_uri(tmpdir):
    db_file = tmpdir.join('db_file')
    uri = 'sqlite:///' + db_file.strpath
    return uri


@pytest.fixture
def default_app(request):
    app = Flask(__name__)
    app.config['TESTING'] = True
    ctx = app.test_request_context()
    ctx.push()

    def fin():
        ctx.pop()
    request.addfinalizer(fin)
    return app


def test_db(default_app, db_uri):
    default_app.config['DATABASE_ENGINE'] = create_engine(db_uri)
    db.begin()


def test_init_db(default_app, db_uri):
    base = declarative_base()
    default_app.config['DATABASE_ENGINE'] = init_db(db_uri, base)
    db.begin()


def test_create_base(default_app, db_uri):
    default_app.config['DATABASE_ENGINE'] = init_db(db_uri, Base)
    assert db.query(User).count() == 0


def test_app(db_uri):
    App(__name__, uri=db_uri, base=Base)


client = generate_client_fixture(App, Base)
pytest.fixture(client)


def test_client(client):
    res = client.get('/')
    assert res.status_code == 404
