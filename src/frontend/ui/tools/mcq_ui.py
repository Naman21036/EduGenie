import json
import streamlit as st
import streamlit.components.v1 as components
from ingestion.retriever import retrieve
from study_tools.mcq_generator import generate_mcqs

_CSS = """
<style>
.mcq-root * { box-sizing: border-box; font-family: 'Inter', sans-serif; }
.mcq-root .ph { margin-bottom: 14px; }
.mcq-root .ph h3 { font-size: 1.1rem; font-weight: 700; color: #F8FAFC !important; margin: 0 0 2px; }
.mcq-root .ph p  { font-size: 12.5px; color: #4B5A72 !important; margin: 0; }
.mcq-root .lbl { font-size: 10.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #4B5A72; margin: 14px 0 8px; display: flex; align-items: center; gap: 8px; }
.mcq-root .lbl::after { content: ""; flex: 1; height: 1px; background: #273449; }
.mcq-root .cfg { background: #161B2E; border: 1px solid rgba(59,130,246,.2); border-radius: 12px; padding: 13px 17px; }
.mcq-root .cfg .ct { font-size: 12.5px; font-weight: 600; color: #E2E8F0 !important; margin: 0 0 2px; display: block; }
.mcq-root .cfg .cd { font-size: 11.5px; color: #4B5A72 !important; margin: 0; display: block; }

/* MCQ result card */
.mcq-card { background: #161B2E; border: 1px solid #273449; border-radius: 12px; padding: 16px 18px; margin-bottom: 10px; }
.mcq-card .qnum { font-size: 10.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #3B82F6 !important; margin: 0 0 6px; display: block; }
.mcq-card .qtxt { font-size: 14px; font-weight: 600; color: #F8FAFC !important; margin: 0 0 12px; line-height: 1.5; display: block; }
.mcq-card .opt  { display: flex; align-items: flex-start; gap: 8px; padding: 7px 10px; border-radius: 8px; margin-bottom: 5px; border: 1px solid #273449; font-size: 13px; color: #94A3B8 !important; }
.mcq-card .opt .ob { font-size: 10.5px; font-weight: 700; color: #60A5FA !important; flex-shrink: 0; margin-top: 1px; }
</style>
"""


def _safe_parse(mcqs):
    if isinstance(mcqs, list): return mcqs
    if isinstance(mcqs, str):
        cleaned = mcqs.replace("```json","").replace("```","").strip()
        try: return json.loads(cleaned)
        except: return []
    return []


def render_mcqs(vector_db):

    components.html(_CSS, height=0)

    st.markdown("""
<div class="mcq-root">
  <div class="ph">
    <h3>🎯 MCQ Generator</h3>
    <p>Generate multiple choice questions with instant answer reveal</p>
  </div>
  <div class="lbl">Configuration</div>
  <div class="cfg">
    <span class="ct">Auto-generated exam questions</span>
    <span class="cd">Enter a topic and set the number of questions — answers are hidden until revealed</span>
  </div>
  <div class="lbl">Generate</div>
</div>
""", unsafe_allow_html=True)

    topic = st.text_input(
        "Topic", key="mcq_topic",
        placeholder="e.g. Newton's Laws, World War II, Cell Biology…",
        label_visibility="collapsed")

    num_mcqs = st.slider("Number of MCQs", min_value=1, max_value=10, value=5)

    if st.button("🎯 Generate MCQs", use_container_width=True, type="primary"):
        if not topic.strip():
            st.warning("Please enter a topic first."); return

        docs = retrieve(topic, vector_db)
        if not docs:
            st.warning("No relevant content found for that topic."); return

        context = "\n".join(doc.page_content for doc in docs)

        with st.spinner("Generating MCQs…"):
            raw = generate_mcqs(context, num_mcqs)

        if isinstance(raw, dict):
            st.error(raw.get("error", "Failed to generate MCQs"))
            if "raw_response" in raw: st.code(raw["raw_response"])
            return

        mcqs = _safe_parse(raw)
        if not mcqs:
            st.warning("Could not parse MCQ response."); return

        st.markdown("---")
        st.markdown(f"#### 🎯 {len(mcqs)} Multiple Choice Questions")

        option_labels = ["A", "B", "C", "D", "E"]

        for idx, mcq in enumerate(mcqs):
            question = mcq.get("question", "")
            options  = mcq.get("options", [])
            answer   = mcq.get("answer", "")

            opts_html = "".join(
                f'<div class="opt"><span class="ob">{option_labels[i] if i < len(option_labels) else i+1}.</span> {opt}</div>'
                for i, opt in enumerate(options)
            )

            st.markdown(f"""
<div class="mcq-card">
  <span class="qnum">Question {idx+1} of {len(mcqs)}</span>
  <span class="qtxt">{question}</span>
  {opts_html}
</div>
""", unsafe_allow_html=True)

            with st.expander("Show Answer"):
                st.success(answer)

        st.session_state.activity_log.append(f"Generated {len(mcqs)} MCQs")
