from langchain_community.cache import SQLiteCache
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import GoogleGenerativeAI

from app.core.config import settings

llm = GoogleGenerativeAI(
    model="models/gemini-3.1-flash-lite-preview",
    api_key=settings.GOOGLE_API_KEY,
    temperature=0.9,
)
set_llm_cache(InMemoryCache())
set_llm_cache(SQLiteCache(database_path='.langchain.db'))
msg = [
    SystemMessage(content='You are a dog'),
    HumanMessage(content='Tell me something good.'),
    AIMessage(content='relevant')
]
output = llm.invoke(msg)
print(output)
