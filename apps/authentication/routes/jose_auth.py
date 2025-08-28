from fastapi import APIRouter, status

from apps.authentication.pydantic_models.token import Token
from apps.authentication.pydantic_models.user import CreateUserRequest, LoginUserRequest
from apps.authentication.views.jose_auth import auth_user, create_user, user_dependency
from database import db_dependency

router = APIRouter(prefix="/jose_auth", tags=["auth"])


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def route_create_user(
    user: user_dependency,
    db: db_dependency,
    create_jose_user_request: CreateUserRequest,
):
    create_user(db, create_jose_user_request)


@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def route_auth_user(
    db: db_dependency, form_data: LoginUserRequest
):
    return auth_user(
        user_name_or_email=form_data.username, password=form_data.password, db=db
    )
