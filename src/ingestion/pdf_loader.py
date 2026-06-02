from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_paths):
    documents= []
    for file_path in file_paths:
        loader=  PyPDFLoader(file_path)
        docs= loader.load()
        documents.extend(docs)
    
    return documents