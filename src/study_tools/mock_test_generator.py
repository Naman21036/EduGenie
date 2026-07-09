from dotenv import load_dotenv
from services.llm_service import generate_response
from services.parser_service import parse_json_response
from services.prompt_service import load_prompt
from utils.decorators import measure_time


load_dotenv()

template = load_prompt("prompts/mock_test_prompt.txt")

@measure_time
def generate_mock_test(text, num_2_mark, num_5_mark, num_10_mark, difficulty):
    prompt= template.format(text=text, num_2_mark=num_2_mark, num_5_mark=num_5_mark, num_10_mark=num_10_mark, difficulty=difficulty)
    response = generate_response(prompt)

    return parse_json_response(response)