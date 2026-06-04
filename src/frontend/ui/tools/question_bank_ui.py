import streamlit as st

from src.ingestion.retriever import retrieve
from src.study_tools.question_bank_generator import (
    generate_question_bank
)


def render_question_bank(vector_db):

    st.subheader(
        "📚 Question Bank Generator"
    )

    topic = st.text_input(
        "Topic",
        key="qb_topic"
    )

    col1, col2 = st.columns(2)

    with col1:

        num_2_mark = st.number_input(
            "2 Mark Questions",
            min_value=1,
            max_value=50,
            value=10
        )

        num_5_mark = st.number_input(
            "5 Mark Questions",
            min_value=1,
            max_value=50,
            value=10
        )

    with col2:

        num_10_mark = st.number_input(
            "10 Mark Questions",
            min_value=1,
            max_value=30,
            value=5
        )

    if st.button(
        "Generate Question Bank"
    ):

        if not topic.strip():

            st.warning(
                "Please enter a topic."
            )

            return

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
            context,
            num_2_mark,
            num_5_mark,
            num_10_mark
        )

        st.markdown(
            questions
        )

        st.session_state.activity_log.append(
            "Generated Question Bank"
        )