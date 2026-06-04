from dotenv import load_dotenv

from services.llm_service import generate_response
from services.prompt_service import load_prompt
from utils.decorators import measure_time

load_dotenv()

template = load_prompt(
    "prompts/question_bank_prompt.txt"
)


@measure_time
def generate_question_bank(
    context,
    num_2_mark=10,
    num_5_mark=10,
    num_10_mark=5,
    difficulty="Mixed"
):

    prompt = template.format(
        context=context,
        num_2_mark=num_2_mark,
        num_5_mark=num_5_mark,
        num_10_mark=num_10_mark,
        difficulty= difficulty
    )

    response = generate_response(
        prompt
    )

    return response