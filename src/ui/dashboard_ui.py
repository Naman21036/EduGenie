import streamlit as st

def render_dashboard():


    st.markdown(
        """
        # 📚 EduGenie
        
        ### Transform PDFs into Notes, Flashcards, MCQs, Mock Tests and AI Insights
        """
    )

    st.write("")

    # =========================
    # Metrics Section
    # =========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📄 Documents",
            st.session_state.get(
                "doc_count",
                0
            )
        )

    with col2:

        st.metric(
            "🧩 Chunks",
            st.session_state.get(
                "chunk_count",
                0
            )
        )

    with col3:

        st.metric(
            "🧠 Topics",
            st.session_state.get(
                "topic_count",
                0
            )
        )

    with col4:

        st.metric(
            "⚡ Status",
            "Ready"
            if st.session_state.get(
                "processed",
                False
            )
            else "Waiting"
        )

    st.markdown("---")

    # =========================
    # Quick Actions
    # =========================

    st.subheader("🚀 Quick Actions")

    qa1, qa2, qa3, qa4 = st.columns(4)

    with qa1:
        st.button(
            "📝 Generate Notes",
            use_container_width=True,
            disabled=not st.session_state.get(
                "processed",
                False
            )
        )

    with qa2:
        st.button(
            "🎯 Generate MCQs",
            use_container_width=True,
            disabled=not st.session_state.get(
                "processed",
                False
            )
        )

    with qa3:
        st.button(
            "🃏 Flashcards",
            use_container_width=True,
            disabled=not st.session_state.get(
                "processed",
                False
            )
        )

    with qa4:
        st.button(
            "💬 Chat",
            use_container_width=True,
            disabled=not st.session_state.get(
                "processed",
                False
            )
        )

    st.markdown("---")

    # =========================
    # Main Features
    # =========================

    st.subheader("✨ Platform Features")

    col1, col2 = st.columns(2)

    with col1:

        st.container(
            border=True
        )

        st.markdown(
            """
            ### 📖 Study Tools

            Generate high quality learning material from uploaded PDFs.

            ✅ Notes

            ✅ Flashcards

            ✅ MCQs

            ✅ Question Banks
            """
        )

    with col2:

        st.container(
            border=True
        )

        st.markdown(
            """
            ### 📊 Analysis

            Understand your learning content better.

            ✅ Topic Extraction

            ✅ Coverage Analysis

            ✅ Importance Ranking
            """
        )

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            """
            ### 📝 Exam Preparation

            Prepare smarter with AI.

            ✅ Revision Sheets

            ✅ Mock Tests

            ✅ Important Questions
            """
        )

    with col4:

        st.markdown(
            """
            ### 💬 AI Assistant

            Interact directly with your documents.

            ✅ RAG Chat

            ✅ Semantic Search

            ✅ Context Aware Answers
            """
        )

    st.markdown("---")

    # =========================
    # Getting Started
    # =========================

    st.subheader("📌 Getting Started")

    st.success(
        """
        1. Upload PDFs from the sidebar
        
        2. Click Process Documents
        
        3. Navigate through Study Tools, Analysis, Exam Prep or Chat
        
        4. Generate personalized study material instantly
        """
    )

