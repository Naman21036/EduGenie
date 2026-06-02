def retrieve(query, vector_db, top_k=5):
    results = vector_db.similarity_search(query, k=top_k)
    return results