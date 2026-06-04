import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <style>
            .logo-box{
                background: linear-gradient(135deg,#6366f1,#8b5cf6);
                padding:20px;
                border-radius:20px;
                text-align:center;
                margin-bottom:20px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown("## 🎓 EduGenie")
        st.caption("AI Learning Workspace")

        status = (
            "🟢 Ready"
            if st.session_state.get(
                "processed",
                False
            )
            else "🔴 Waiting"
        )

        st.success(
            f"Status: {status}"
        )

        st.markdown("---")

        st.subheader(
            "📂 Document Upload"
        )

        uploaded_files = st.file_uploader(
            "Upload PDF Files",
            type=["pdf"],
            accept_multiple_files=True
        )

        process = st.button(
            "⚡ Process Documents",
            use_container_width=True
        )

        st.markdown("---")

        st.subheader(
            "📊 Workspace Stats"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Pages",
                st.session_state.get(
                    "doc_count",
                    0
                )
            )

        with col2:

            st.metric(
                "Chunks",
                st.session_state.get(
                    "chunk_count",
                    0
                )
            )

        st.metric(
            "Topics",
            st.session_state.get(
                "topic_count",
                0
            )
        )

        st.markdown("---")

        st.subheader(
            "⚡ Quick Actions"
        )

        if st.button(
            "🗑 Clear Chat",
            use_container_width=True
        ):

            st.session_state.chat_history = []

            st.success(
                "Chat cleared"
            )

        if st.button(
            "🔄 Reset Workspace",
            use_container_width=True
        ):

            keys = list(
                st.session_state.keys()
            )

            for key in keys:

                del st.session_state[key]

            st.rerun()

        st.markdown("---")

        st.subheader(
            "📝 Recent Activity"
        )

        activity_log = st.session_state.get(
            "activity_log",
            []
        )

        if activity_log:

            for item in reversed(
                activity_log[-5:]
            ):

                st.caption(
                    f"• {item}"
                )

        else:

            st.caption(
                "No activity yet"
            )

    return uploaded_files, process