from flask import Flask

from .db import init_db

class App(Flask):
    def __init__(self, *args, **kwargs):
        base = kwargs.pop('base')
        uri = kwargs.pop('uri')
        super(App, self).__init__(*args, **kwargs)
        self.config['DATABASE_ENGINE'] = init_db(uri, base)