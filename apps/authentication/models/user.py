from sqlalchemy import Column, Integer, String

from database import Base, engine


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.username}', email='{self.email}')>"


Base.metadata.create_all(engine)
