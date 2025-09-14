import requests
from loguru import logger
from openai import OpenAI

from app.api.deps import db_dependency, get_current_active_superuser
from app.core.config import settings
from app.models.open_ai import SimpleChat

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def simple_open_ai_chat(
        user: get_current_active_superuser,
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
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        # seed=1234,
        # top_p=0.1,
        # max_tokens=10,
        # n=2,
        # stop=[";", ".", "\n"],
        frequency_penalty=0,  # between -2 and 2, default 0
        presence_penalty=0  # [-2, +2]
    )
    return response.choices[0].message.content


def simple_request_open_ai_chat(
        user: get_current_active_superuser,
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
    response = requests.post(url=settings.URL_CHAT_OPEN_AI, headers=settings.HEADER_OPEN_AI, json=data)
    return response.json()


def models_open_ai_chat(
        user: get_current_active_superuser,
        db: db_dependency,
        data_request: SimpleChat
):
    messages = [
      {
        "role": "user",
        "content": data_request.message
      },
    ]
    response = client.chat.completions.create(
        model="o3-mini",
        reasoning_effort="medium",
        max_completion_tokens=10000,
        messages=messages,
    )
    return response.choices[0].message.content


def whisper_models_open_ai_chat(
        user: get_current_active_superuser,
        db: db_dependency,
        data_request: SimpleChat
):
    with open(data_request.message, "rb") as audio_file:
        transcript = client.audio.translations.create(
            model="whisper-1",
            file=audio_file
        )
        logger.info(transcript.text)
        return transcript
