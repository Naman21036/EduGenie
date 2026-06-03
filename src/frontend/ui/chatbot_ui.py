from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


def render_chatbot(vector_db):

    base = Path(
        "src/frontend/chatbot"
    )

    html = (
        base /
        "chatbot.html"
    ).read_text(
        encoding="utf-8"
    )

    css = (
        base /
        "chatbot.css"
    ).read_text(
        encoding="utf-8"
    )

    js = (
        base /
        "chatbot.js"
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

    chat_history = st.session_state.get(
        "chat_history",
        []
    )

    messages_html = ""

    for message in chat_history:

        role = message["role"]

        content = message["content"]

        if role == "user":

            messages_html += f"""
            <div class="user-message">
                {content}
            </div>
            """

        else:

            messages_html += f"""
            <div class="assistant-message">
                {content}
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
            "{{CHAT_MESSAGES}}",
            messages_html
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