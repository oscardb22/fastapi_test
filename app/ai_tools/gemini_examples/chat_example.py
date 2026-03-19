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
chat = client.chats.create(
    model='models/gemini-3.1-flash-lite-preview',
    config=config,
    history=[]
)
response = chat.send_message('Give me an example of SELECT statement with postgresql to a beginner')
print(chat.get_history()[-1].parts[0].text)

print(response.model_dump_json(
    exclude_none=True,
    indent=4)
)

for item in chat.get_history():
    print(f"{item.role.capitalize()}: {item.parts[0].text}")
    print("." * 100)
