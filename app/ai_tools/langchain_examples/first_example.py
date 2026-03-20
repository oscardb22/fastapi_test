from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# https://reference.langchain.com/python/langchain-google-genai/llms/GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI

from app.core.config import settings

llm = GoogleGenerativeAI(
    model="models/gemini-3.1-flash-lite-preview",
    api_key=settings.GOOGLE_API_KEY,
    temperature=0.9,
)
output = llm.invoke('hello world')
print(output)
msg = [
    SystemMessage(content='You are a dog'),
    HumanMessage(content='Tell me something good.'),
    AIMessage(content='relevant')
]
output = llm.invoke(msg)
print(output)
