from langchain_community.document_loaders import PyPDFLoader
from utils.logger import get_logger

logger = get_logger()

def load_pdf(file_paths):
    documents= []
    logger.info(f"Loading PDFs from {file_paths}")
    for file_path in file_paths:
        loader=  PyPDFLoader(file_path)
        docs= loader.load()
        documents.extend(docs)
    
    logger.info(f"Loaded {len(documents)} documents from PDFs")
    return documents
