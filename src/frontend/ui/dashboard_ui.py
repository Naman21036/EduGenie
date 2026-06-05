import streamlit as st
from datetime import datetime


# ── Shared dark-theme CSS injected once ─────────────────────────────────────

DASHBOARD_CSS = """
<style>
/* ── Base resets for dashboard ── */
.dash-root * { box-sizing: border-box; font-family: 'Inter', sans-serif; }

/* ── Hero ─────────────────────────────────────────── */
.dash-hero {
    background: linear-gradient(135deg, #0c1120 0%, #111827 60%, #0f172a 100%);
    border: 1px solid rgba(99,102,241,0.20);
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.dash-hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.dash-hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 11.5px;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #818cf8;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.22);
    border-radius: 20px;
    padding: 4px 12px;
    margin-bottom: 16px;
}
.dash-hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    color: #f1f5f9;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin: 0 0 12px;
}
.dash-hero h1 span { color: #818cf8; }
.dash-hero-sub {
    font-size: 15px;
    color: #64748b;
    line-height: 1.65;
    max-width: 560px;
    margin-bottom: 24px;
}
.dash-hero-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}
.dash-hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 12.5px;
    color: #94a3b8;
}
.dash-hero-pill .pip {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #6366f1;
    flex-shrink: 0;
}
.dash-hero-pill .pip.green { background: #34d399; }

/* ── Section label ────────────────────────────────── */
.dash-section-label {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin: 28px 0 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.dash-section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.05);
}

/* ── Workspace nav cards ──────────────────────────── */
.nav-card {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 28px 24px;
    cursor: pointer;
    transition: border-color 0.18s ease, background 0.18s ease, transform 0.18s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.nav-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 16px 16px 0 0;
    background: transparent;
    transition: background 0.18s ease;
}
.nav-card:hover { border-color: rgba(99,102,241,0.35); transform: translateY(-2px); background: #111827; }
.nav-card:hover::before { background: linear-gradient(90deg, #6366f1, #8b5cf6); }
.nav-card-icon {
    font-size: 26px;
    margin-bottom: 14px;
    display: block;
}
.nav-card h3 {
    font-size: 15px;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 6px;
    letter-spacing: -0.01em;
}
.nav-card p {
    font-size: 12.5px;
    color: #64748b;
    line-height: 1.5;
    margin: 0 0 18px;
}
.nav-card-cta {
    font-size: 12px;
    font-weight: 600;
    color: #6366f1;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* ── Metrics ──────────────────────────────────────── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 6px;
}
.metric-box {
    background: #0c1120;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 18px 20px;
}
.metric-box .m-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 6px;
}
.metric-box .m-val {
    font-size: 28px;
    font-weight: 800;
    color: #a5b4fc;
    letter-spacing: -0.03em;
    line-height: 1;
}
.metric-box .m-sub {
    font-size: 11px;
    color: #334155;
    margin-top: 4px;
}
.metric-box.status .m-val { font-size: 16px; padding-top: 4px; }
.metric-box.status .m-val.ready { color: #34d399; }
.metric-box.status .m-val.waiting { color: #f87171; }

/* ── Pipeline ─────────────────────────────────────── */
.pipeline {
    background: #0c1120;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 24px 28px;
}
.pipeline-steps {
    display: flex;
    align-items: center;
    gap: 0;
    flex-wrap: wrap;
}
.pipeline-step {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: 1;
    min-width: 160px;
}
.pipeline-step .ps-dot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    flex-shrink: 0;
}
.pipeline-step .ps-dot.done {
    background: rgba(52,211,153,0.12);
    color: #34d399;
    border: 1.5px solid rgba(52,211,153,0.3);
}
.pipeline-step .ps-dot.pending {
    background: rgba(255,255,255,0.04);
    color: #475569;
    border: 1.5px solid rgba(255,255,255,0.08);
}
.pipeline-step .ps-text { font-size: 12.5px; color: #94a3b8; }
.pipeline-step .ps-text.done { color: #e2e8f0; }
.pipeline-connector {
    width: 32px;
    height: 1px;
    background: rgba(255,255,255,0.08);
    flex-shrink: 0;
    margin: 0 4px;
}
.pipeline-connector.done { background: rgba(52,211,153,0.3); }

/* ── Activity ─────────────────────────────────────── */
.activity-list {
    background: #0c1120;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    overflow: hidden;
}
.activity-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 13px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.activity-row:last-child { border-bottom: none; }
.activity-row .a-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #6366f1;
    flex-shrink: 0;
}
.activity-row .a-text {
    font-size: 13px;
    color: #94a3b8;
    flex: 1;
}
.activity-row .a-time {
    font-size: 11px;
    color: #334155;
}
.activity-empty {
    padding: 28px 20px;
    font-size: 13px;
    color: #334155;
    text-align: center;
}

/* ── AI Recommendation ────────────────────────────── */
.ai-rec {
    background: linear-gradient(135deg, #0f172a, #111827);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 22px 24px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
}
.ai-rec-icon {
    width: 38px; height: 38px;
    border-radius: 10px;
    background: rgba(99,102,241,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.ai-rec-body {}
.ai-rec-body .rec-label {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 5px;
}
.ai-rec-body .rec-text {
    font-size: 13.5px;
    color: #cbd5e1;
    line-height: 1.6;
}
</style>
"""


