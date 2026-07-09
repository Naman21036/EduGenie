from dotenv import load_dotenv
from services.llm_service import generate_response
from services.parser_service import parse_json_response
from services.prompt_service import load_prompt
from utils.decorators import measure_time



load_dotenv()

template = load_prompt("prompts/revision_sheet_prompt.txt")

@measure_time
def generate_revision_sheet(text):
    prompt= template.format(text=text)
    response = generate_response(prompt)
    
    return parse_json_response(response)
        