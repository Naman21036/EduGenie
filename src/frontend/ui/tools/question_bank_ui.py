import streamlit as st

from ingestion.retriever import retrieve
from study_tools.question_bank_generator import generate_question_bank


QB_CSS = """
<style>
.qb-header { margin-bottom: 18px; }
.qb-header h3 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 4px;
    letter-spacing: -0.02em;
}
.qb-header p { font-size: 13px; color: #475569; margin: 0; }

.qb-config {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 12px;
}
.qb-config .qc-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 14px;
}

/* Preview panel */
.qb-preview {
    background: #0f172a;
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.qb-preview .qp-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 12px;
}
.qb-preview-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 7px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 13px;
}
.qb-preview-row:last-child { border-bottom: none; }
.qb-preview-row .pr-label { color: #94a3b8; }
.qb-preview-row .pr-val { font-weight: 700; color: #60a5fa; }
.qb-preview-row.total .pr-label { color: #e2e8f0; font-weight: 600; }
.qb-preview-row.total .pr-val { color: #f8fafc; font-size: 15px; }

.qb-result {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 22px 24px;
    margin-top: 16px;
}
.qb-result .qr-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
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

/* Disabled state */

div[data-testid="stButton"] > button:disabled {

    background: #1e293b !important;

    color: #64748b !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    box-shadow: none !important;

    cursor: not-allowed !important;
}
</style>
"""


def render_question_bank(vector_db):

    st.markdown(QB_CSS, unsafe_allow_html=True)

    # ── Header ───────────────────────────────────────
    st.markdown(
        '<div class="qb-header">'
        '<h3>📚 Question Bank Generator</h3>'
        '<p>Build a comprehensive set of questions.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Configuration panel ───────────────────────────
    st.markdown(
        '<div class="qb-config"><div class="qc-title">Configuration</div></div>',
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Topic",
        key="qb_topic",
        placeholder="e.g. Organic Chemistry, Cold War, Data Structures…",
    )

    col1, col2, col3 = st.columns(3, gap="small")

    with col1:
        num_2_mark = st.number_input(
            "2 Mark Questions",
            min_value=0,
            max_value=10,
            value=5,
            key="qb_2mark",
        )

    with col2:
        num_5_mark = st.number_input(
            "5 Mark Questions",
            min_value=0,
            max_value=10,
            value=2,
            key="qb_5mark",
        )

    with col3:
        num_10_mark = st.number_input(
            "10 Mark Questions",
            min_value=0,
            max_value=10,
            value=3,
            key="qb_10mark",
        )

    # ── Live preview panel ────────────────────────────
    total = int(num_2_mark) + int(num_5_mark) + int(num_10_mark)

    st.markdown(
        '<div class="qb-preview">'
        '<div class="qp-title">Question Preview</div>'
        '<div class="qb-preview-row">'
        f'<span class="pr-label">2 Mark Questions</span>'
        f'<span class="pr-val">{int(num_2_mark)}</span>'
        '</div>'
        '<div class="qb-preview-row">'
        f'<span class="pr-label">5 Mark Questions</span>'
        f'<span class="pr-val">{int(num_5_mark)}</span>'
        '</div>'
        '<div class="qb-preview-row">'
        f'<span class="pr-label">10 Mark Questions</span>'
        f'<span class="pr-val">{int(num_10_mark)}</span>'
        '</div>'
        '<div class="qb-preview-row total">'
        f'<span class="pr-label">Total Questions</span>'
        f'<span class="pr-val">{total}</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Generate ──────────────────────────────────────
    generate_btn = st.button(
        f"📚 Generate {total} Question{'s' if total != 1 else ''}",
        key="qb_btn",
        use_container_width=True,
        disabled=(total == 0),
    )

    if generate_btn:

        if not topic.strip():
            st.warning("Please enter a topic before generating questions.")
            return

        if total == 0:
            st.warning("Set at least one question count above zero.")
            return

        docs = retrieve(topic, vector_db)

        if not docs:
            st.warning("No relevant content found for that topic. Try a different keyword.")
            return

        context = "\n".join(doc.page_content for doc in docs)

        with st.spinner(f"Generating {total} questions…"):
            questions = generate_question_bank(
                context,
                int(num_2_mark),
                int(num_5_mark),
                int(num_10_mark),
            )

        if not questions or (isinstance(questions, str) and not questions.strip()):
            st.error("The model returned an empty question bank. Please try again.")
            return

        # ── Results ───────────────────────────────────
        st.markdown(
            '<div class="qb-result"><div class="qr-title">Generated Question Bank</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown(questions)

        # ── Activity log ──────────────────────────────
        if "activity_log" not in st.session_state:
            st.session_state.activity_log = []
        entry = f"Generated Question Bank ({total} questions)"
        if entry not in st.session_state.activity_log:
            st.session_state.activity_log.append(entry)
