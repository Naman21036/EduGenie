import streamlit as st

from src.ingestion.retriever import retrieve

from src.study_tools.notes_generator import generate_notes
from src.study_tools.flashcard_generator import generate_flashcards
from src.study_tools.mcq_generator import generate_mcqs
from src.study_tools.question_bank_generator import generate_question_bank


def render_study_tools(vector_db):

    st.header("📖 Study Tools")

    query = st.text_input(
        "Enter a topic or concept",
        placeholder="Machine Learning, Neural Networks, ESD..."
    )

    if not query:
        st.info(
            "Enter a topic to generate study materials."
        )
        return

    results = retrieve(
        query,
        vector_db
    )

    context = "\n".join(
        [doc.page_content for doc in results]
    )

    notes_tab, flashcard_tab, mcq_tab, question_bank_tab = st.tabs(
        [
            "Notes",
            "Flashcards",
            "MCQs",
            "Question Bank"
        ]
    )

    with notes_tab:

        if st.button(
            "Generate Notes",
            use_container_width=True
        ):

            with st.spinner(
                "Generating notes..."
            ):

                notes = generate_notes(
                    context
                )

                st.write(
                    notes
                )

    with flashcard_tab:

        num_cards = st.number_input(
            "Number of Flashcards",
            min_value=1,
            max_value=50,
            value=10
        )

        if st.button(
            "Generate Flashcards",
            use_container_width=True
        ):

            with st.spinner(
                "Generating flashcards..."
            ):

                flashcards = generate_flashcards(
                    context,
                    num_cards
                )

                st.json(
                    flashcards
                )

    with mcq_tab:

        num_mcqs = st.number_input(
            "Number of MCQs",
            min_value=1,
            max_value=100,
            value=10
        )

        if st.button(
            "Generate MCQs",
            use_container_width=True
        ):

            with st.spinner(
                "Generating MCQs..."
            ):

                mcqs = generate_mcqs(
                    context,
                    num_mcqs
                )

                st.json(
                    mcqs
                )

    with question_bank_tab:

        num_2_mark = st.number_input(
            "2 Mark Questions",
            min_value=0,
            value=5,
            key="2_mark"
        )

        num_5_mark = st.number_input(
            "5 Mark Questions",
            min_value=0,
            value=5,
            key="5_mark"
        )

        num_10_mark = st.number_input(
            "10 Mark Questions",
            min_value=0,
            value=5,
            key="10_mark"
        )

        if st.button(
            "Generate Question Bank",
            use_container_width=True
        ):

            with st.spinner(
                "Generating question bank..."
            ):

                questions = generate_question_bank(
                    context,
                    num_2_mark,
                    num_5_mark,
                    num_10_mark
                )

                st.json(
                    questions
                )