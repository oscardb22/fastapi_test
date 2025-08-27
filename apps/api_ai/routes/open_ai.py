
from fastapi import APIRouter, status

from apps.api_ai.pydantic_models.open_ai import SimpleChat
from apps.api_ai.views.open_ai import simple_open_ai_chat, simple_request_open_ai_chat
from apps.authentication.views.py_jwt_auth import user_dependency
from database import db_dependency

router = APIRouter(prefix="/open_ai", tags=["open_ai"])


@router.post("/simple_request_chat", status_code=status.HTTP_201_CREATED)
async def simple_request_chat(
    user: user_dependency,
    db: db_dependency,
    data_request: SimpleChat,
):
    return simple_request_open_ai_chat(user, db, data_request)


@router.post("/simple_chat", status_code=status.HTTP_201_CREATED)
async def simple_chat(
    user: user_dependency,
    db: db_dependency,
    data_request: SimpleChat,
):
    return simple_open_ai_chat(user, db, data_request)
