from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import config.settings
from functools import lru_cache
EMBEDDING_MODEL = config.settings.EMBEDDING_MODEL

load_dotenv()

@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    encode_kwargs={"normalize_embeddings": True},
)