import streamlit as st

from src.chatbot.chatbot import chat


def render_chatbot(vector_db):

    st.header("💬 EduGenie Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    # User input

    question = st.chat_input(
        "Ask anything about your documents..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner(
                "Thinking..."
            ):

                answer = chat(
                    question,
                    vector_db
                )

                st.markdown(
                    answer
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )