from pathlib import Path

from langchain_community.vectorstores import FAISS

from ingestion.embeddings import get_embeddings
from utils.logger import get_logger


INDEX_PATH = Path("vector_store")

logger = get_logger()

def create_vector_db(documents):

    logger.info(
        f"Creating vector database from {len(documents)} documents"
    )

    embeddings = get_embeddings()

    vector_db = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    vector_db.save_local(
        str(INDEX_PATH)
    )

    logger.info(
        "Vector database created successfully"
    )

    return vector_db


def load_vector_db():

    logger.info(
        "Loading vector database"
    )

    embeddings = get_embeddings()

    vector_db = FAISS.load_local(
        str(INDEX_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

    logger.info(
        "Vector database loaded successfully"
    )

    return vector_db


def vector_db_exists():

    return INDEX_PATH.exists()
