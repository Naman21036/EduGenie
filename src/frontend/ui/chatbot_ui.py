from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from src.chatbot.chatbot import chat


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

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    messages_html = ""

    for message in st.session_state.chat_history:

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
        height=700,
        scrolling=True
    )

    st.divider()
    col1, col2 = st.columns(
        [5,1]
    )

    with col2:

        if st.button(
            "🗑 Clear"
        ):

            st.session_state.chat_history = []

            st.rerun()

    question = st.chat_input(
        "Ask a question about your documents..."
    )

    if question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.spinner(
            "Thinking..."
        ):

            answer = chat(
                question,
                vector_db,
                st.session_state.chat_history
            )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()