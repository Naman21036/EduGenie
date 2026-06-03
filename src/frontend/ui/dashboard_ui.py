from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


def render_dashboard():

    base = Path(
        "src/frontend/dashboard"
    )

    html = (
        base /
        "dashboard.html"
    ).read_text(
        encoding="utf-8"
    )

    css = (
        base /
        "dashboard.css"
    ).read_text(
        encoding="utf-8"
    )

    js = (
        base /
        "dashboard.js"
    ).read_text(
        encoding="utf-8"
    )

    docs = st.session_state.get(
        "doc_count",
        0
    )

    chunks = st.session_state.get(
        "chunk_count",
        0
    )

    topics = st.session_state.get(
        "topic_count",
        0
    )

    status = (
        "Ready"
        if st.session_state.get(
            "processed",
            False
        )
        else "Waiting"
    )

    file_names = st.session_state.get(
        "file_names",
        []
    )

    activity_log = st.session_state.get(
        "activity_log",
        []
    )

    files_html = ""

    if file_names:

        for file in file_names:

            files_html += f"""
            <div class="document-item">
                📄 {file}
            </div>
            """

    else:

        files_html = """
        <div class="document-item">
            No documents uploaded yet
        </div>
        """

    activity_html = ""

    if activity_log:

        for item in reversed(
            activity_log[-10:]
        ):

            activity_html += f"""
            <div class="activity-item">
                ✓ {item}
            </div>
            """

    else:

        activity_html = """
        <div class="activity-item">
            No recent activity
        </div>
        """

    html = (
        html
        .replace(
            "{{DOCS}}",
            str(docs)
        )
        .replace(
            "{{CHUNKS}}",
            str(chunks)
        )
        .replace(
            "{{TOPICS}}",
            str(topics)
        )
        .replace(
            "{{STATUS}}",
            status
        )
        .replace(
            "{{FILES}}",
            files_html
        )
        .replace(
            "{{ACTIVITY}}",
            activity_html
        )
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
        height=1800,
        scrolling=True
    )