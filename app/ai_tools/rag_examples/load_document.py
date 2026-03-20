import os

# https://docs.langchain.com/oss/python/integrations/document_loaders#pdfs
from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
    WikipediaLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_document(file):
    name, extension = os.path.splitext(file)
    if extension == ".pdf":
        loader = PyPDFLoader(file)
    elif extension == ".docx":
        loader = Docx2txtLoader(file)
    else:
        raise Exception("Unknown document format")

    data_to_return = loader.load()
    return data_to_return


def load_wikipedia(query, lang='en', load_max_docs=2):
    loader = WikipediaLoader(query=query, lang=lang, load_max_docs=load_max_docs)
    data_to_return = loader.load()
    return data_to_return


def chunk_data(data, chunk_size=256):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
    chunks = text_splitter.split_documents(data)
    return chunks


if __name__ == "__main__":
    data_look = load_document("constitution.pdf")
    print(data_look[1].page_content)
    print(data_look[10].metadata)
