import json
import streamlit as st
from ingestion.retriever import retrieve
from study_tools.mock_test_generator import generate_mock_test
from study_tools.revision_sheet_generator import generate_revision_sheet
from frontend.exam_prep.mock_test_engine import initialize_test, render_mock_test, reset_test


# ── Design Tokens ─────────────────────────────────────────────────────────────
# Centralised token map — change here, propagates everywhere.
_BLUE_500  = "#3b82f6"
_BLUE_400  = "#60a5fa"
_BLUE_300  = "#93c5fd"
_BLUE_GLOW = "rgba(59,130,246,0.12)"
_BLUE_RING = "rgba(59,130,246,0.22)"
_GREEN_500 = "#22c55e"
_GREEN_400 = "#4ade80"

# ── CSS ───────────────────────────────────────────────────────────────────────
EXAM_CSS = f"""
<style>
/* ═══════════════════════════════════════════════
   RESET & BASE
═══════════════════════════════════════════════ */
.ep-wrap * {{ box-sizing: border-box; }}

/* ═══════════════════════════════════════════════
   PAGE HEADER
═══════════════════════════════════════════════ */
.ep-header {{ margin-bottom: 24px; }}
.ep-header h2 {{
    font-size: 1.4rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 5px;
    letter-spacing: -0.025em;
    line-height: 1.2;
}}
.ep-header p {{
    font-size: 13px;
    color: #64748b;
    margin: 0;
    line-height: 1.5;
}}

/* ═══════════════════════════════════════════════
   SECTION LABEL  (divider + uppercase tag)
═══════════════════════════════════════════════ */
.ep-label {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin: 28px 0 14px;
}}
.ep-label::after {{
    content: "";
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.05);
}}

/* ═══════════════════════════════════════════════
   FEATURE CARDS
═══════════════════════════════════════════════ */
.ep-features {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}}
.ep-feature {{
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}}
.ep-feature:hover {{ border-color: rgba(255,255,255,0.13); }}
.ep-feature::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 14px 14px 0 0;
}}
.ep-feature.mock::before     {{ background: {_BLUE_500}; }}
.ep-feature.revision::before {{ background: {_GREEN_500}; }}
.ep-feature .ef-icon  {{ font-size: 22px; margin-bottom: 10px; display: block; }}
.ep-feature h4 {{
    font-size: 14px;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 6px;
}}
.ep-feature p  {{
    font-size: 12.5px;
    color: #64748b;
    margin: 0 0 10px;
    line-height: 1.55;
}}
.ep-feature ul {{ padding-left: 16px; margin: 0; }}
.ep-feature li {{ font-size: 12px; color: #475569; margin-bottom: 4px; line-height: 1.4; }}

/* ═══════════════════════════════════════════════
   PREP STATS GRID
═══════════════════════════════════════════════ */
.prep-stats {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}}
.prep-stat {{
    background: #0c1120;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 16px 18px;
}}
.prep-stat .ps-val {{
    font-size: 24px;
    font-weight: 800;
    color: {_BLUE_300};
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 4px;
}}
.prep-stat .ps-val.green {{ color: {_GREEN_400}; }}
.prep-stat .ps-lbl {{
    font-size: 11px;
    color: #475569;
    line-height: 1.3;
}}

/* ═══════════════════════════════════════════════
   READINESS + RECOMMENDATION  (2-col grid)
═══════════════════════════════════════════════ */
.readiness-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}}
.readiness-panel {{
    background: #0c1120;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 18px 20px;
}}
.rp-title {{
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin: 0 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}}
.readiness-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 9px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 13px;
}}
.readiness-row:last-child {{ border-bottom: none; }}
.rr-label {{ color: #94a3b8; }}
.rr-badge {{
    font-size: 11px;
    font-weight: 600;
    padding: 2px 9px;
    border-radius: 20px;
    white-space: nowrap;
}}
.rr-badge.ready   {{ background: rgba(34,197,94,0.12); color: {_GREEN_400}; }}
.rr-badge.pending {{ background: {_BLUE_GLOW};          color: {_BLUE_400}; }}

/* ═══════════════════════════════════════════════
   AI RECOMMENDATION PANEL
═══════════════════════════════════════════════ */
.ep-rec {{
    background: linear-gradient(145deg, #0f172a, #0c1526);
    border: 1px solid {_BLUE_RING};
    border-radius: 14px;
    padding: 18px 20px;
    height: 100%;
}}
.rec-tag {{
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: {_BLUE_400};
    margin: 0 0 10px;
}}
.rec-body {{
    font-size: 13px;
    color: #cbd5e1;
    line-height: 1.65;
}}
.rec-body ol {{
    padding-left: 18px;
    margin: 8px 0 0;
}}
.rec-body li {{
    font-size: 13px;
    color: #94a3b8;
    margin-bottom: 5px;
    line-height: 1.5;
}}

/* ═══════════════════════════════════════════════
   GENERATE MATERIAL SECTION
═══════════════════════════════════════════════ */
.ep-action {{
    background: #0c1120;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 14px;
}}
.ea-title {{
    font-size: 13px;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 6px;
}}
.ea-subtitle {{
    font-size: 12px;
    color: #475569;
    margin: 0;
}}

/* ═══════════════════════════════════════════════
   RESPONSIVE  –  collapse to single column below ~720 px
═══════════════════════════════════════════════ */
@media (max-width: 720px) {{
    .ep-features,
    .prep-stats,
    .readiness-grid {{ grid-template-columns: 1fr; }}
    .prep-stats      {{ grid-template-columns: 1fr 1fr; }}
}}
/* ─────────────────────────────────────────────
   Exam Prep Button Override
───────────────────────────────────────────── */

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


# ── Utility helpers ────────────────────────────────────────────────────────────

def _safe_json(data) -> dict:
    """Safely coerce *data* to a dict (best-effort JSON parse for strings)."""
    if isinstance(data, dict):
        return data
    if isinstance(data, str):
        try:
            return json.loads(data)
        except Exception:
            return {}
    return {}


def _readiness_row(label: str, ready: bool) -> str:
    """Return a single readiness-checklist row as an HTML string."""
    cls = "ready" if ready else "pending"
    txt = "Ready"  if ready else "Pending"
    return (
        f'<div class="readiness-row">'
        f'  <span class="rr-label">{label}</span>'
        f'  <span class="rr-badge {cls}">{txt}</span>'
        f'</div>'
    )


def _stat_card(value, label: str, green: bool = False) -> str:
    """Return a single prep-stat card as an HTML string."""
    cls = ' green' if green else ''
    return (
        f'<div class="prep-stat">'
        f'  <div class="ps-val{cls}">{value}</div>'
        f'  <div class="ps-lbl">{label}</div>'
        f'</div>'
    )


def _feature_card(variant: str, icon: str, title: str, desc: str, bullets: list[str]) -> str:
    """Return a feature card as an HTML string."""
    li_html = "".join(f"<li>{b}</li>" for b in bullets)
    return (
        f'<div class="ep-feature {variant}">'
        f'  <span class="ef-icon">{icon}</span>'
        f'  <h4>{title}</h4>'
        f'  <p>{desc}</p>'
        f'  <ul>{li_html}</ul>'
        f'</div>'
    )


# ── Revision sheet renderer ────────────────────────────────────────────────────

def render_revision_sheet(sheet: dict) -> None:
    """Render a parsed revision-sheet dict using native Streamlit widgets."""
    if not sheet.get("success", True):
        st.error(sheet.get("error", "JSON Parsing Failed"))
        st.code(sheet.get("raw_response", ""))
        return

    definitions = sheet.get("important_definitions", [])
    if definitions:
        st.markdown("#### 📖 Definitions")
        for d in definitions:
            st.markdown(f"**{d.get('term', '')}**")
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


# ── Main page renderer ─────────────────────────────────────────────────────────

def render_exam_prep(vector_db) -> None:
    """Render the full Exam Preparation page."""

    # Inject scoped CSS once
    st.markdown(EXAM_CSS, unsafe_allow_html=True)

    # ── Pull session state ────────────────────────────────────────────────────
    doc_count    = st.session_state.get("doc_count", 0)
    chunk_count  = st.session_state.get("chunk_count", 0)
    topic_count  = st.session_state.get("topic_count", 0)
    processed    = st.session_state.get("processed", False)
    activity_log = st.session_state.get("activity_log", [])

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown(
        """
        <div class="ep-header">
            <h2>📝 Exam Preparation</h2>
            <p>Generate exam-ready material instantly — mock tests, revision sheets and practice questions</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Feature cards ─────────────────────────────────────────────────────────
    st.markdown('<div class="ep-label">Features</div>', unsafe_allow_html=True)

    mock_card = _feature_card(
        "mock", "📝", "Mock Test",
        "Interactive, exam-style questions generated from your material.",
        ["Multiple choice questions", "Instant scoring", "Difficulty control"],
    )
    revision_card = _feature_card(
        "revision", "⚡", "Revision Sheet",
        "Condensed summary of key definitions, formulas and concepts.",
        ["Important definitions", "Core formulas", "Key exam questions"],
    )
    st.markdown(
        f'<div class="ep-features">{mock_card}{revision_card}</div>',
        unsafe_allow_html=True,
    )

    # ── Difficulty selector ───────────────────────────────────────────────────
    st.markdown('<div class="ep-label">Difficulty</div>', unsafe_allow_html=True)

    if "exam_difficulty" not in st.session_state:
        st.session_state.exam_difficulty = "Mixed"

    difficulty_levels = ["Easy", "Medium", "Hard", "Mixed"]
    diff_cols = st.columns(4, gap="small")
    for col, level in zip(diff_cols, difficulty_levels):
        with col:
            is_active = st.session_state.exam_difficulty == level
            if st.button(
                level,
                key=f"diff_{level}",
                use_container_width=True,
            ):
                st.session_state.exam_difficulty = level
                st.rerun()

    # ── Preparation overview ──────────────────────────────────────────────────
    st.markdown('<div class="ep-label">Preparation Overview</div>', unsafe_allow_html=True)

    readiness_score = 0
    if processed:                                    readiness_score += 40
    if "Generated Notes"         in activity_log:   readiness_score += 20
    if "Generated Flashcards"    in activity_log:   readiness_score += 20
    if "Generated Question Bank" in activity_log:   readiness_score += 20

    stats_html = "".join([
        _stat_card(doc_count,   "Documents"),
        _stat_card(chunk_count, "Knowledge Chunks"),
        _stat_card(topic_count, "Topics Available"),
        _stat_card(f"{readiness_score}%", "Readiness Score", green=True),
    ])
    st.markdown(
        f'<div class="prep-stats">{stats_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Study readiness + AI recommendation ──────────────────────────────────
    st.markdown('<div class="ep-label">Study Readiness</div>', unsafe_allow_html=True)

    has_notes = "Generated Notes"         in activity_log
    has_flash = "Generated Flashcards"    in activity_log
    has_qbank = "Generated Question Bank" in activity_log
    has_mock  = "Generated Mock Test"     in activity_log

    checklist_rows = "".join([
        _readiness_row("Mock Test",      has_mock),
        _readiness_row("Revision Sheet", processed),
        _readiness_row("Question Bank",  has_qbank),
        _readiness_row("Flashcards",     has_flash),
    ])

    # Derive contextual AI recommendation
    if not processed:
        rec_text = "Upload and process a PDF to unlock exam preparation tools."
        rec_steps: list[str] = []
    elif not has_notes:
        rec_text = "Start with Study Tools to build your notes before attempting a mock test."
        rec_steps = ["Generate Notes", "Create Flashcards", "Run Mock Test"]
    elif not has_flash:
        rec_text = "Notes are ready. Generate flashcards to strengthen recall before testing."
        rec_steps = ["Create Flashcards", "Revision Sheet", "Mock Test"]
    else:
        rec_text = "You have sufficient material. Recommended exam preparation sequence:"
        rec_steps = ["Revision Sheet", "Flashcards review", "Mock Test"]

    if rec_steps:
        rec_ol = "<ol>" + "".join(f"<li>{s}</li>" for s in rec_steps) + "</ol>"
    else:
        rec_ol = ""

    left_col, right_col = st.columns(2, gap="medium")

    with left_col:
        st.markdown(
            f"""
            <div class="readiness-panel">
                <div class="rp-title">Readiness Checklist</div>
                {checklist_rows}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        st.markdown(
            f"""
            <div class="ep-rec">
                <div class="rec-tag">✦ AI Recommendation</div>
                <div class="rec-body">{rec_text}{rec_ol}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Material generation ───────────────────────────────────────────────────
    st.markdown('<div class="ep-label">Generate Material</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="ep-action">
            <div class="ea-title">Enter a topic to generate exam material</div>
            <p class="ea-subtitle">Type any subject, chapter, or concept covered in your uploaded documents</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Topic",
        key="exam_topic",
        placeholder="e.g. Thermodynamics, World War II, Machine Learning…",
        label_visibility="collapsed",
    )

    btn_col1, btn_col2 = st.columns(2, gap="small")
    with btn_col1:
        mock_test_btn = st.button("📝 Generate Mock Test",     use_container_width=True)
    with btn_col2:
        revision_btn  = st.button("⚡ Generate Revision Sheet", use_container_width=True)

    # ── Generation logic ──────────────────────────────────────────────────────
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
            render_revision_sheet(_safe_json(sheet))
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

    # ── Interactive mock test UI ───────────────────────────────────────────────
    if "mock_test" in st.session_state:
        st.markdown("---")
        st.markdown("#### 📝 Interactive Mock Test")
        render_mock_test()
        reset_test()
