import streamlit as st


def render_metrics():

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Documents",
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

    with col3:

        st.metric(
            "Topics",
            st.session_state.get(
                "topic_count",
                0
            )
        )

    with col4:

        st.metric(
            "Status",
            "Ready"
            if st.session_state.get(
                "processed",
                False
            )
            else "Waiting"
        )