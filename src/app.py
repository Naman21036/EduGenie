import os

import streamlit as st
from src.frontend.components.sidebar import render_sidebar
from src.frontend.components.navbar import render_navbar

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.text_splitter import split_documents
from src.ingestion.vector_db import create_vector_db

from src.frontend.ui.dashboard_ui import render_dashboard
from src.frontend.ui.study_tools import render_study_tools
from src.frontend.ui.analysis import render_analysis
from src.frontend.ui.exam_prep import render_exam_prep
from src.frontend.ui.chatbot_ui import render_chatbot

from src.utils.logger import get_logger


logger = get_logger()


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="EduGenie",
    page_icon="📚",
    layout="wide"
)


# ==================================================
# GLOBAL CSS
# ==================================================

st.markdown(
    """
<style>

.block-container{
    max-width:1600px;
    padding-top:1rem;
}

.stApp{
    background:
    linear-gradient(
        135deg,
        #020617,
        #0f172a
    );
}

.stButton > button{

    width:100%;

    border-radius:12px;

    height:3rem;

    border:none;

    background:
    linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    );

    color:white;

    font-weight:600;
}

.stButton > button:hover{

    transform:
    translateY(-2px);
}

</style>
""",
    unsafe_allow_html=True
)


# ==================================================
# SESSION STATE
# ==================================================

if "documents" not in st.session_state:
    st.session_state.documents = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "processed" not in st.session_state:
    st.session_state.processed = False

if "activity_log" not in st.session_state:
    st.session_state.activity_log = []

if "file_names" not in st.session_state:
    st.session_state.file_names = []

if "doc_count" not in st.session_state:
    st.session_state.doc_count = 0

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "topic_count" not in st.session_state:
    st.session_state.topic_count = 0

if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = "notes"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==================================================
# HEADER
# ==================================================



# ==================================================
# SIDEBAR
# ==================================================

uploaded_files, process_button = render_sidebar()


# ==================================================
# DOCUMENT PROCESSING
# ==================================================

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
            "Processing Documents..."
        ):

            try:

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

                st.session_state.doc_count = len(
                    documents
                )

                st.session_state.chunk_count = len(
                    chunks
                )

                st.session_state.file_names = [
                    file.name
                    for file in uploaded_files
                ]

                st.session_state.activity_log.append(
                    "Processed Documents"
                )

                st.success(
                    "Documents Processed Successfully!"
                )

            except Exception as e:

                logger.exception(
                    "Document Processing Failed"
                )

                st.error(
                    str(e)
                )


# ==================================================
# NAVIGATION
# ==================================================

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Dashboard"

if "nav_target" not in st.session_state:
    st.session_state.nav_target = None

navbar_selection = render_navbar()

if st.session_state.nav_target:

    st.session_state.selected_page = (
        st.session_state.nav_target
    )

    st.session_state.nav_target = None

else:

    st.session_state.selected_page = (
        navbar_selection
    )

selected = st.session_state.selected_page


# ==================================================
# PAGE ROUTING
# ==================================================

if selected == "Dashboard":

    render_dashboard()


elif selected == "Study Tools":

    if st.session_state.processed:

        render_study_tools(
            st.session_state.vector_db
        )

    else:

        st.warning(
            "Please process documents first."
        )


elif selected == "Analysis":

    if st.session_state.processed:

        render_analysis(
            st.session_state.vector_db
        )

    else:

        st.warning(
            "Please process documents first."
        )


elif selected == "Exam Prep":

    if st.session_state.processed:

        render_exam_prep(
            st.session_state.vector_db
        )

    else:

        st.warning(
            "Please process documents first."
        )


elif selected == "Chat":

    if st.session_state.processed:

        render_chatbot(
            st.session_state.vector_db
        )

    else:

        st.warning(
            "Please process documents first."
        )