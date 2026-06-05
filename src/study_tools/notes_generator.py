from model.llm import get_llm
from utils.decorators import measure_time

@measure_time
def generate_notes(context):
    llm = get_llm()

    prompt = f"""
    Create concise study notes.

    Context:
    {context}

    Include:
    1. Summary
    2. Key Concepts
    3. Important Points
    """

    response = llm.invoke(prompt)

    return response.content
