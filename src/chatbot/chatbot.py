from services.llm_service import generate_response
from services.prompt_service import load_prompt

template = load_prompt(
    "chatbot/chatbot_prompt.txt"
)

def chat(
    question,
    vector_db,
    history=None
):

    results = vector_db.max_marginal_relevance_search(
        question,
        k=5,
        fetch_k=20
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in results
        ]
    )

    history_text = ""

    if history:

        history_text = "\n".join(
            [
                f"{msg['role']}: {msg['content']}"
                for msg in history[-10:]
            ]
        )

    prompt = template.format(
        history=history_text,
        context=context,
        question=question
    )

    response = generate_response(
        prompt
    )

    if hasattr(
        response,
        "content"
    ):
        return response.content

    return str(response)
