from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

SECRET_KEY = "197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe4"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
outh2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
