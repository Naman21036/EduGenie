import json
import streamlit as st
from src.ingestion.retriever import retrieve
from src.study_tools.mock_test_generator import generate_mock_test
from src.study_tools.revision_sheet_generator import generate_revision_sheet
from src.frontend.exam_prep.mock_test_engine import initialize_test, render_mock_test, reset_test


# ── CSS ──────────────────────────────────────────────────────────────────────

EXAM_CSS = """
<style>
/* ── Page header ── */
.ep-header { margin-bottom: 22px; }
.ep-header h2 {
    font-size: 1.35rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 4px;
    letter-spacing: -0.02em;
}
.ep-header p { font-size: 13px; color: #475569; margin: 0; }

/* ── Section label ── */
.ep-label {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin: 22px 0 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.ep-label::after { content:""; flex:1; height:1px; background:rgba(255,255,255,0.05); }

/* ── Feature cards ── */
.ep-features { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.ep-feature {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
}
.ep-feature::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 14px 14px 0 0;
}
.ep-feature.mock::before     { background: #6366f1; }
.ep-feature.revision::before { background: #22c55e; }
.ep-feature .ef-icon  { font-size: 24px; margin-bottom: 10px; }
.ep-feature h4 { font-size: 14px; font-weight: 700; color: #e2e8f0; margin: 0 0 6px; }
.ep-feature p  { font-size: 12.5px; color: #475569; margin: 0 0 12px; line-height: 1.5; }
.ep-feature ul { padding-left: 16px; margin: 0; }
.ep-feature li { font-size: 12px; color: #64748b; margin-bottom: 3px; }

/* ── Difficulty selector ── */
.diff-row { display: flex; gap: 8px; }
.diff-btn {
    flex: 1;
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 10px;
    text-align: center;
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    color: #64748b;
    transition: all 0.15s;
}
.diff-btn.active { border-color: #6366f1; color: #a5b4fc; background: rgba(99,102,241,0.08); }

/* ── Prep overview ── */
.prep-stats { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; }
.prep-stat {
    background: #0c1120;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 14px 16px;
}
.prep-stat .ps-val { font-size: 22px; font-weight: 800; color: #a5b4fc; letter-spacing:-0.02em; }
.prep-stat .ps-lbl { font-size: 11px; color: #475569; margin-top: 3px; }

/* ── Readiness panel ── */
.readiness-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.readiness-panel {
    background: #0c1120;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 18px 20px;
}
.readiness-panel .rp-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #475569;
    margin: 0 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.readiness-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 13px;
}
.readiness-row:last-child { border-bottom: none; }
.readiness-row .rr-label { color: #94a3b8; }
.readiness-row .rr-badge {
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
}
.rr-badge.ready   { background: rgba(34,197,94,0.1);  color: #4ade80; }
.rr-badge.pending { background: rgba(99,102,241,0.1); color: #818cf8; }

/* ── AI recommendation ── */
.ep-rec {
    background: linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 14px;
    padding: 18px 20px;
}
.ep-rec .rec-tag {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6366f1;
    margin: 0 0 8px;
}
.ep-rec .rec-body { font-size: 13px; color: #cbd5e1; line-height: 1.65; }
.ep-rec ol { padding-left: 18px; margin: 8px 0 0; }
.ep-rec li { font-size: 13px; color: #94a3b8; margin-bottom: 4px; }

/* ── Action area ── */
.ep-action {
    background: #0c1120;
    border: 1px solid rgba(99,102,241,0.14);
    border-radius: 14px;
    padding: 20px 22px;
}
.ep-action .ea-title {
    font-size: 13px;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 14px;
}
</style>
"""


def safe_json(data):
    if isinstance(data, dict):
        return data
    if isinstance(data, str):
        try:
            return json.loads(data)
        except Exception:
            return {}
    return {}


