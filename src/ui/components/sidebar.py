import os
import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.markdown("# 📚 EduGenie")

        st.caption(
            "AI Powered Learning Workspace"
        )

        st.divider()

        uploaded_files = st.file_uploader(
            "Upload PDFs",
            type=["pdf"],
            accept_multiple_files=True
        )

        process = st.button(
            "⚡ Process Documents",
            use_container_width=True
        )

        st.divider()

        st.subheader("Statistics")

        st.metric(
            "Documents",
            st.session_state.get(
                "doc_count",
                0
            )
        )

        st.metric(
            "Chunks",
            st.session_state.get(
                "chunk_count",
                0
            )
        )

        status = (
            "🟢 Ready"
            if st.session_state.get(
                "processed",
                False
            )
            else "🔴 Waiting"
        )

        st.write(
            f"Status: {status}"
        )

    return uploaded_files, process