from google import genai
from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
client_genai = genai.Client(api_key=settings.GOOGLE_API_KEY)
embeddings = client.embeddings.create(
    model='text-embedding-3-small',
    input='This is an example text',
)
print(embeddings.data[0].embedding)
# https://ai.google.dev/gemini-api/docs/migrate#embed-content
embeddings = client_genai.models.embed_content(
    model='gemini-embedding-001',
    contents='This is an example text',
)
print(embeddings.embeddings[0].values)
