import uuid
from datetime import UTC, datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship

from app.core.base_model import BaseModel


class Users(BaseModel, table=True):

    full_name: str | None = Field(default=None, max_length=255, nullable=True)
    username: str | None = Field(max_length=20, default=None)
    cellphone: str | None = Field(max_length=50, nullable=True, default=None)
    email: EmailStr = Field(unique=True, index=True, max_length=100)
    hashed_password: str = Field(max_length=255)
    is_superuser: bool = False
    date_joined: datetime = Field(default=datetime.now(UTC))
    tokens: Optional["Tokens"] = Relationship(
        back_populates="users", sa_relationship_kwargs={"uselist": False}
    )

    def __repr__(self):
        return (f"<User({self.id=}, '{self.username=}', '{self.date_joined=}', "
                f"'{self.email=}', '{self.hashed_password=}'), '{self.is_active=}')>")


class Tokens(BaseModel, table=True):
    token: str = Field(unique=True, index=True, max_length=100)
    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
    users: Optional["Users"] | None = Relationship(
        back_populates="tokens", sa_relationship_kwargs={"uselist": False}
    )

    def __repr__(self):
        return f"<User({self.id=}, '{self.token=}', '{self.user_id=}', {self.is_active=}')>"


class TokenPayload(BaseModel):
    sub: str | None = None


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginUserRequest(BaseModel):
    username: str
    password: str
