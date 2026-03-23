from google import genai
from google.genai import types
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI

from app.ai_tools.rag_examples.load_document import chunk_data, load_document
from app.core.config import settings


def ask_and_get_answer(vector_store, question, amount_k: int = 3):
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
        history=[]
    )
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={"k": amount_k})
    chain = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=retriever)
    answer = chain.invoke(question)
    return answer


def create_embeddings_chroma(chunks, persist_directory="./chroma_db"):
    client_genai = genai.Client(api_key=settings.GOOGLE_API_KEY)
    # https://ai.google.dev/gemini-api/docs/embeddings#control-embedding-size
    result = client_genai.models.embed_content(
        model="gemini-embedding-001",
        contents="This is an example text",
        config=types.EmbedContentConfig(output_dimensionality=1536),
    )

    vector_store = Chroma.from_documents(
        chunks, embedding=result.embeddings, persist_directory=persist_directory
    )
    return vector_store


def load_embeddings_chroma(persist_directory="./chroma_db"):
    client_genai = genai.Client(api_key=settings.GOOGLE_API_KEY)
    # https://ai.google.dev/gemini-api/docs/embeddings#control-embedding-size
    result = client_genai.models.embed_content(
        model="gemini-embedding-001",
        contents="This is an example text",
        config=types.EmbedContentConfig(output_dimensionality=1536),
    )

    vector_store = Chroma(
        embedding_function=result.embeddings, persist_directory=persist_directory
    )
    return vector_store


if __name__ == "__main__":
    data = load_document('./constitution.pdf')
    chunks_data = chunk_data(data=data, chunk_size=256)
    vector_store_example = create_embeddings_chroma(chunks_data)

    db_example = load_embeddings_chroma()