def render_revision_sheet(sheet):
    if not sheet.get("success", True):
        st.error(sheet.get("error", "JSON Parsing Failed"))
        st.code(sheet.get("raw_response", ""))
        return

    definitions = sheet.get("important_definitions", [])
    if definitions:
        st.markdown("#### 📖 Definitions")
        for d in definitions:
            st.markdown(f"**{d.get('term','')}**")
            st.caption(d.get("definition", ""))

    formulas = sheet.get("important_formulas", [])
    if formulas:
        st.markdown("#### 🧮 Formulas")
        for f in formulas:
            st.code(f.get("formula", ""))
            st.caption(f.get("explanation", ""))

    concepts = sheet.get("important_concepts", [])
    if concepts:
        st.markdown("#### 💡 Key Concepts")
        for c in concepts:
            st.markdown(f"• {c}")

    questions = sheet.get("most_important_questions", [])
    if questions:
        st.markdown("#### 🔥 Most Important Questions")
        for q in questions:
            st.markdown(f"• {q}")


# ── Helper: build readiness rows ─────────────────────────────────────────────

def _readiness_row(label, ready):
    badge_cls = "ready" if ready else "pending"
    badge_txt = "Ready"  if ready else "Pending"
    return f"""
    <div class="readiness-row">
        <span class="rr-label">{label}</span>
        <span class="rr-badge {badge_cls}">{badge_txt}</span>
    </div>
    """


# ── Main render ──────────────────────────────────────────────────────────────

