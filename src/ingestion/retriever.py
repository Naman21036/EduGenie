from src.utils.logger import get_logger
from src.config.settings import TOP_K

logger = get_logger()


def retrieve(query, vector_db, top_k=TOP_K):

    logger.info(
        f"Retrieving {top_k} chunks for query: {query}"
    )

    results = vector_db.similarity_search(
        query,
        k=top_k
    )

    logger.info(
        f"Retrieved {len(results)} chunks"
    )

    return results