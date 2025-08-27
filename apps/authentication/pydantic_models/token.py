from pydantic import BaseModel

from settings import TOKEN_TYPE


class Token(BaseModel):
    access_token: str
    token_type: str = TOKEN_TYPE
