import json
import streamlit as st

from ingestion.retriever import retrieve
from study_tools.mcq_generator import generate_mcqs


MCQ_CSS = """
<style>
.mcq-header { margin-bottom: 18px; }
.mcq-header h3 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 4px;
    letter-spacing: -0.02em;
}
.mcq-header p { font-size: 13px; color: #475569; margin: 0; }

.mcq-config {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 16px;
}
.mcq-config .mc-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 14px;
}

/* MCQ card */
.mcq-card {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 12px;
    position: relative;
}
.mcq-card .mcq-num {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 8px;
}
.mcq-card .mcq-question {
    font-size: 14px;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 14px;
    line-height: 1.5;
}
.mcq-option {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 6px;
    font-size: 13px;
    color: #94a3b8;
    background: rgba(255,255,255,0.02);
}
.mcq-option .opt-label {
    font-size: 11px;
    font-weight: 700;
    color: #3b82f6;
    flex-shrink: 0;
    margin-top: 1px;
}
/* ── Generate Button Override ───────────────────── */

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

div[data-testid="stButton"] > button p {

    color: #ffffff !important;
}
</style>
"""

_OPTION_LABELS = ["A", "B", "C", "D", "E"]


def _parse_mcqs(raw):
    """Normalise MCQ output — accepts dict (error), list, or JSON string."""
    if isinstance(raw, dict):
        return None, raw.get("error", "Generation failed"), raw.get("raw_response", "")
    if isinstance(raw, str):
        cleaned = raw.replace("```json", "").replace("```", "").strip()
        try:
            raw = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            return None, f"Could not parse model output: {exc}", cleaned
    if not isinstance(raw, list):
        return None, "Unexpected output format from model.", str(raw)
    parsed = []
    for item in raw:
        if isinstance(item, str):
            try:
                item = json.loads(item)
            except Exception:
                continue
        if isinstance(item, dict):
            parsed.append(item)
    return parsed, None, None


def render_mcqs(vector_db):

    st.markdown(MCQ_CSS, unsafe_allow_html=True)

    # ── Header ───────────────────────────────────────
    st.markdown(
        '<div class="mcq-header">'
        '<h3>🎯 MCQ Generator</h3>'
        '<p>Generate exam-style multiple choice questions with instant answer reveal.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Configuration panel ───────────────────────────
    st.markdown(
        '<div class="mcq-config"><div class="mc-title">Configuration</div></div>',
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Topic",
        key="mcq_topic",
        placeholder="e.g. Cell Division, Thermodynamics, World War II…",
    )

    num_mcqs = st.number_input(
        "Number of MCQs",
        min_value=1,
        max_value=10,
        value=5,
        key="mcq_count",
    )

    # ── Generate ──────────────────────────────────────
    generate_btn = st.button(
        f"🎯 Generate {int(num_mcqs)} MCQ{'s' if num_mcqs != 1 else ''}",
        key="mcq_btn",
        use_container_width=True,
    )

    if generate_btn:

        if not topic.strip():
            st.warning("Please enter a topic before generating MCQs.")
            return

        docs = retrieve(topic, vector_db)

        if not docs:
            st.warning("No relevant content found for that topic. Try a different keyword.")
            return

        context = "\n".join(doc.page_content for doc in docs)

        with st.spinner(f"Generating {int(num_mcqs)} MCQs…"):
            raw = generate_mcqs(context, num_mcqs)

        mcqs, err_msg, raw_response = _parse_mcqs(raw)

        if err_msg:
            st.error(err_msg)
            if raw_response:
                with st.expander("Raw model output"):
                    st.code(raw_response)
            return

        if not mcqs:
            st.error("No questions were returned. Please try again.")
            return

        # ── Render MCQ cards ──────────────────────────
        st.markdown(
            f'<p style="font-size:13px; color:#475569; margin:16px 0 12px;">'
            f'{len(mcqs)} question{"s" if len(mcqs) != 1 else ""} generated</p>',
            unsafe_allow_html=True,
        )

        for idx, mcq in enumerate(mcqs):
            question = mcq.get("question", "")
            options  = mcq.get("options", [])
            answer   = mcq.get("answer", "")

            options_html = "".join(
                f'<div class="mcq-option">'
                f'<span class="opt-label">{_OPTION_LABELS[i] if i < len(_OPTION_LABELS) else str(i+1)}</span>'
                f'<span>{opt}</span>'
                f'</div>'
                for i, opt in enumerate(options)
            )

            st.markdown(
                f'<div class="mcq-card">'
                f'<div class="mcq-num">Question {idx + 1} of {len(mcqs)}</div>'
                f'<div class="mcq-question">{question}</div>'
                f'{options_html}'
                f'</div>',
                unsafe_allow_html=True,
            )

            with st.expander("Show Answer"):
                st.success(answer)

        # ── Activity log ──────────────────────────────
        if "activity_log" not in st.session_state:
            st.session_state.activity_log = []
        entry = f"Generated {len(mcqs)} MCQs"
        if entry not in st.session_state.activity_log:
            st.session_state.activity_log.append(entry)
