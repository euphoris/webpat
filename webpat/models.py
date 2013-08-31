from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    pk = Column(Integer, primary_key=True)
    username = Column(String(32))
    email = Column(String(256))
    password = Column(String(66))
    is_admin = Column(Boolean, default=False)

    def is_authenticated(self):
        """Returns True if the user is authenticated"""
        return self.pk is not None

    def is_active(self):
        """Returns True if this is an active user"""
        return self.pk is not None

    def is_anonymous(self):
        """Returns True if this is an anonymous user."""
        return self.pk is None

    def get_id(self):
        return self.pk
