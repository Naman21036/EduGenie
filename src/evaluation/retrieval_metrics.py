import time

def evaluate_retrieval(vector_db, query, k=5):

    start_time = time.time()

    results = vector_db.similarity_search(
        query,
        k=k
    )

    latency = time.time() - start_time

    metrics = {
        "query": query,
        "retrieved_chunks": len(results),
        "retrieval_latency": round(latency, 3)
    }

    return metrics