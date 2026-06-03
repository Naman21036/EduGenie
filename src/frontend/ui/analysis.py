from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


def render_analysis(vector_db):

    base = Path(
        "src/frontend/analysis"
    )

    html = (
        base /
        "analysis.html"
    ).read_text(
        encoding="utf-8"
    )

    css = (
        base /
        "analysis.css"
    ).read_text(
        encoding="utf-8"
    )

    js = (
        base /
        "analysis.js"
    ).read_text(
        encoding="utf-8"
    )

    html = (
        html
        .replace(
            "{{TOPICS}}",
            str(
                st.session_state.get(
                    "topic_count",
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