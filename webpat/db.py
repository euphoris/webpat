""":mod:`webpat.db` --- Database connections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import current_app, g
from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from werkzeug.local import LocalProxy


__all__ = ('close_session', 'get_session', 'session',
           'setup_session')


def get_session():
    """Gets a session.  If there's no yet, creates one.

    :returns: a session
    """
    if hasattr(g, 'session'):
        return g.session
    sess = create_session(bind=current_app.config['DATABASE_ENGINE'])
    try:
        g.session = sess
    except RuntimeError:
        pass
    return sess


def close_session():
    """Closes an established session."""
    if hasattr(g, 'session'):
        g.session.close()


def setup_session(app):
    """Sets up the ``app`` to be able to use :data:`session`.

    :param app: the Flask application to setup
    :type app: :class:`~flask.Flask`

    """
    app.teardown_appcontext(close_session)


#: The context local session.  Use this.
db = LocalProxy(get_session)


def init_db(uri, base, **kwargs):
    """Create engine and tables
    :param uri: db uri
    :param base: declarative base
    :returns: an engine
    """
    engine = create_engine(uri, **kwargs)
    base.metadata.create_all(engine)
    return engine
