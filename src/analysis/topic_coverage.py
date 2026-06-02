from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json
from services.llm_service import generate_response
from services.parser_service import parse_json_response
from services.prompt_service import load_prompt
from utils.decorators import measure_time


load_dotenv()

template = load_prompt("prompts/topic_coverage_prompt.txt")

@measure_time
def generate_topic_coverage(text):
    prompt= template.format(text=text)
    response= generate_response(prompt)
    return parse_json_response(response)