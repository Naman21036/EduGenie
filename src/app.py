import os
import streamlit as st

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.text_splitter import split_documents
from src.ingestion.vector_db import create_vector_db

from src.ui.study_tools import render_study_tools
from src.ui.analysis import render_analysis
from src.ui.exam_prep import render_exam_prep
from src.ui.chatbot_ui import render_chatbot

from src.utils.logger import get_logger


logger = get_logger()

st.set_page_config(
    page_title="EduGenie",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>

.block-container{
    max-width:1400px;
    padding-top:2rem;
}

[data-testid="stMetric"]{
    background:#1E293B;
    padding:20px;
    border-radius:16px;
    border:1px solid #334155;
}

.stButton > button{
    border-radius:12px;
    height:3rem;
}

</style>
""", unsafe_allow_html=True)


# Session State

if "documents" not in st.session_state:
    st.session_state.documents = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "processed" not in st.session_state:
    st.session_state.processed = False


# UI Header

st.title("📚 EduGenie")
st.caption(
    "AI Powered Study Assistant using RAG"
)


# Sidebar for Document Upload and Stats

with st.sidebar:

    st.header("Document Upload")

    uploaded_files = st.file_uploader(
        "Upload PDF Files",
        type=["pdf"],
        accept_multiple_files=True
    )

    process_button = st.button(
        "Process Documents",
        use_container_width=True
    )

    st.divider()

    st.subheader("Statistics")

    if st.session_state.documents:

        st.metric(
            "Documents",
            len(st.session_state.documents)
        )

    if st.session_state.chunks:

        st.metric(
            "Chunks",
            len(st.session_state.chunks)
        )


# Document Processing Logic
if process_button:

    if not uploaded_files:

        st.warning(
            "Please upload at least one PDF."
        )

    else:

        save_dir = "saved_files"

        os.makedirs(
            save_dir,
            exist_ok=True
        )

        file_paths = []

        for uploaded_file in uploaded_files:

            file_path = os.path.join(
                save_dir,
                uploaded_file.name
            )

            with open(
                file_path,
                "wb"
            ) as f:

                f.write(
                    uploaded_file.getbuffer()
                )

            file_paths.append(
                file_path
            )

        with st.spinner(
            "Processing documents..."
        ):

            try:

                logger.info(
                    f"Loading PDFs: {file_paths}"
                )

                documents = load_pdf(
                    file_paths
                )

                chunks = split_documents(
                    documents
                )

                vector_db = create_vector_db(
                    chunks
                )

                st.session_state.documents = documents
                st.session_state.chunks = chunks
                st.session_state.vector_db = vector_db
                st.session_state.processed = True

                logger.info(
                    "Document processing completed"
                )

                st.success(
                    "Documents processed successfully!"
                )

            except Exception as e:

                logger.exception(
                    "Document processing failed"
                )

                st.error(
                    f"Error: {str(e)}"
                )


# Main Tabs for Study Tools, Analysis, Exam Prep, and Chatbot

if st.session_state.processed:

    study_tab, analysis_tab, exam_tab, chat_tab = st.tabs(
        [
            "📖 Study Tools",
            "📊 Analysis",
            "📝 Exam Prep",
            "💬 Chat"
        ]
    )

    with study_tab:

        render_study_tools(
            st.session_state.vector_db
        )

    with analysis_tab:

        render_analysis(
            st.session_state.vector_db
        )

    with exam_tab:

        render_exam_prep(
            st.session_state.vector_db
        )

    with chat_tab:

        render_chatbot(
            st.session_state.vector_db
        )

else:

    st.info(
        "Upload and process PDFs to get started."
    )