from model.llm import get_llm

llm = get_llm()

def generate_response(prompt):

    try:

        response = llm.invoke(prompt)

        return response.content

    except Exception as e:

        raise RuntimeError(
            f"LLM generation failed: {str(e)}"
        )
