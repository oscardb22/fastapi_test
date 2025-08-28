from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base, engine


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return (f"<User({self.id=}, '{self.username=}', '{self.date_joined=}', "
                f"'{self.email=}', '{self.hashed_password=}'), '{self.is_active=}')>")


class Tokens(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship(Users)
    token = Column(String, unique=True)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return (f"<User({self.id=}, '{self.token=}', '{self.date_joined=}', "
                f"'{self.date_joined=}'), '{self.is_active=}')>")


Base.metadata.create_all(engine)
