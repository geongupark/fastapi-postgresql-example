from sqlalchemy import Column, Integer, VARCHAR, BIGINT
from .base import Base


class Users(Base):
    __tablename__ = "health_users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(VARCHAR(255))
    gender = Column(VARCHAR(2))
    age = Column(Integer())


class MetaInts(Base):
    __tablename__ = "meta_ints"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(VARCHAR(255))
    value = Column(BIGINT())


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(VARCHAR(30))
    password = Column(VARCHAR(10))
    content = Column(VARCHAR(100))
    sessionid = Column(VARCHAR(10))
