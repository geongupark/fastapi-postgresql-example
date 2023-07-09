from sqlalchemy import Column, Integer, String, CHAR, VARCHAR
from .base import Base


class Users(Base):
    __tablename__ = "health_users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(VARCHAR(255))
    gender = Column(VARCHAR(2))
    age = Column(Integer())
