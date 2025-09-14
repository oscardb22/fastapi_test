from fastapi import APIRouter, status
from pydantic import BaseModel

from app.api.deps import db_dependency
from app.cruds.open_ai import simple_open_ai_chat, simple_request_open_ai_chat
from app.cruds.py_jwt_auth import user_dependency

router = APIRouter(prefix="/open_ai", tags=["open_ai"])


class SimpleChat(BaseModel):
    message: str

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
