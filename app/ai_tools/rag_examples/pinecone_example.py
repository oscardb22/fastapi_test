# https://docs.pinecone.io/reference/sdks/python/overview
# https://pypi.org/project/pinecone-client/
from pinecone import Pinecone, ServerlessSpec

from app.core.config import settings


def pinecone_insert(vectors, pc_obj: Pinecone, name_index:str):
    index_obj = pc_obj.Index(name_index)
    index_obj.upsert(vectors=vectors)


def pinecone_update(column:str, pc_obj: Pinecone, name_index:str):
    index_obj = pc_obj.Index(name_index)
    index_obj.upsert(vectors=[(column, [0.5] * 1536)])


def pinecone_delete(columns:list, pc_obj: Pinecone, name_index:str):
    index_obj = pc_obj.Index(name_index)
    index_obj.delete(ids=columns)
    print(index_obj.describe_index_stats())


def pinecone_retrieve(columns:list, pc_obj: Pinecone, name_index:str):
    index_obj = pc_obj.Index(name_index)
    print(index_obj.fetch(ids=columns))


def pinecone_query(vectors, pc_obj: Pinecone, name_index:str):
    index_obj = pc_obj.Index(name_index)
    index_obj.query(top_k=3,include_values=False, vector=vectors)


if __name__ == "__main__":
    index_name = "example"
    pc = Pinecone(api_key=settings.PINECONE_APY_KEY)
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    # When you want to delete an index
    # pc.delete_index(name=index_name)
    # When you would like to know de summary of the index
    index = pc.Index(name=index_name)
    print(index.describe_index_stats())
    print(pc.list_indexes())
    print(pc.describe_index(name=index_name))
    print(pc.list_indexes().names())
