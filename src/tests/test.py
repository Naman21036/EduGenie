from src.ingestion.pdf_loader import load_pdf
from src.ingestion.vector_db import create_vector_db
from src.ingestion.text_splitter import split_documents
from src.ingestion.retriever import retrieve
from src.generators.notes_generator import generate_notes

document = load_pdf([r"saved_files\Resume- Naman Gupta (1).pdf"])

chunks = split_documents(document)
vector_db = create_vector_db(chunks)
query = "What is the name of the person in the resume?"
results = retrieve(query, vector_db)

print(f"Documents: {len(document)}")
print(f"Chunks: {len(chunks)}")
for result in results:
    print(result.page_content)

context = "\n".join(
    [doc.page_content for doc in results]
)

notes = generate_notes(context)

print(notes)