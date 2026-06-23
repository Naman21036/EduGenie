import os

import streamlit as st
from frontend.components.sidebar import render_sidebar
from frontend.components.navbar import render_navbar

from ingestion.pdf_loader import load_pdf
from ingestion.text_splitter import split_documents
from ingestion.vector_db import create_vector_db

from frontend.ui.dashboard_ui import render_dashboard
from frontend.ui.study_tools import render_study_tools
from frontend.ui.analysis import render_analysis
from frontend.ui.exam_prep import render_exam_prep
from frontend.ui.chatbot_ui import render_chatbot
from frontend.components.icons import ICON_CSS_RULES

from utils.logger import get_logger

logger = get_logger()

# PAGE CONFIG


st.set_page_config(
    page_title="EduGenie AI",
    page_icon=":material/menu_book:",
    layout="wide",
)
# GLOBAL CSS


st.markdown(
    f"""
    <style>
    {ICON_CSS_RULES}
    /* ── App background ── */
    .stApp {
        background: #020617;
    }

    /* ── Max width + top padding ── */
    .block-container {
        max-width: 1440px;
        padding-top: 0.6rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* ── Streamlit primary button ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: #fff;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        font-size: 13.5px;
        padding: 10px 20px;
        transition: opacity 0.15s;
    }
    .stButton > button[kind="primary"]:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }

    /* ── Secondary buttons ── */
    .stButton > button {
        border-radius: 10px;
        font-size: 13px;
        font-weight: 500;
        border: 1px solid rgba(255,255,255,0.08);
        background: #111827;
        color: #94a3b8;
        padding: 8px 14px;
        transition: background 0.15s, color 0.15s;
    }
    .stButton > button:hover {
        background: #1e293b;
        color: #e2e8f0;
        border-color: rgba(99,102,241,0.3);
    }

    /* ── Workspace nav card buttons: hide them visually, keep them clickable ── */
    [data-testid="stVerticalBlock"] .stButton > button[key^="nav_card"] {
        background: transparent;
        border: none;
        color: #6366f1;
        font-size: 12px;
        font-weight: 600;
        padding: 0;
        height: auto;
        box-shadow: none;
        margin-top: -8px;
    }
    [data-testid="stVerticalBlock"] .stButton > button[key^="nav_card"]:hover {
        background: transparent;
        color: #818cf8;
    }

    /* ── Text inputs ── */
    .stTextInput > div > div > input {
        background: #0f172a;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        color: #e2e8f0;
        font-size: 14px;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(255,255,255,0.06);
    }

    /* ── Metrics widget ── */
    [data-testid="stMetric"] {
        background: #0c1120;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 14px 18px;
    }
    [data-testid="stMetricLabel"] { color: #475569; font-size: 12px; }
    [data-testid="stMetricValue"] { color: #a5b4fc; font-size: 22px; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #6366f1 !important; }

    /* ── Alerts ── */
    .stAlert {
        background: #0f172a;
        border-radius: 12px;
        border: 1px solid rgba(99,102,241,0.18);
        color: #94a3b8;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        background: #0f172a;
        border: 1px dashed rgba(99,102,241,0.25);
        border-radius: 12px;
        padding: 12px;
    }

    /* ── Chat input ── */
    .stChatInput > div {
        background: #0f172a;
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# SESSION STATE

defaults = {
    "documents": None,
    "chunks": None,
    "vector_db": None,
    "processed": False,
    "activity_log": [],
    "file_names": [],
    "doc_count": 0,
    "chunk_count": 0,
    "topic_count": 0,
    "selected_tool": "notes",
    "chat_history": [],
    "selected_page": "Dashboard",
    "nav_target": None,
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val
# SIDEBAR

uploaded_files, process_button = render_sidebar()

# DOCUMENT PROCESSING


if process_button:
    if not uploaded_files:
        st.warning("Please upload at least one PDF.")
    else:
        save_dir = "saved_files"
        os.makedirs(save_dir, exist_ok=True)
        file_paths = []

        for uploaded_file in uploaded_files:
            file_path = os.path.join(save_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            file_paths.append(file_path)

        with st.spinner("Processing documents…"):
            try:
                documents = load_pdf(file_paths)
                chunks = split_documents(documents)
                vector_db = create_vector_db(chunks)

                st.session_state.documents = documents
                st.session_state.chunks = chunks
                st.session_state.vector_db = vector_db
                st.session_state.processed = True
                st.session_state.doc_count = len(documents)
                st.session_state.chunk_count = len(chunks)
                st.session_state.file_names = [f.name for f in uploaded_files]
                st.session_state.activity_log.append("Processed Documents")
                st.success("Documents processed successfully!")

            except Exception as e:
                logger.exception("Document processing failed")
                st.error(str(e))

# NAVIGATION


navbar_selection = render_navbar()

if st.session_state.nav_target:
    st.session_state.selected_page = st.session_state.nav_target
    st.session_state.nav_target = None
else:
    st.session_state.selected_page = navbar_selection

selected = st.session_state.selected_page

# PAGE ROUTING


if selected == "Dashboard":
    render_dashboard()

elif selected == "Study Tools":
    if st.session_state.processed:
        render_study_tools(st.session_state.vector_db)
    else:
        st.warning("Please process documents first.")

elif selected == "Analysis":
    if st.session_state.processed:
        render_analysis(st.session_state.vector_db)
    else:
        st.warning("Please process documents first.")

elif selected == "Exam Prep":
    if st.session_state.processed:
        render_exam_prep(st.session_state.vector_db)
    else:
        st.warning("Please process documents first.")

elif selected == "Chat":
    if st.session_state.processed:
        render_chatbot(st.session_state.vector_db)
    else:
        st.warning("Please process documents first.")
