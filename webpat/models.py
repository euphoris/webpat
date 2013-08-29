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
