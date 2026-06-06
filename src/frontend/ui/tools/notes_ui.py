import streamlit as st

from ingestion.retriever import retrieve
from study_tools.notes_generator import generate_notes


NOTES_CSS = """
<style>
.notes-header { margin-bottom: 18px; }
.notes-header h3 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 4px;
    letter-spacing: -0.02em;
}
.notes-header p { font-size: 13px; color: #475569; margin: 0; }

.notes-config {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 16px;
}
.notes-config .nc-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 14px;
}
.notes-result {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 22px 24px;
    margin-top: 16px;
}
.notes-result .nr-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
/* Generate button override */

div[data-testid="stButton"] > button {

    background: linear-gradient(
        135deg,
        #2563eb,
        #0891b2
    ) !important;

    color: #ffffff !important;

    border: none !important;

    border-radius: 12px !important;

    font-weight: 600 !important;

    transition: all .2s ease !important;
}

div[data-testid="stButton"] > button:hover {

    background: linear-gradient(
        135deg,
        #3b82f6,
        #06b6d4
    ) !important;

    transform: translateY(-2px);

    box-shadow:
        0 8px 20px rgba(
            6,
            182,
            212,
            .35
        ) !important;
}
</style>
"""


def render_notes(vector_db):

    st.markdown(NOTES_CSS, unsafe_allow_html=True)

    # ── Header ───────────────────────────────────────
    st.markdown(
        '<div class="notes-header">'
        '<h3>📄 Notes Generator</h3>'
        '<p>Generate structured, topic-focused study notes from your uploaded documents.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Configuration panel ───────────────────────────
    st.markdown(
        '<div class="notes-config"><div class="nc-title">Configuration</div></div>',
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Topic",
        key="notes_topic",
        placeholder="e.g. Photosynthesis, Newton's Laws, French Revolution…",
        label_visibility="visible",
    )

    detail_level = st.select_slider(
        "Detail level",
        options=["Brief", "Standard", "Detailed"],
        value="Standard",
        key="notes_detail",
    )

    # ── Generate ──────────────────────────────────────
    generate_btn = st.button(
        "📄 Generate Notes",
        key="notes_btn",
        use_container_width=True,
    )

    if generate_btn:

        if not topic.strip():
            st.warning("Please enter a topic before generating notes.")
            return

        docs = retrieve(topic, vector_db)

        if not docs:
            st.warning("No relevant content found for that topic. Try a different keyword.")
            return

        context = "\n".join(doc.page_content for doc in docs)

        with st.spinner("Generating Notes…"):
            notes = generate_notes(context)

        if not notes or not notes.strip():
            st.error("The model returned empty notes. Please try again.")
            return

        # ── Results ───────────────────────────────────
        st.markdown(
            '<div class="notes-result"><div class="nr-title">Generated Notes</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown(notes)

        # ── Activity log ──────────────────────────────
        if "activity_log" not in st.session_state:
            st.session_state.activity_log = []
        if "Generated Notes" not in st.session_state.activity_log:
            st.session_state.activity_log.append("Generated Notes")
