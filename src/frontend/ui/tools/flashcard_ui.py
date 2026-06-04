import json
import streamlit as st

from src.ingestion.retriever import retrieve
from src.study_tools.flashcard_generator import generate_flashcards

from src.frontend.components.cards import (
    render_flashcards as render_flashcard_cards
)


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

        flashcards = generate_flashcards(
            context,
            num_cards
        )

        if isinstance(
            flashcards,
            str
        ):

            flashcards = (
                flashcards
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            flashcards = json.loads(
                flashcards
            )

        cleaned_cards = []

        for card in flashcards:

            if isinstance(card, str):

                card = json.loads(card)

            cleaned_cards.append(card)

        render_flashcard_cards(
            cleaned_cards
        )

        st.session_state.activity_log.append(
            f"Generated {num_cards} Flashcards"
        )