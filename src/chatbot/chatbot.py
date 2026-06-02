from src.services.llm_service import generate_response
from src.services.prompt_service import load_prompt

template = load_prompt(
    "src/chatbot/chatbot_prompt.txt"
)

def chat(
    question,
    vector_db
):

    results = vector_db.max_marginal_relevance_search(
        question,
        k=5,
        fetch_k=20
    )

    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    prompt = template.format(
        context=context,
        question=question
    )

    return generate_response(prompt)