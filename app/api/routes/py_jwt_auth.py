from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import db_dependency
from app.cruds.py_jwt_auth import (
    auth_user,
    create_user,
    user_dependency,
)
from app.models.user import CreateUserRequest, Tokens

router = APIRouter(prefix="/py_jwt_auth", tags=["auth"])


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def route_create_user(
    user: user_dependency,
    db: db_dependency,
    create_jose_user_request: CreateUserRequest,
):
    create_user(db, create_jose_user_request)


@router.post("/token", status_code=status.HTTP_200_OK, response_model=Tokens)
async def route_auth_user(
    db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return auth_user(
        user_name_or_email=form_data.username, password=form_data.password, db=db
    )
