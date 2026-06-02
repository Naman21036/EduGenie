from src.utils.logger import get_logger
import config.settings

logger = get_logger(__name__)

TOP_K = config.settings.TOP_K


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