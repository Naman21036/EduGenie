from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json
from services.llm_service import generate_response
from services.parser_service import parse_json_response
from services.prompt_service import load_prompt
from utils.decorators import measure_time


load_dotenv()

template = load_prompt("src/prompts/question_bank_prompt.txt")

@measure_time
def generate_question_bank(text, num_2_mark, num_5_mark, num_10_mark):
    prompt= template.format(text=text, num_2_mark=num_2_mark, num_5_mark=num_5_mark, num_10_mark=num_10_mark)
    response = generate_response(prompt)

    return parse_json_response(response)