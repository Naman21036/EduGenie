from pathlib import Path
import json
import streamlit as st
import streamlit.components.v1 as components

from src.ingestion.retriever import retrieve

from src.analysis.topic_extractor import (
    generate_topic_extractor
)

from src.analysis.topic_coverage import (
    generate_topic_coverage
)

from src.analysis.importance_ranker import (
    generate_importance_ranker
)



def render_topics(result):

    topics = result.get("topics", [])

    for item in topics:

        st.markdown(
            f"### 📚 {item.get('topic','Unknown')}"
        )

        for sub in item.get(
            "subtopics",
            []
        ):
            st.markdown(
                f"• {sub}"
            )

        st.divider()


def render_coverage(result):

    coverage = result.get(
        "topic_coverage",
        []
    )

    for item in coverage:

        st.markdown(
            f"### 📊 {item.get('topic','Unknown')}"
        )

        percentage = int(
            item.get(
                "coverage_percentage",
                0
            )
        )

        st.progress(
            min(
                max(
                    percentage,
                    0
                ),
                100
            )
        )

        st.caption(
            f"{percentage}% • {item.get('coverage_level','Unknown')}"
        )

        subs = item.get(
            "subtopics",
            []
        )

        if subs:
            st.write(
                ", ".join(subs)
            )

        st.divider()


def render_importance(result):

    ranked = result.get(
        "ranked_topics",
        []
    )

    medals = [
        "🥇",
        "🥈",
        "🥉"
    ]

    for idx, topic in enumerate(
        ranked
    ):

        icon = (
            medals[idx]
            if idx < 3
            else "⭐"
        )

        score = int(
            topic.get(
                "importance_score",
                0
            )
        )

        st.markdown(
            f"""
### {icon} {topic.get('topic','Unknown')}

**Importance Score:** {score}/100

{topic.get('reason','')}
"""
        )

        st.progress(
            min(
                max(
                    score,
                    0
                ),
                100
            )
        )

        st.divider()


def safe_json(data):

    if isinstance(data, dict):
        return data

    if isinstance(data, str):

        try:
            return json.loads(data)
        except:
            return {}

    return {}

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

    theme_css = (
        Path(
            "src/frontend/shared/theme.css"
        )
    ).read_text(
        encoding="utf-8"
    )

    page_css = (
        base /
        "analysis.css"
    ).read_text(
        encoding="utf-8"
    )

    css = theme_css + "\n" + page_css

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
        <style>
        {css}
        </style>

        {html}

        <script>
        {js}
        </script>
        """,
        height=1000,
        scrolling=True
    )

    st.divider()

    topic = st.text_input(
        "Topic",
        key="analysis_topic"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        topic_extract = st.button(
            "🧠 Topic Extraction",
            use_container_width=True
        )

    with col2:

        topic_coverage = st.button(
            "📈 Topic Coverage",
            use_container_width=True
        )

    with col3:

        importance_rank = st.button(
            "⭐ Importance Ranking",
            use_container_width=True
        )

    if (
        topic_extract
        or topic_coverage
        or importance_rank
    ):

        if not topic:

            st.warning(
                "Please enter a topic."
            )
            return

        docs = retrieve(
            topic,
            vector_db
        )

        if not docs:

            st.warning(
                "No relevant content found."
            )
            return

        context = "\n".join(
            [
                doc.page_content
                for doc in docs
            ]
        )

        if topic_extract:

            st.subheader(
                "🧠 Extracted Topics"
            )

            result = generate_topic_extractor(
                context
            )

            render_topics(
                safe_json(result)
            )

        if topic_coverage:

            st.subheader(
                "📈 Topic Coverage"
            )

            result = generate_topic_coverage(
                context
            )

            render_coverage(
                safe_json(result)
            )

        if importance_rank:

            st.subheader(
                "⭐ Importance Ranking"
            )

            topics = generate_topic_extractor(
                context
            )

            result = generate_importance_ranker(
                context,
                topics
            )

            render_importance(
                safe_json(result)
            )