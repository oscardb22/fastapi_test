import requests
from openai import OpenAI

from apps.api_ai.pydantic_models.open_ai import SimpleChat
from apps.authentication.views.py_jwt_auth import user_dependency
from database import db_dependency
from settings import HEADER_OPEN_AI, OPENAI_API_KEY, URL_CHAT_OPEN_AI

client = OpenAI(api_key=OPENAI_API_KEY)


def simple_open_ai_chat(
        user: user_dependency,
        db: db_dependency,
        data_request: SimpleChat
):
    messages = [
      {
        "role": "developer",
        "content": "You high-school tutor."
      },
      {
        "role": "user",
        "content": data_request.message
      },
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, temperature=0.7
    )
    return response.choices[0].message.content


def simple_request_open_ai_chat(
        user: user_dependency,
        db: db_dependency,
        data_request: SimpleChat
):
    data = {
    "model": "gpt-4o-mini",
    "messages": [
      {
        "role": "developer",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": data_request.message
      }
    ], "temperature": 0.7
    }
    response = requests.post(url=URL_CHAT_OPEN_AI, headers=HEADER_OPEN_AI, json=data)
    return response.json()
