import streamlit as st

from frontend.ui.tools.notes_ui import render_notes
from frontend.ui.tools.mcq_ui import render_mcqs
from frontend.ui.tools.flashcard_ui import render_flashcards
from frontend.ui.tools.question_bank_ui import render_question_bank


def render_selected_tool(vector_db):

    tool = st.session_state.get(
        "selected_tool"
    )

    if tool == "notes":

        render_notes(
            vector_db
        )

    elif tool == "mcqs":

        render_mcqs(
            vector_db
        )

    elif tool == "flashcards":

        render_flashcards(
            vector_db
        )

    elif tool == "question_bank":

        render_question_bank(
            vector_db
        )
