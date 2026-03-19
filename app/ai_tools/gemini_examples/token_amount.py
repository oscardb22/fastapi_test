# https://ai.google.dev/gemini-api/docs/migrate#upload
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
model = client.models.get(
    model='models/gemini-3.1-flash-lite-preview',
)
print(model.input_token_limit)
print(f"\n{'*' * 100}", end='\n')

print(model.output_token_limit)
print(f"\n{'*' * 100}", end='\n')

print(model.temperature)
print(f"\n{'*' * 100}", end='\n')


token_count = client.models.count_tokens(
    model='models/gemini-3.1-flash-lite-preview',
    contents='Hi Zion.'
)
print(token_count.total_tokens)
print(f"\n{'*' * 100}", end='\n')

sample_file = client.files.upload(file='example.png')
token_count = client.models.count_tokens(
    model='models/gemini-3.1-flash-lite-preview',
    contents=['Hi Zion.', sample_file]
)
print(token_count.total_tokens)
print(f"\n{'*' * 100}", end='\n')
