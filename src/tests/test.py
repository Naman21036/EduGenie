from src.ingestion.pdf_loader import load_pdf
from src.ingestion.vector_db import create_vector_db
from src.ingestion.text_splitter import split_documents
from src.ingestion.retriever import retrieve


def test_rag_pipeline():

    documents = load_pdf(
        [r"saved_files\Analysis-of-2-kV-HBM-ESD-Event-in-CMOS.pdf"]
    )

    assert len(documents) > 0

    chunks = split_documents(documents)

    assert len(chunks) > 0

    vector_db = create_vector_db(chunks)

    assert vector_db is not None

    results = retrieve(
        "What is the name of the person in the resume?",
        vector_db
    )

    assert len(results) > 0

if __name__ == "__main__":
    test_rag_pipeline()