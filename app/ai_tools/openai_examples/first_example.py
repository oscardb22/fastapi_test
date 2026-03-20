from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)
completion = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'system', 'content': 'the best search'},
              {'role': 'user', 'content': 'hi team'}],
    temperature=1
)
print(completion.choices[0].message.content)
