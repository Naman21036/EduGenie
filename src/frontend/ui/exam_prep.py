from pathlib import Path
import json
import streamlit as st
import streamlit.components.v1 as components

from src.ingestion.retriever import retrieve

from src.study_tools.mock_test_generator import (
    generate_mock_test
)

from src.study_tools.revision_sheet_generator import (
    generate_revision_sheet
)
from src.frontend.exam_prep.mock_test_engine import (
    initialize_test,
    render_mock_test,
    reset_test
)

def safe_json(data):

    if isinstance(data, dict):
        return data

    if isinstance(data, str):

        try:
            return json.loads(data)
        except:
            return {}

    return {}
def render_revision_sheet(sheet):

    st.subheader(
        "📌 Summary"
    )

    if not sheet.get("success", True):

        st.error(
            sheet.get(
                "error",
                "JSON Parsing Failed"
            )
        )

        st.code(
            sheet.get(
                "raw_response",
                ""
            )
        )

        return

    definitions = sheet.get(
        "important_definitions",
        []
    )

    if definitions:

        st.subheader(
            "📖 Definitions"
        )

        for d in definitions:

            st.markdown(
                f"""
**{d.get('term','')}**

{d.get('definition','')}
"""
            )

    formulas = sheet.get(
        "important_formulas",
        []
    )

    if formulas:

        st.subheader(
            "🧮 Formulas"
        )

        for f in formulas:

            st.code(
                f.get(
                    "formula",
                    ""
                )
            )

            st.caption(
                f.get(
                    "explanation",
                    ""
                )
            )

    concepts = sheet.get(
        "important_concepts",
        []
    )

    if concepts:

        st.subheader(
            "💡 Concepts"
        )

        for c in concepts:

            st.markdown(
                f"• {c}"
            )

    questions = sheet.get(
        "most_important_questions",
        []
    )

    if questions:

        st.subheader(
            "🔥 Most Important Questions"
        )

        for q in questions:

            st.markdown(
                f"• {q}"
            )

def render_exam_prep(vector_db):

    base = Path(
        "src/frontend/exam_prep"
    )

    html = (
        base /
        "exam_prep.html"
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
        "exam_prep.css"
    ).read_text(
        encoding="utf-8"
    )

    css = theme_css + "\n" + page_css

    js = (
        base /
        "exam_prep.js"
    ).read_text(
        encoding="utf-8"
    )

    html = (
        html
        .replace(
            "{{DOCS}}",
            str(
                st.session_state.get(
                    "doc_count",
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
        key="exam_topic"
    )

    col1, col2 = st.columns(2)

    with col1:

        mock_test_btn = st.button(
            "📝 Generate Mock Test",
            use_container_width=True
        )

    with col2:

        revision_btn = st.button(
            "⚡ Generate Revision Sheet",
            use_container_width=True
        )

    if (
        mock_test_btn
        or revision_btn
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

        if revision_btn:

            st.subheader(
                "⚡ Revision Sheet"
            )

            sheet = generate_revision_sheet(
                context
            )

            render_revision_sheet(
                safe_json(sheet)
            )

        if mock_test_btn:

            mock_test = generate_mock_test(
                context,
                num_2_mark=5,
                num_5_mark=0,
                num_10_mark=0,
                difficulty="Mixed"
            )

            if (
                not mock_test.get(
                    "success",
                    True
                )
                and
                "mcqs"
                not in mock_test
            ):

                st.error(
                    mock_test.get(
                        "error",
                        "Mock Test Generation Failed"
                    )
                )

                if (
                    "raw_response"
                    in mock_test
                ):

                    st.code(
                        mock_test[
                            "raw_response"
                        ]
                    )

                return

            initialize_test(
                mock_test
            )

    if (
        "mock_test"
        in st.session_state
    ):

        st.subheader(
            "📝 Interactive Mock Test"
        )

        render_mock_test()

        reset_test()