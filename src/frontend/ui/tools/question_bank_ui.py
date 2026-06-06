import streamlit as st
import streamlit.components.v1 as components
from ingestion.retriever import retrieve
from study_tools.question_bank_generator import generate_question_bank

_CSS = """
<style>
.qb-root * { box-sizing: border-box; font-family: 'Inter', sans-serif; }
.qb-root .ph { margin-bottom: 14px; }
.qb-root .ph h3 { font-size: 1.1rem; font-weight: 700; color: #F8FAFC !important; margin: 0 0 2px; }
.qb-root .ph p  { font-size: 12.5px; color: #4B5A72 !important; margin: 0; }
.qb-root .lbl { font-size: 10.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #4B5A72; margin: 14px 0 8px; display: flex; align-items: center; gap: 8px; }
.qb-root .lbl::after { content: ""; flex: 1; height: 1px; background: #273449; }
.qb-root .cfg { background: #161B2E; border: 1px solid rgba(139,92,246,.2); border-radius: 12px; padding: 13px 17px; }
.qb-root .cfg .ct { font-size: 12.5px; font-weight: 600; color: #E2E8F0 !important; margin: 0 0 2px; display: block; }
.qb-root .cfg .cd { font-size: 11.5px; color: #4B5A72 !important; margin: 0; display: block; }
/* mark type pills */
.qb-root .mark-info { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; }
.qb-root .mp { background: #161B2E; border: 1px solid #273449; border-radius: 10px; padding: 10px 14px; }
.qb-root .mp .mv { font-size: 18px; font-weight: 800; color: #8B5CF6 !important; line-height: 1; display: block; }
.qb-root .mp .ml { font-size: 10.5px; color: #4B5A72 !important; margin-top: 2px; display: block; }
</style>
"""


def render_question_bank(vector_db):

    components.html(_CSS, height=0)

    st.markdown("""
<div class="qb-root">
  <div class="ph">
    <h3>📚 Question Bank Generator</h3>
    <p>Generate comprehensive 2, 5 and 10 mark questions for exam preparation</p>
  </div>
  <div class="lbl">Configuration</div>
  <div class="cfg">
    <span class="ct">Multi-mark question sets</span>
    <span class="cd">Set the number of questions per mark category — all generated from your uploaded documents</span>
  </div>
  <div class="lbl">Question Count</div>
</div>
""", unsafe_allow_html=True)

    topic = st.text_input(
        "Topic", key="qb_topic",
        placeholder="e.g. Thermodynamics, Civil War, Recursion…",
        label_visibility="collapsed")

    c1, c2, c3 = st.columns(3, gap="small")
    with c1:
        num_2_mark  = st.number_input("2 Mark Questions",  min_value=1, max_value=50, value=10)
    with c2:
        num_5_mark  = st.number_input("5 Mark Questions",  min_value=1, max_value=50, value=10)
    with c3:
        num_10_mark = st.number_input("10 Mark Questions", min_value=1, max_value=30, value=5)

    # Live count preview
    st.markdown(f"""
<div class="qb-root">
  <div class="lbl">Preview</div>
  <div class="mark-info">
    <div class="mp"><span class="mv">{num_2_mark}</span><span class="ml">2-mark questions</span></div>
    <div class="mp"><span class="mv">{num_5_mark}</span><span class="ml">5-mark questions</span></div>
    <div class="mp"><span class="mv">{num_10_mark}</span><span class="ml">10-mark questions</span></div>
  </div>
  <div class="lbl">Generate</div>
</div>
""", unsafe_allow_html=True)

    total = num_2_mark + num_5_mark + num_10_mark

    if st.button(f"📚 Generate {total} Questions", use_container_width=True, type="primary"):
        if not topic.strip():
            st.warning("Please enter a topic first."); return

        docs = retrieve(topic, vector_db)
        if not docs:
            st.warning("No relevant content found for that topic."); return

        context = "\n".join(doc.page_content for doc in docs)

        with st.spinner("Generating question bank…"):
            questions = generate_question_bank(context, num_2_mark, num_5_mark, num_10_mark)

        st.markdown("---")
        st.markdown(f"#### 📚 Question Bank — {topic}")
        st.markdown(questions)

        if "Generated Question Bank" not in st.session_state.get("activity_log", []):
            st.session_state.activity_log.append("Generated Question Bank")
