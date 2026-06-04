import json
import streamlit as st

from src.ingestion.retriever import retrieve
from src.study_tools.mcq_generator import generate_mcqs


def render_mcqs(vector_db):

    st.subheader("🎯 MCQ Generator")

    topic = st.text_input(
        "Topic",
        key="mcq_topic"
    )

    num_mcqs = st.number_input(
        "Number of MCQs",
        min_value=1,
        max_value=10,
        value=5
    )

    if st.button(
        "Generate MCQs"
    ):

        if not topic.strip():

            st.warning(
                "Please enter a topic."
            )

            return

        docs = retrieve(
            topic,
            vector_db
        )

        context = "\n".join(
            [
                doc.page_content
                for doc in docs
            ]
        )

        mcqs = generate_mcqs(
            context,
            num_mcqs
        )
        
        if isinstance(mcqs, dict):

            st.error(
                mcqs.get(
                    "error",
                    "Failed to generate MCQs"
                )
            )

            st.code(
                mcqs.get(
                    "raw_response",
                    ""
                )
            )

            return

        if isinstance(mcqs, str):

            mcqs = (
                mcqs
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            mcqs = json.loads(mcqs)

        for idx, mcq in enumerate(mcqs):

            st.markdown(
                f"### Q{idx+1}. {mcq['question']}"
            )

            for option in mcq["options"]:

                st.write(
                    f"• {option}"
                )

            with st.expander(
                "Show Answer"
            ):

                st.success(
                    mcq["answer"]
                )

            st.divider()

        st.session_state.activity_log.append(
            f"Generated {num_mcqs} MCQs"
        )