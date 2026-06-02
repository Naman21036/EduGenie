from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from src.config.settings import EMBEDDING_MODEL
from functools import lru_cache

load_dotenv()

@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    encode_kwargs={"normalize_embeddings": True},
)