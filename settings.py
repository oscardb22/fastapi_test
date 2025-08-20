from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from decouple import config

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
TOKEN_TYPE = config("TOKEN_TYPE")
SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
outh2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
