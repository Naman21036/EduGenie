import streamlit as st

from src.ingestion.retriever import retrieve
from src.study_tools.question_bank_generator import generate_question_bank


def render_question_bank(vector_db):

    st.subheader(
        "📚 Question Bank"
    )

    topic = st.text_input(
        "Topic",
        key="qb_topic"
    )

    if st.button(
        "Generate Question Bank"
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

        questions = generate_question_bank(
            context
        )

        st.markdown(
            questions
        )

        st.session_state.activity_log.append(
            "Generated Question Bank"
        )