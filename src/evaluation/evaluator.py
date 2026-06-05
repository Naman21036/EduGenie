from evaluation.retrieval_metrics import evaluate_retrieval
from evaluation.generation_metrics import evaluate_generation

def evaluate_pipeline(
    vector_db,
    query,
    generator_func
):

    retrieval_metrics = evaluate_retrieval(
        vector_db,
        query
    )

    results = vector_db.similarity_search(
        query,
        k=5
    )

    context = "\n".join(
        [doc.page_content for doc in results]
    )

    output, generation_metrics = evaluate_generation(
        generator_func,
        context
    )

    return {
        "retrieval": retrieval_metrics,
        "generation": generation_metrics
    }
