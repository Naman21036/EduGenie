import html
import re

from services.llm_service import generate_response
from services.prompt_service import load_prompt

template = load_prompt(
    "chatbot/chatbot_prompt.txt"
)

_UI_ROW_RE = re.compile(
    r'<div[^>]*class=["\'][^"\']*msg-row[^"\']*["\'][^>]*>.*',
    re.DOTALL | re.IGNORECASE,
)
_UI_BUBBLE_RE = re.compile(
    r'<div[^>]*class=["\'][^"\']*msg-bubble[^"\']*["\'][^>]*>(.*)',
    re.DOTALL | re.IGNORECASE,
)
_TAG_RE = re.compile(r"<[^>]+>")


def plain_text_content(text):
    """Return message text without UI/HTML markup for storage or LLM context."""

    if not text:
        return text

    text = html.unescape(str(text).strip())

    for _ in range(5):
        if not _UI_ROW_RE.search(text) and not _UI_BUBBLE_RE.search(text):
            break

        bubble_match = _UI_BUBBLE_RE.search(text)
        if bubble_match:
            text = bubble_match.group(1)
            continue

        if _UI_ROW_RE.search(text):
            text = _TAG_RE.sub("", text)
            continue

        break

    text = _TAG_RE.sub("", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def _format_history(history):
    if not history:
        return ""

    return "\n".join(
        f"{msg['role']}: {plain_text_content(msg['content'])}"
        for msg in history[-10:]
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

    history_text = _format_history(history)

    prompt = template.format(
        history=history_text,
        context=context,
        question=question
    )

    answer = generate_response(
        prompt
    )

    return plain_text_content(answer)
