import streamlit as st

from src.ingestion.retriever import retrieve
from src.study_tools.mcq_generator import generate_mcqs


def render_mcqs(vector_db):

    st.subheader(
        "🎯 MCQ Generator"
    )

    topic = st.text_input(
        "Topic",
        key="mcq_topic"
    )

    num_mcqs = st.number_input(
        "Number of MCQs",
        min_value=1,
        max_value=50,
        value=10
    )

    if st.button(
        "Generate MCQs"
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

        mcqs = generate_mcqs(
            context,
            num_mcqs
        )

        st.markdown(
            mcqs
        )

        st.session_state.activity_log.append(
            f"Generated {num_mcqs} MCQs"
        )