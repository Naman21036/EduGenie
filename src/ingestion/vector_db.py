from langchain_community.vectorstores import FAISS
from .embeddings import get_embeddings

def create_vector_db(documents):
    embeddings = get_embeddings()
    vector_db = FAISS.from_documents(
        documents=documents,
        embedding=embeddings,
        )
    return vector_db