from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


def render_exam_prep(vector_db):

    base = Path(
        "src/frontend/exam_prep"
    )

    html = (
        base /
        "exam_prep.html"
    ).read_text(
        encoding="utf-8"
    )

    css = (
        base /
        "exam_prep.css"
    ).read_text(
        encoding="utf-8"
    )

    js = (
        base /
        "exam_prep.js"
    ).read_text(
        encoding="utf-8"
    )

    html = (
        html
        .replace(
            "{{DOCS}}",
            str(
                st.session_state.get(
                    "doc_count",
                    0
                )
            )
        )
        .replace(
            "{{CHUNKS}}",
            str(
                st.session_state.get(
                    "chunk_count",
                    0
                )
            )
        )
    )

    components.html(
        f"""
        <style>{css}</style>

        {html}

        <script>{js}</script>
        """,
        height=1000,
        scrolling=True
    )