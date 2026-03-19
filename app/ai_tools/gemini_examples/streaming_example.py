# https://ai.google.dev/gemini-api/docs/migrate
from google import genai

from app.core.config import settings

client = genai.Client(api_key=settings.GOOGLE_API_KEY)
for chunk in client.models.generate_content_stream(
        model='models/gemini-3.1-flash-lite-preview',
        contents='What is my age?'):
    print(chunk.text, end='')
    print("__" * 50)
