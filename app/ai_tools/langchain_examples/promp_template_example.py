# https://reference.langchain.com/python/langchain-google-genai/chat_models/ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

llm = ChatGoogleGenerativeAI(
    model="models/gemini-3.1-flash-lite-preview",
    api_key=settings.GOOGLE_API_KEY,
    temperature=0.9,
)
prompt_template = PromptTemplate.from_template(
    template="""A huge example, {key} - {example}"""
)
prompt = prompt_template.format_prompt(key="hi", example="Buddy")
for chunk in llm.stream(prompt):
    print(chunk.content, end="\n\n", flush=True)
