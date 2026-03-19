from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "developer", "content": "You high-school tutor."},
        {"role": "user", "content": "Explain Quantum mechanics to teenagers"},
    ],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content)
        print(f"\n{'*' * 100}", end='\n')
