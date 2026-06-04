from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from src.frontend.ui.tool_router import render_selected_tool


def render_study_tools(vector_db):

    base = Path(
        "src/frontend/study_tools"
    )

    html = (
        base /
        "study_tools.html"
    ).read_text(
        encoding="utf-8"
    )

    theme_css = (
        Path("src/frontend/shared/theme.css")
    ).read_text(
        encoding="utf-8"
    )

    page_css = (
        base /
        "study_tools.css"
    ).read_text(
        encoding="utf-8"
    )

    css = theme_css + "\n" + page_css

    js = (
        base /
        "study_tools.js"
    ).read_text(
        encoding="utf-8"
    )

    components.html(
        f"""
        <style>
        {css}
        </style>

        {html}

        <script>
        {js}
        </script>
        """,
        height=650,
        scrolling=False
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if st.button(
            "📄 Notes",
            use_container_width=True
        ):
            st.session_state.selected_tool = "notes"

    with col2:

        if st.button(
            "🎯 MCQs",
            use_container_width=True
        ):
            st.session_state.selected_tool = "mcqs"

    with col3:

        if st.button(
            "🃏 Flashcards",
            use_container_width=True
        ):
            st.session_state.selected_tool = "flashcards"

    with col4:

        if st.button(
            "📚 Question Bank",
            use_container_width=True
        ):
            st.session_state.selected_tool = "question_bank"

    st.divider()

    render_selected_tool(
        vector_db
    )