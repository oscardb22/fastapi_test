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
while True:
    prompt = input('User: ')
    if prompt.lower() not in ('/exit', '/quit', '/bye'):
        response = chat.send_message(prompt)
        print(f"{chat.get_history()[-1].role.capitalize()}: {chat.get_history()[-1].parts[0].text}")
        print("\n" + "." * 100 + "\n")
    else:
        print("\n" + "QUITTING .." + "\n")
        break
