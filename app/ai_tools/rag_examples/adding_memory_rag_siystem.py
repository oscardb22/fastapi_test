from google import genai
from langchain_classic.chains.conversational_retrieval.base import (
    ConversationalRetrievalChain,
)
from langchain_classic.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

from app.ai_tools.rag_examples.chromadb_example import load_embeddings_chroma
from app.core.config import settings

config = genai.types.GenerateContentConfig(
    candidate_count=1,
    stop_sequences=[";"],
    max_output_tokens=65536,
    temperature=0.9,
    top_k=64,
    top_p=0.95,
)
chat = ChatGoogleGenerativeAI(
    api_key=settings.GOOGLE_API_KEY,
    model="models/gemini-3.1-flash-lite-preview",
    config=config,
    history=[],
)
retriever = load_embeddings_chroma().as_retriever(
    search_type="similarity", search_kwargs={"k": 5}
)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
crc = ConversationalRetrievalChain.from_llm(
    llm=chat, retriever=retriever, memory=memory, chain_type="stuff", verbose=True
)
