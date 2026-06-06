import streamlit as st
import streamlit.components.v1 as components
from frontend.ui.tool_router import render_selected_tool

_CSS = """
<style>
.st-root * { box-sizing: border-box; font-family: 'Inter', sans-serif; }

/* page header */
.st-root .ph { margin-bottom: 16px; }
.st-root .ph h2 { font-size: 1.25rem; font-weight: 700; color: #F8FAFC !important; margin: 0 0 2px; letter-spacing: -.02em; }
.st-root .ph p  { font-size: 13px; color: #4B5A72 !important; margin: 0; }

/* section label */
.st-root .lbl { font-size: 10.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #4B5A72; margin: 14px 0 10px; display: flex; align-items: center; gap: 8px; }
.st-root .lbl::after { content: ""; flex: 1; height: 1px; background: #273449; }

/* tool cards grid */
.st-root .tool-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.st-root .tc {
    background: #161B2E; border: 1px solid #273449; border-radius: 12px;
    padding: 18px 16px; position: relative; overflow: hidden; cursor: pointer;
    transition: border-color .15s, background .15s, transform .15s;
}
.st-root .tc::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px; border-radius: 12px 12px 0 0; }
.st-root .tc.t1::before { background: #3B82F6; }
.st-root .tc.t2::before { background: #F59E0B; }
.st-root .tc.t3::before { background: #10B981; }
.st-root .tc.t4::before { background: #8B5CF6; }
.st-root .tc:hover { border-color: rgba(59,130,246,.4); background: #1E2640; transform: translateY(-2px); }
.st-root .tc .ti { font-size: 22px; margin-bottom: 10px; display: block; }
.st-root .tc h4  { font-size: 13px; font-weight: 700; color: #E2E8F0 !important; margin: 0 0 4px; }
.st-root .tc p   { font-size: 11.5px; color: #4B5A72 !important; margin: 0 0 10px; line-height: 1.5; }
.st-root .tc ul  { padding-left: 13px; margin: 0; }
.st-root .tc li  { font-size: 11px; color: #4B5A72 !important; margin-bottom: 2px; }
.st-root .tc .cta { font-size: 11.5px; font-weight: 600; color: #60A5FA !important; margin-top: 12px; display: block; }

/* active tool indicator */
.st-root .active-tool {
    background: #161B2E; border: 1px solid rgba(59,130,246,.25);
    border-radius: 12px; padding: 13px 17px;
    display: flex; align-items: center; gap: 10px;
}
.st-root .active-tool .at-dot { width: 8px; height: 8px; border-radius: 50%; background: #3B82F6; flex-shrink: 0; }
.st-root .active-tool .at-txt { font-size: 12.5px; color: #94A3B8 !important; }
.st-root .active-tool .at-name { font-weight: 600; color: #E2E8F0 !important; }
</style>
"""

_TOOLS = [
    ("t1", "📄", "Notes Generator",    "Structured study notes from your documents.",        ["Key concepts", "Summaries", "Definitions"], "notes"),
    ("t2", "🎯", "MCQ Generator",      "Exam-level multiple choice questions.",               ["Auto-graded", "Difficulty levels", "Instant feedback"], "mcqs"),
    ("t3", "🃏", "Flashcards",         "Active recall cards for spaced repetition.",          ["Front & back format", "Key terms", "Quick review"], "flashcards"),
    ("t4", "📚", "Question Bank",      "Comprehensive practice question sets.",               ["2, 5 & 10 mark", "Topic sorted", "Export ready"], "question_bank"),
]

_TOOL_LABELS = {
    "notes":         "Notes Generator",
    "mcqs":          "MCQ Generator",
    "flashcards":    "Flashcards",
    "question_bank": "Question Bank",
}


def render_study_tools(vector_db):

    components.html(_CSS, height=0)

    active = st.session_state.get("selected_tool", "notes")

    # Build card HTML
    cards_html = ""
    for cls, icon, title, desc, features, key in _TOOLS:
        li_items = "".join(f"<li>{f}</li>" for f in features)
        cards_html += f"""
        <div class="tc {cls}">
            <span class="ti">{icon}</span>
            <h4>{title}</h4>
            <p>{desc}</p>
            <ul>{li_items}</ul>
            <span class="cta">Select below →</span>
        </div>"""

    active_label = _TOOL_LABELS.get(active, "Notes Generator")

    st.markdown(f"""
<div class="st-root">
  <div class="ph">
    <h2>📖 Study Tools</h2>
    <p>Generate notes, flashcards, MCQs and question banks from your documents</p>
  </div>

  <div class="lbl">Available Tools</div>
  <div class="tool-grid">{cards_html}</div>

  <div class="lbl">Active Tool</div>
  <div class="active-tool">
    <div class="at-dot"></div>
    <div class="at-txt">Currently selected: <span class="at-name">{active_label}</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Tool selector buttons
    c1, c2, c3, c4 = st.columns(4, gap="small")
    col_map = {"notes": c1, "mcqs": c2, "flashcards": c3, "question_bank": c4}
    labels  = {"notes": "📄 Notes", "mcqs": "🎯 MCQs", "flashcards": "🃏 Flashcards", "question_bank": "📚 Question Bank"}

    for key, col in col_map.items():
        with col:
            is_active = active == key
            if st.button(labels[key], key=f"tool_{key}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.selected_tool = key
                st.rerun()

    st.markdown("---")
    render_selected_tool(vector_db)
