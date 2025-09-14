from pydantic import BaseModel


class SimpleChat(BaseModel):
    message: str | None = None
