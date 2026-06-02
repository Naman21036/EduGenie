import streamlit as st

from src.ingestion.retriever import retrieve

from src.study_tools.revision_sheet_generator import (
    generate_revision_sheet
)

from src.study_tools.mock_test_generator import (
    generate_mock_test
)


def render_exam_prep(vector_db):

    st.header("📝 Exam Preparation")

    query = st.text_input(
        "Enter a topic",
        placeholder="Neural Networks, Operating Systems, DBMS...",
        key="exam_query"
    )

    if not query:
        st.info(
            "Enter a topic to generate exam preparation material."
        )
        return

    results = retrieve(
        query,
        vector_db
    )

    context = "\n".join(
        [doc.page_content for doc in results]
    )

    revision_tab, mock_test_tab = st.tabs(
        [
            "Revision Sheet",
            "Mock Test"
        ]
    )

    # Revision Sheet

    with revision_tab:

        if st.button(
            "Generate Revision Sheet",
            use_container_width=True
        ):

            with st.spinner(
                "Generating revision sheet..."
            ):

                revision_sheet = generate_revision_sheet(
                    context
                )

                st.write(
                    revision_sheet
                )

    # Mock Test

    with mock_test_tab:

        num_questions = st.number_input(
            "Number of Questions",
            min_value=5,
            max_value=100,
            value=20
        )

        if st.button(
            "Generate Mock Test",
            use_container_width=True
        ):

            with st.spinner(
                "Generating mock test..."
            ):

                mock_test = generate_mock_test(
                    context,
                    num_questions
                )

                st.json(
                    mock_test
                )