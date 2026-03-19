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
)
response = client.models.generate_content(
    model='models/gemini-3.1-flash-lite-preview',
    contents='Give me an example of SELECT statement with postgresql',
    config=config,
)
print(response.text)

print(response.model_dump_json(
    exclude_none=True,
    indent=4)
)
