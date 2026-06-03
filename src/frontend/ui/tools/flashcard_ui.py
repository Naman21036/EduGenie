import streamlit as st

from src.ingestion.retriever import retrieve
from src.study_tools.flashcard_generator import generate_flashcards


def render_flashcards(vector_db):

    st.subheader(
        "🃏 Flashcards"
    )

    topic = st.text_input(
        "Topic",
        key="flash_topic"
    )

    num_cards = st.number_input(
        "Number of Flashcards",
        min_value=1,
        max_value=50,
        value=10
    )

    if st.button(
        "Generate Flashcards"
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

        flashcards = generate_flashcards(
            context,
            num_cards
        )

        st.json(
            flashcards
        )

        st.session_state.activity_log.append(
            f"Generated {num_cards} Flashcards"
        )