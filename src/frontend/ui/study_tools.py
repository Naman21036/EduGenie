import streamlit as st
from frontend.ui.tool_router import render_selected_tool


STUDY_TOOLS_CSS = """
<style>
/* ── Page header ── */
.st-header { margin-bottom: 22px; }
.st-header h2 {
    font-size: 1.35rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 4px;
    letter-spacing: -0.02em;
}
.st-header p { font-size: 13px; color: #475569; margin: 0; }

/* ── Section label ── */
.st-label {
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
.st-label::after { content:""; flex:1; height:1px; background:rgba(255,255,255,0.05); }

/* ── Tool card ── */
.tool-card {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 22px 20px 18px;
    position: relative;
    overflow: hidden;
    height: 100%;
    transition: border-color 0.18s ease, transform 0.18s ease;
}
.tool-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 14px 14px 0 0;
    background: transparent;
    transition: background 0.18s ease;
}
.tool-card:hover { border-color: rgba(59,130,246,0.35); transform: translateY(-2px); }
.tool-card:hover::before { background: linear-gradient(90deg, #3b82f6, #06b6d4); }
.tool-card.active { border-color: rgba(59,130,246,0.5); background: #111827; }
.tool-card.active::before { background: linear-gradient(90deg, #3b82f6, #06b6d4); }
.tool-card .tc-icon { font-size: 24px; margin-bottom: 12px; display: block; }
.tool-card h4 { font-size: 14px; font-weight: 700; color: #e2e8f0; margin: 0 0 5px; }
.tool-card p { font-size: 12px; color: #475569; margin: 0 0 14px; line-height: 1.5; }
.tool-card ul { padding-left: 15px; margin: 0; }
.tool-card li { font-size: 11.5px; color: #64748b; margin-bottom: 3px; }
.tool-card .tc-cta {
    font-size: 12px;
    font-weight: 600;
    color: #3b82f6;
    margin-top: 14px;
    display: flex;
    align-items: center;
    gap: 4px;
}
</style>
"""

_TOOLS = [
    {
        "key": "notes",
        "icon": "📄",
        "title": "Notes Generator",
        "desc": "Structured, topic-focused study notes from your documents.",
        "features": ["Hierarchical summaries", "Key definitions", "Concept breakdown"],
    },
    {
        "key": "mcqs",
        "icon": "🎯",
        "title": "MCQ Generator",
        "desc": "Exam-style multiple choice questions with instant answer reveal.",
        "features": ["Difficulty control", "Instant scoring", "Detailed answers"],
    },
    {
        "key": "flashcards",
        "icon": "🃏",
        "title": "Flashcards",
        "desc": "Interactive flip cards for active recall and spaced repetition.",
        "features": ["Flip animation", "Front & back format", "Batch generation"],
    },
    {
        "key": "question_bank",
        "icon": "📚",
        "title": "Question Bank",
        "desc": "Comprehensive question set across 2, 5 and 10 mark levels.",
        "features": ["2 / 5 / 10 mark tiers", "Exam-ready format", "Full coverage"],
    },
]


def render_study_tools(vector_db):

    st.markdown(STUDY_TOOLS_CSS, unsafe_allow_html=True)

    # ── Page header ──────────────────────────────────
    st.markdown(
        '<div class="st-header">'
        '<h2>📖 Study Tools</h2>'
        '<p>Generate notes, flashcards, MCQs and question banks directly from your documents</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Tool selection cards ──────────────────────────
    st.markdown('<div class="st-label">Select a Tool</div>', unsafe_allow_html=True)

    selected_tool = st.session_state.get("selected_tool", None)

    cols = st.columns(4, gap="small")

    for col, tool in zip(cols, _TOOLS):
        with col:
            active_cls = "active" if selected_tool == tool["key"] else ""
            features_html = "".join(f"<li>{f}</li>" for f in tool["features"])
            st.markdown(
                f'<div class="tool-card {active_cls}">'
                f'<span class="tc-icon">{tool["icon"]}</span>'
                f'<h4>{tool["title"]}</h4>'
                f'<p>{tool["desc"]}</p>'
                f'<ul>{features_html}</ul>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button(
                f"Open {tool['title']}",
                key=f"tool_btn_{tool['key']}",
                use_container_width=True,
            ):
                st.session_state.selected_tool = tool["key"]
                st.rerun()

    # ── Active tool renderer ──────────────────────────
    if selected_tool:
        st.markdown('<div class="st-label">Generate</div>', unsafe_allow_html=True)
        render_selected_tool(vector_db)
    else:
        st.markdown(
            '<div style="padding:32px 0; text-align:center;">'
            '<p style="font-size:13px; color:#334155;">Select a tool above to get started.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
