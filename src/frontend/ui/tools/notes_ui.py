import streamlit as st

from src.ingestion.retriever import retrieve
from src.study_tools.notes_generator import generate_notes


def render_notes(vector_db):

    st.subheader(
        "📄 Notes Generator"
    )

    topic = st.text_input(
        "Topic"
    )

    if st.button(
        "Generate Notes",
        key="notes_btn"
    ):

        docs = retrieve(
            topic,
            vector_db
        )

        context = "\n".join(
            [
                doc.page_content
                for doc in docs
            ]
        )

        notes = generate_notes(
            context
        )

        st.markdown(
            notes
        )

        st.session_state.activity_log.append(
            f"Generated Notes on {topic}"
        )