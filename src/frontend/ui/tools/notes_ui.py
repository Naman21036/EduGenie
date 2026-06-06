import streamlit as st

from ingestion.retriever import retrieve
from study_tools.notes_generator import generate_notes


def render_notes(vector_db):

    st.success("Notes UI Loaded")

    st.subheader("📄 Notes Generator")

    topic = st.text_input("Topic")

    st.write("Current topic:", topic)

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

        st.markdown(notes)
