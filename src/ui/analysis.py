import streamlit as st

from src.ingestion.retriever import retrieve

from src.analysis.topic_extractor import generate_topic_extractor
from src.analysis.topic_coverage import generate_topic_coverage
from src.analysis.importance_ranker import generate_importance_ranker


def render_analysis(vector_db):

    st.header("📊 Document Analysis")

    query = st.text_input(
        "Enter a topic",
        placeholder="Machine Learning, CNN, Operating Systems...",
        key="analysis_query"
    )

    if not query:
        st.info(
            "Enter a topic to analyze."
        )
        return

    results = retrieve(
        query,
        vector_db
    )

    context = "\n".join(
        [doc.page_content for doc in results]
    )

    topics_tab, coverage_tab, importance_tab = st.tabs(
        [
            "Topics",
            "Coverage",
            "Importance"
        ]
    )

    # Topic Extraction

    with topics_tab:

        if st.button(
            "Extract Topics",
            use_container_width=True
        ):

            with st.spinner(
                "Extracting topics..."
            ):

                topics = generate_topic_extractor(
                    context
                )

                st.json(
                    topics
                )

    # Topic Coverage Analysis

    with coverage_tab:

        if st.button(
            "Analyze Coverage",
            use_container_width=True
        ):

            with st.spinner(
                "Analyzing topic coverage..."
            ):

                coverage = generate_topic_coverage(
                    context
                )

                st.json(
                    coverage
                )

    # Importance Ranking

    with importance_tab:

        if st.button(
            "Rank Topics",
            use_container_width=True
        ):

            with st.spinner(
                "Ranking topics..."
            ):

                rankings = generate_importance_ranker(
                    context,
                    topics
                )

                st.json(
                    rankings
                )