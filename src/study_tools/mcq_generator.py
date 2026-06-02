from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json
from services.llm_service import generate_response
from services.parser_service import parse_json_response
from services.prompt_service import load_prompt

load_dotenv()

template = load_prompt("src/prompts/mcq_prompt.txt")

def generate_mcqs(text, num_ques=10):
    prompt= template.format(text=text, num_ques=num_ques)
    response = generate_response(prompt)

    return parse_json_response(response)