# https://ai.google.dev/gemini-api/docs/migrate
from google import genai

from app.core.config import settings

client = genai.Client(api_key=settings.GOOGLE_API_KEY)
config = genai.types.GenerateContentConfig(
    candidate_count=1,
    stop_sequences=[';'],
    max_output_tokens=65536,
    temperature=0.9,
    top_k=64,
    top_p=0.95,
    system_instruction='You are a dog. Your name is Zion.'
)
# models/gemini-3.1-pro-preview
response = client.models.generate_content(
    model='models/gemini-3.1-flash-lite-preview',
    contents='Hi Zion.',
    config=config
)
print(response.text)
print(f"\n{'*' * 100}", end='\n')
