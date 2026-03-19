# https://ai.google.dev/gemini-api/docs/migrate
from google import genai
from PIL import Image

from app.core.config import settings

client = genai.Client(api_key=settings.GOOGLE_API_KEY)
with Image.open('example.jpg') as img:
    response = client.models.generate_content(
        model="models/gemini-3.1-flash-lite-preview",
        contents=[
            "Tell me a story based on this image",
            img
        ],
    )
    print(response.text)
