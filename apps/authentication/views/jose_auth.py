from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from loguru import logger

from apps.authentication.models.user import Users
from apps.authentication.pydantic_models.token import Token
from apps.authentication.pydantic_models.user import CreateUserRequest
from database import db_dependency
from settings import ALGORITHM, SECRET_KEY, bcrypt_context, outh2_bearer


def create_user(db: db_dependency, create_jose_user_request: CreateUserRequest):
    jose_user_model = Users(
        username=create_jose_user_request.username,
        email=create_jose_user_request.email,
        hashed_password=bcrypt_context.hash(create_jose_user_request.password),
    )
    db.add(jose_user_model)
    db.commit()


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "exp": datetime.utcnow() + expires_delta}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def auth_user(user_name_or_email: str, password: str, db):
    user_data = db.query(Users).filter(Users.username == user_name_or_email).first()
    if not user_data:
        user_data = db.query(Users).filter(Users.email == user_name_or_email).first()
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Couldn't validate this user",
            )
    if not bcrypt_context.verify(password, user_data.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate this user",
        )
    access_token = create_access_token(
        username=user_data.username,
        user_id=user_data.id,
        expires_delta=timedelta(minutes=20),
    )
    return Token(access_token=access_token)


async def get_current_user(token: Annotated[str, Depends(outh2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub", None)
        user_id = payload.get("id", None)
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": user_id}
    except JWTError as error:
        logger.error(error)
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate"
        )


user_dependency = Annotated[dict, Depends(get_current_user)]
