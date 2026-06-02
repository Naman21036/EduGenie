from src.model.llm import get_llm

llm = get_llm()

def generate_response(prompt, temperature= 0.7, max_tokens= None):

    try:

        if max_tokens is not None:

            temp_llm = get_llm(
                temperature=temperature,
                max_tokens=max_tokens
            )

            response = temp_llm.invoke(prompt)

        else:

            response = llm.invoke(prompt)

        return response.content

    except Exception as e:

        raise RuntimeError(
            f"LLM generation failed: {str(e)}"
        )