def _hero(processed, file_names, doc_count, chunk_count):
    file_label = (
        file_names[0] if file_names else "No document uploaded"
    )
    extra = f"  +{len(file_names)-1} more" if len(file_names) > 1 else ""
    status_pip = "green" if processed else ""
    status_txt = "Ready" if processed else "Waiting for upload"

    st.markdown(
        f"""
        <div class="dash-hero">
            <div class="dash-hero-eyebrow">
                ✦ AI Learning Platform
            </div>
            <h1>EduGenie <span>AI</span></h1>
            <p class="dash-hero-sub">
                Transform PDFs into Notes, Flashcards, Question Banks,
                Mock Tests and AI powered insights.
            </p>
            <div class="dash-hero-meta">
                <span class="dash-hero-pill">
                    <span class="pip {status_pip}"></span>
                    {status_txt}
                </span>
                <span class="dash-hero-pill">
                    📄 {file_label}{extra}
                </span>
                <span class="dash-hero-pill">
                    🗂 {doc_count} pages
                </span>
                <span class="dash-hero-pill">
                    🧩 {chunk_count} chunks
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _workspace_cards():
    cards = [
        {
            "icon": "📝",
            "title": "Study Tools",
            "desc": "Generate notes, flashcards and question banks from your documents.",
            "page": "Study Tools",
        },
        {
            "icon": "📊",
            "title": "Analysis",
            "desc": "Topic extraction, coverage mapping and importance ranking.",
            "page": "Analysis",
        },
        {
            "icon": "📋",
            "title": "Exam Prep",
            "desc": "Build revision sheets and run interactive mock tests.",
            "page": "Exam Prep",
        },
        {
            "icon": "💬",
            "title": "AI Chat",
            "desc": "Ask questions directly from your uploaded PDFs.",
            "page": "Chat",
        },
    ]

    st.markdown(
        '<div class="dash-section-label">Workspace</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(4, gap="small")
    for col, card in zip(cols, cards):
        with col:
            # Render the visual card via HTML
            st.markdown(
                f"""
                <div class="nav-card">
                    <span class="nav-card-icon">{card['icon']}</span>
                    <h3>{card['title']}</h3>
                    <p>{card['desc']}</p>
                    <div class="nav-card-cta">Open → </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Streamlit button that actually routes — hidden behind the card visually
            # We show it with minimal height so it appears as part of the card footer
            if st.button(
                f"Open {card['title']}",
                key=f"nav_card_{card['page']}",
                use_container_width=True,
            ):
                st.session_state.nav_target = card["page"]
                st.rerun()


def _metrics(doc_count, chunk_count, topic_count, processed):
    status_cls = "ready" if processed else "waiting"
    status_txt = "Ready" if processed else "Waiting"

    st.markdown(
        '<div class="dash-section-label">At a Glance</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="metric-row">
            <div class="metric-box">
                <div class="m-label">Pages</div>
                <div class="m-val">{doc_count}</div>
                <div class="m-sub">documents loaded</div>
            </div>
            <div class="metric-box">
                <div class="m-label">Chunks</div>
                <div class="m-val">{chunk_count}</div>
                <div class="m-sub">text segments</div>
            </div>
            <div class="metric-box">
                <div class="m-label">Topics</div>
                <div class="m-val">{topic_count}</div>
                <div class="m-sub">extracted</div>
            </div>
            <div class="metric-box status">
                <div class="m-label">System</div>
                <div class="m-val {status_cls}">{status_txt}</div>
                <div class="m-sub">vector DB status</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _pipeline(processed):
    steps = [
        ("PDF Uploaded", processed or False),
        ("Documents Processed", processed or False),
        ("Vector DB Created", processed or False),
        ("Ready for Study", processed or False),
    ]

    st.markdown(
        '<div class="dash-section-label">Learning Pipeline</div>',
        unsafe_allow_html=True,
    )

    steps_html = ""
    for idx, (label, done) in enumerate(steps):
        dot_cls = "done" if done else "pending"
        txt_cls = "done" if done else ""
        icon = "✓" if done else str(idx + 1)
        connector = ""
        if idx < len(steps) - 1:
            conn_cls = "done" if done else ""
            connector = f'<div class="pipeline-connector {conn_cls}"></div>'
        steps_html += f"""
        <div class="pipeline-step">
            <div class="ps-dot {dot_cls}">{icon}</div>
            <div class="ps-text {txt_cls}">{label}</div>
        </div>
        {connector}
        """

    st.markdown(
        f"""
        <div class="pipeline">
            <div class="pipeline-steps">
                {steps_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _activity(activity_log):
    st.markdown(
        '<div class="dash-section-label">Recent Activity</div>',
        unsafe_allow_html=True,
    )

    if not activity_log:
        st.markdown(
            '<div class="activity-list"><div class="activity-empty">No activity yet — upload a PDF to get started.</div></div>',
            unsafe_allow_html=True,
        )
        return

    rows_html = ""
    for item in reversed(activity_log[-10:]):
        rows_html += f"""
        <div class="activity-row">
            <div class="a-dot"></div>
            <div class="a-text">{item}</div>
            <div class="a-time">just now</div>
        </div>
        """

    st.markdown(
        f'<div class="activity-list">{rows_html}</div>',
        unsafe_allow_html=True,
    )


def _ai_recommendation(processed, activity_log):
    if not processed:
        rec = (
            "Upload a PDF using the sidebar and click Process Documents "
            "to unlock notes, flashcards, mock tests and AI insights."
        )
    elif not activity_log:
        rec = (
            "Your documents are ready. Start with Study Tools to generate "
            "structured notes and flashcards for active recall."
        )
    elif "Generated Notes" in activity_log and "Generated Flashcards" not in activity_log:
        rec = (
            "Notes are ready. Generate flashcards next to reinforce key "
            "concepts through spaced repetition."
        )
    elif "Generated Flashcards" in activity_log and "Generated Mock Test" not in activity_log:
        rec = (
            "Flashcards are set. Head to Exam Prep and run a mock test "
            "to evaluate your retention before the real thing."
        )
    elif "Generated Mock Test" in activity_log:
        rec = (
            "You have completed a full study cycle. Use Analysis to identify "
            "coverage gaps and focus your revision on lower-scored topics."
        )
    else:
        rec = (
            "Your workspace is active. Explore Analysis for topic coverage "
            "or jump into AI Chat to ask specific questions."
        )

    st.markdown(
        '<div class="dash-section-label">AI Recommendation</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="ai-rec">
            <div class="ai-rec-icon">✦</div>
            <div class="ai-rec-body">
                <div class="rec-label">Suggested next step</div>
                <div class="rec-text">{rec}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Public render function ───────────────────────────────────────────────────

def render_dashboard():

    # Inject styles once
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

    # Read session state
    doc_count = st.session_state.get("doc_count", 0)
    chunk_count = st.session_state.get("chunk_count", 0)
    topic_count = st.session_state.get("topic_count", 0)
    processed = st.session_state.get("processed", False)
    file_names = st.session_state.get("file_names", [])
    activity_log = st.session_state.get("activity_log", [])

    # ── Sections ─────────────────────────────────────
    _hero(processed, file_names, doc_count, chunk_count)
    _workspace_cards()
    _metrics(doc_count, chunk_count, topic_count, processed)
    _pipeline(processed)

    # Activity + Rec side-by-side
    left, right = st.columns([3, 2], gap="medium")

    with left:
        _activity(activity_log)

    with right:
        _ai_recommendation(processed, activity_log)