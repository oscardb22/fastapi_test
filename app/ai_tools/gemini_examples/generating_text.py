# https://ai.google.dev/gemini-api/docs/migrate
from google import genai

from app.core.config import settings

client = genai.Client(api_key=settings.GOOGLE_API_KEY)
for model in client.models.list():
    print(model)
    print(model.name, model.input_token_limit, model.output_token_limit)

response = client.models.generate_content(
    model='models/gemini-3.1-flash-lite-preview',
    contents='What is your age?',
)
print(response.text)

print(response.model_dump_json(
    exclude_none=True,
    indent=4)
)

# Get the info regarding with the model
print("+" * 50, end='\n')
print(
    client.models.get(
        model='models/gemini-3.1-flash-lite-preview'
    )
)
