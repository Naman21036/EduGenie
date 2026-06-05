from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP
from utils.logger import get_logger

text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

logger = get_logger()
def split_documents(documents):
    logger.info(f"Splitting {len(documents)} documents into chunks of size {CHUNK_SIZE} with overlap of {CHUNK_OVERLAP}")   
    return text_splitter.split_documents(documents)




