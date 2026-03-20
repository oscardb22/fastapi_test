# https://reference.langchain.com/python/langchain-google-genai/chat_models/ChatGoogleGenerativeAI
from langchain_classic.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

llm = ChatGoogleGenerativeAI(
    model="models/gemini-3.1-flash-lite-preview",
    api_key=settings.GOOGLE_API_KEY,
    temperature=0.9,
)
prompt = PromptTemplate.from_template(
    template="""A huge example, {topics}"""
)
chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

response = chain.invoke(input='must be true')
print(response)
