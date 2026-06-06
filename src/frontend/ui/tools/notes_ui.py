import streamlit as st
import streamlit.components.v1 as components
from ingestion.retriever import retrieve
from study_tools.notes_generator import generate_notes

_CSS = """
<style>
.notes-root * { box-sizing: border-box; font-family: 'Inter', sans-serif; }
.notes-root .ph { margin-bottom: 14px; }
.notes-root .ph h3 { font-size: 1.1rem; font-weight: 700; color: #F8FAFC !important; margin: 0 0 2px; }
.notes-root .ph p  { font-size: 12.5px; color: #4B5A72 !important; margin: 0; }
.notes-root .lbl { font-size: 10.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #4B5A72; margin: 14px 0 8px; display: flex; align-items: center; gap: 8px; }
.notes-root .lbl::after { content: ""; flex: 1; height: 1px; background: #273449; }
.notes-root .cfg { background: #161B2E; border: 1px solid rgba(59,130,246,.2); border-radius: 12px; padding: 13px 17px; }
.notes-root .cfg .ct { font-size: 12.5px; font-weight: 600; color: #E2E8F0 !important; margin: 0 0 2px; display: block; }
.notes-root .cfg .cd { font-size: 11.5px; color: #4B5A72 !important; margin: 0; display: block; }
</style>
"""


def render_notes(vector_db):

    components.html(_CSS, height=0)

    st.markdown("""
<div class="notes-root">
  <div class="ph">
    <h3>📄 Notes Generator</h3>
    <p>Generate structured, comprehensive study notes from your uploaded documents</p>
  </div>
  <div class="lbl">Configuration</div>
  <div class="cfg">
    <span class="ct">Topic-based extraction</span>
    <span class="cd">Enter a topic below — the AI will retrieve relevant content and generate structured notes</span>
  </div>
  <div class="lbl">Generate</div>
</div>
""", unsafe_allow_html=True)

    topic = st.text_input(
        "Topic",
        key="notes_topic",
        placeholder="e.g. Machine Learning, Photosynthesis, French Revolution…",
        label_visibility="collapsed",
    )

    if st.button("📄 Generate Notes", use_container_width=True, type="primary"):
        if not topic.strip():
            st.warning("Please enter a topic first.")
            return

        docs = retrieve(topic, vector_db)
        if not docs:
            st.warning("No relevant content found for that topic.")
            return

        context = "\n".join(doc.page_content for doc in docs)

        with st.spinner("Generating notes…"):
            notes = generate_notes(context)

        st.markdown("---")
        st.markdown("#### 📄 Generated Notes")
        st.markdown(notes)

        if "Generated Notes" not in st.session_state.get("activity_log", []):
            st.session_state.activity_log.append("Generated Notes")