def render_exam_prep(vector_db):

    st.markdown(EXAM_CSS, unsafe_allow_html=True)

    doc_count   = st.session_state.get("doc_count", 0)
    chunk_count = st.session_state.get("chunk_count", 0)
    topic_count = st.session_state.get("topic_count", 0)
    processed   = st.session_state.get("processed", False)
    activity_log = st.session_state.get("activity_log", [])

    # ── Page header ──────────────────────────────────
    st.markdown(
        """
        <div class="ep-header">
            <h2>📝 Exam Preparation</h2>
            <p>Generate exam-ready material instantly — mock tests, revision sheets and practice questions</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Feature cards ─────────────────────────────────
    st.markdown('<div class="ep-label">Features</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="ep-features">
            <div class="ep-feature mock">
                <div class="ef-icon">📝</div>
                <h4>Mock Test</h4>
                <p>Interactive, exam-style questions generated from your material.</p>
                <ul>
                    <li>Multiple choice questions</li>
                    <li>Instant scoring</li>
                    <li>Difficulty control</li>
                </ul>
            </div>
            <div class="ep-feature revision">
                <div class="ef-icon">⚡</div>
                <h4>Revision Sheet</h4>
                <p>Condensed summary of key definitions, formulas and concepts.</p>
                <ul>
                    <li>Important definitions</li>
                    <li>Core formulas</li>
                    <li>Key exam questions</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Difficulty selector ───────────────────────────
    st.markdown('<div class="ep-label">Difficulty</div>', unsafe_allow_html=True)

    if "exam_difficulty" not in st.session_state:
        st.session_state.exam_difficulty = "Mixed"

    diff_col1, diff_col2, diff_col3, diff_col4 = st.columns(4, gap="small")
    for col, level in zip(
        [diff_col1, diff_col2, diff_col3, diff_col4],
        ["Easy", "Medium", "Hard", "Mixed"],
    ):
        with col:
            active = st.session_state.exam_difficulty == level
            if st.button(
                level,
                key=f"diff_{level}",
                use_container_width=True,
                type="primary" if active else "secondary",
            ):
                st.session_state.exam_difficulty = level
                st.rerun()

    # ── Preparation overview ──────────────────────────
    st.markdown('<div class="ep-label">Preparation Overview</div>', unsafe_allow_html=True)

    readiness_score = 0
    if processed:
        readiness_score += 40
    if "Generated Notes" in activity_log:
        readiness_score += 20
    if "Generated Flashcards" in activity_log:
        readiness_score += 20
    if "Generated Question Bank" in activity_log:
        readiness_score += 20

    st.markdown(
        f"""
        <div class="prep-stats">
            <div class="prep-stat">
                <div class="ps-val">{doc_count}</div>
                <div class="ps-lbl">Documents</div>
            </div>
            <div class="prep-stat">
                <div class="ps-val">{chunk_count}</div>
                <div class="ps-lbl">Knowledge Chunks</div>
            </div>
            <div class="prep-stat">
                <div class="ps-val">{topic_count}</div>
                <div class="ps-lbl">Topics Available</div>
            </div>
            <div class="prep-stat">
                <div class="ps-val" style="color:#4ade80">{readiness_score}%</div>
                <div class="ps-lbl">Readiness Score</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Study readiness + AI recommendation ──────────
    st.markdown('<div class="ep-label">Study Readiness</div>', unsafe_allow_html=True)

    has_notes     = "Generated Notes"         in activity_log
    has_flash     = "Generated Flashcards"    in activity_log
    has_qbank     = "Generated Question Bank" in activity_log
    has_mock      = "Generated Mock Test"     in activity_log

    readiness_html = (
        _readiness_row("Mock Test",     has_mock)  +
        _readiness_row("Revision Sheet", processed) +
        _readiness_row("Question Bank",  has_qbank) +
        _readiness_row("Flashcards",     has_flash)
    )

    # AI recommendation text
    if not processed:
        rec_text = "Upload and process a PDF to unlock exam preparation tools."
        rec_seq  = ""
    elif not has_notes:
        rec_text = "Start with Study Tools to build your notes before attempting a mock test."
        rec_seq  = "<ol><li>Generate Notes</li><li>Create Flashcards</li><li>Run Mock Test</li></ol>"
    elif not has_flash:
        rec_text = "Notes are ready. Generate flashcards to strengthen recall before testing."
        rec_seq  = "<ol><li>Create Flashcards</li><li>Revision Sheet</li><li>Mock Test</li></ol>"
    else:
        rec_text = "You have sufficient material. Recommended exam preparation sequence:"
        rec_seq  = "<ol><li>Revision Sheet</li><li>Flashcards review</li><li>Mock Test</li></ol>"

    rg_col, rec_col = st.columns([1, 1], gap="medium")

    with rg_col:
        st.markdown(
            f"""
            <div class="readiness-panel">
                <div class="rp-title">Readiness Checklist</div>
                {readiness_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with rec_col:
        st.markdown(
            f"""
            <div class="ep-rec">
                <div class="rec-tag">✦ AI Recommendation</div>
                <div class="rec-body">{rec_text}{rec_seq}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Generation controls ───────────────────────────
    st.markdown('<div class="ep-label">Generate Material</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="ep-action"><div class="ea-title">Enter a topic to generate exam material</div></div>',
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Topic",
        key="exam_topic",
        placeholder="e.g. Thermodynamics, World War II, Machine Learning…",
        label_visibility="collapsed",
    )

    gen_col1, gen_col2 = st.columns(2, gap="small")
    with gen_col1:
        mock_test_btn = st.button("📝 Generate Mock Test",    use_container_width=True, type="primary")
    with gen_col2:
        revision_btn  = st.button("⚡ Generate Revision Sheet", use_container_width=True)

    # ── Generation logic ──────────────────────────────
    if mock_test_btn or revision_btn:
        if not topic:
            st.warning("Please enter a topic first.")
            return

        docs = retrieve(topic, vector_db)
        if not docs:
            st.warning("No relevant content found for that topic.")
            return

        context = "\n".join(doc.page_content for doc in docs)

        if revision_btn:
            st.markdown("---")
            st.markdown("#### ⚡ Revision Sheet")
            sheet = generate_revision_sheet(context)
            render_revision_sheet(safe_json(sheet))
            if "Generated Revision Sheet" not in activity_log:
                st.session_state.activity_log.append("Generated Revision Sheet")

        if mock_test_btn:
            difficulty = st.session_state.get("exam_difficulty", "Mixed")
            mock_test = generate_mock_test(
                context,
                num_2_mark=5,
                num_5_mark=0,
                num_10_mark=0,
                difficulty=difficulty,
            )

            if not mock_test.get("success", True) and "mcqs" not in mock_test:
                st.error(mock_test.get("error", "Mock Test Generation Failed"))
                if "raw_response" in mock_test:
                    st.code(mock_test["raw_response"])
                return

            initialize_test(mock_test)
            if "Generated Mock Test" not in activity_log:
                st.session_state.activity_log.append("Generated Mock Test")

    # ── Mock test UI ──────────────────────────────────
    if "mock_test" in st.session_state:
        st.markdown("---")
        st.markdown("#### 📝 Interactive Mock Test")
        render_mock_test()
        reset_test()