from langchain_text_splitters import RecursiveCharacterTextSplitter
import config.settings
from src.utils.logger import get_logger

CHUNK_SIZE = config.settings.CHUNK_SIZE
CHUNK_OVERLAP = config.settings.CHUNK_OVERLAP

text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

logger = get_logger()
def split_documents(documents):
    logger.info(f"Splitting {len(documents)} documents into chunks of size {CHUNK_SIZE} with overlap of {CHUNK_OVERLAP}")   
    return text_splitter.split_documents(documents)




