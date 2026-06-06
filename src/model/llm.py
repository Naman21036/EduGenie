from langchain_groq import ChatGroq
from dotenv import load_dotenv
import config.settings 

LLM_MODEL = config.settings.LLM_MODEL
TEMPERATURE = config.settings.TEMPERATURE

load_dotenv()

def get_llm():
    llm= ChatGroq(
        model= LLM_MODEL,
        temperature=TEMPERATURE,
        max_tokens= 2048,
    )
    
    return llm
