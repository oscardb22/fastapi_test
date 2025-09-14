from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cache.decorator import cache

from app.api.deps import db_dependency
from app.cruds.py_jwt_auth import auth_user

router = APIRouter()


@router.get("/")
@cache(expire=60)
async def index():
    return {"response": "my test"}


@router.post("/token")
async def token(
        db: db_dependency,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return auth_user(
        user_name_or_email=form_data.username, password=form_data.password, db=db
    )
