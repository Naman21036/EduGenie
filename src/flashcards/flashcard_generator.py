from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json

load_dotenv()

with open("src/flashcards/flashcards_prompt.txt", "r", encoding="utf-8") as f:
    template = f.read()
llm= ChatGroq(
        model= "llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens= 2048,
    )

def generate_flashcards(text):
    prompt= template.format(text=text)
    response= llm.invoke(prompt)
    content = response.content.strip()
    if content.startswith("```json"):
        content = content.replace(
            "```json",
            ""
        )
        content = content.replace(
            "```",
            ""
        ).strip()
    try:
        return json.loads(content)

    except json.JSONDecodeError:
        raise ValueError(
            f"Invalid JSON returned by LLM:\n{content}"
        )