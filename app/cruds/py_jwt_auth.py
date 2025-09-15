from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from jwt.exceptions import InvalidTokenError
from loguru import logger

from app.api.deps import db_dependency
from app.core.config import settings
from app.core.security import get_password_hash, outh2_bearer, verify_password
from app.models.user import CreateUserRequest, TokenPayload, Tokens, Users


def create_user(db: db_dependency, create_jose_user_request: CreateUserRequest):
    user_model = Users(
        username=create_jose_user_request.username,
        email=create_jose_user_request.email,
        hashed_password=get_password_hash(create_jose_user_request.password),
    )
    db.add(user_model)
    db.commit()


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "exp": datetime.now(UTC)  + expires_delta}
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def auth_user(user_name_or_email: str, password: str, db: db_dependency):
    user_data = db.query(Users).filter(Users.username == user_name_or_email).first()
    if not user_data:
        user_data = db.query(Users).filter(Users.email == user_name_or_email).first()
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Couldn't validate this user",
            )
    if not verify_password(password, user_data.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Couldn't validate this user",
        )
    access_token = create_access_token(
        username=user_data.username,
        user_id=user_data.id,
        expires_delta=timedelta(minutes=20),
    )
    token_model = Tokens(user=user_data, token=access_token)
    db.add(token_model)
    db.commit()
    return TokenPayload(sub=access_token)


async def get_current_user(
        token: Annotated[str, Depends(outh2_bearer)]
):
    db = db_dependency()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub", None)
        user_id = payload.get("id", None)
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        user_data = db.query(Users).filter(Users.id == user_id).first()
        if user_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        token_data = db.query(Tokens).filter(
            Tokens.user_id == user_id, Tokens.token==token
        ).first()
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": user_id}
    except InvalidTokenError as error:
        logger.error(error)
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate"
        )


user_dependency = Annotated[dict, Depends(get_current_user)]
