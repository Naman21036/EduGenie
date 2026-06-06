import json
import streamlit as st
import streamlit.components.v1 as components
from ingestion.retriever import retrieve
from study_tools.mock_test_generator import generate_mock_test
from study_tools.revision_sheet_generator import generate_revision_sheet
from frontend.exam_prep.mock_test_engine import initialize_test, render_mock_test, reset_test


# ── CSS ──────────────────────────────────────────────────────────────────────
# ROOT CAUSE OF OLD EMPTY GAP — same as analysis.py:
#   Multiple consecutive st.markdown() calls each add ~1rem container margin.
#   The old design had: features block → difficulty block → stats block →
#   readiness block → rec block → action label → action body = 7 × ~16px = ~112px
#   of dead vertical space before the actual input.
#
# FIX: One consolidated HTML block for all visual sections. Streamlit widgets
#   (buttons, text_input) are placed immediately below with no extra markup calls.

EXAM_CSS = """
<style>
.ep-root * { box-sizing:border-box; font-family:'Inter',sans-serif; }

/* header */
.ep-root .ph { margin-bottom:16px; }
.ep-root .ph h2 { font-size:1.3rem; font-weight:700; color:#F8FAFC; margin:0 0 3px; letter-spacing:-0.02em; }
.ep-root .ph p  { font-size:13px; color:#4B5A72; margin:0; }

/* section label */
.ep-root .lbl {
    font-size:10.5px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
    color:#4B5A72; margin:16px 0 10px; display:flex; align-items:center; gap:8px;
}
.ep-root .lbl::after { content:""; flex:1; height:1px; background:#273449; }

/* feature cards */
.ep-root .feat { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.ep-root .fc {
    background:#161B2E; border:1px solid #273449; border-radius:12px;
    padding:16px 18px; position:relative; overflow:hidden;
}
.ep-root .fc::before { content:""; position:absolute; top:0; left:0; right:0; height:2px; border-radius:12px 12px 0 0; }
.ep-root .fc.mock::before     { background:#3B82F6; }
.ep-root .fc.revision::before { background:#10B981; }
.ep-root .fc .fi { font-size:22px; margin-bottom:8px; }
.ep-root .fc h4  { font-size:13.5px; font-weight:700; color:#E2E8F0; margin:0 0 5px; }
.ep-root .fc p   { font-size:12px; color:#4B5A72; margin:0 0 10px; line-height:1.5; }
.ep-root .fc ul  { padding-left:15px; margin:0; }
.ep-root .fc li  { font-size:11.5px; color:#4B5A72; margin-bottom:3px; }

/* prep stats */
.ep-root .stats { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; }
.ep-root .stat  { background:#161B2E; border:1px solid #273449; border-radius:10px; padding:12px 14px; }
.ep-root .stat .sv { font-size:21px; font-weight:800; color:#60A5FA; letter-spacing:-0.02em; line-height:1; }
.ep-root .stat .sl { font-size:11px; color:#4B5A72; margin-top:3px; }
.ep-root .stat .sv.green { color:#10B981; }

/* readiness + rec side-by-side */
.ep-root .lower { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.ep-root .rp { background:#161B2E; border:1px solid #273449; border-radius:12px; padding:16px 18px; }
.ep-root .rp .rpt {
    font-size:10.5px; font-weight:700; letter-spacing:0.07em; text-transform:uppercase;
    color:#4B5A72; margin:0 0 12px; padding-bottom:9px; border-bottom:1px solid #273449;
}
.ep-root .rr { display:flex; align-items:center; justify-content:space-between; padding:7px 0; border-bottom:1px solid rgba(39,52,73,0.5); font-size:12.5px; }
.ep-root .rr:last-child { border-bottom:none; }
.ep-root .rr .rl { color:#94A3B8; }
.ep-root .rr .rb { font-size:10.5px; font-weight:600; padding:2px 8px; border-radius:20px; }
.ep-root .rb.ready   { background:rgba(16,185,129,0.1); color:#10B981; }
.ep-root .rb.pending { background:rgba(59,130,246,0.1); color:#60A5FA; }
/* AI rec */
.ep-root .rec { background:#161B2E; border:1px solid rgba(59,130,246,0.2); border-radius:12px; padding:16px 18px; }
.ep-root .rec .rt { font-size:10.5px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#3B82F6; margin:0 0 7px; }
.ep-root .rec .rb2 { font-size:12.5px; color:#CBD5E1; line-height:1.65; }
.ep-root .rec ol  { padding-left:16px; margin:7px 0 0; }
.ep-root .rec li  { font-size:12.5px; color:#94A3B8; margin-bottom:4px; }

/* action panel */
.ep-root .act { background:#161B2E; border:1px solid rgba(59,130,246,0.2); border-radius:12px; padding:14px 18px; }
.ep-root .act .at { font-size:12.5px; font-weight:600; color:#E2E8F0; margin:0 0 3px; }
.ep-root .act .ad { font-size:11.5px; color:#4B5A72; margin:0; }
</style>
"""


def safe_json(data):
    if isinstance(data, dict): return data
    if isinstance(data, str):
        try: return json.loads(data)
        except: return {}
    return {}


def render_revision_sheet(sheet):
    if not sheet.get("success", True):
        st.error(sheet.get("error","JSON Parsing Failed"))
        st.code(sheet.get("raw_response","")); return

    definitions = sheet.get("important_definitions",[])
    if definitions:
        st.markdown("#### 📖 Definitions")
        for d in definitions:
            st.markdown(f"**{d.get('term','')}**")
            st.caption(d.get("definition",""))

    formulas = sheet.get("important_formulas",[])
    if formulas:
        st.markdown("#### 🧮 Formulas")
        for f in formulas:
            st.code(f.get("formula",""))
            st.caption(f.get("explanation",""))

    concepts = sheet.get("important_concepts",[])
    if concepts:
        st.markdown("#### 💡 Key Concepts")
        for c in concepts: st.markdown(f"• {c}")

    questions = sheet.get("most_important_questions",[])
    if questions:
        st.markdown("#### 🔥 Most Important Questions")
        for q in questions: st.markdown(f"• {q}")


def _rr(label, ready):
    cls = "ready" if ready else "pending"
    txt = "Ready"  if ready else "Pending"
    return f'<div class="rr"><span class="rl">{label}</span><span class="rb {cls}">{txt}</span></div>'


def render_exam_prep(vector_db):

    components.html(EXAM_CSS, height=0)

    doc_count    = st.session_state.get("doc_count",   0)
    chunk_count  = st.session_state.get("chunk_count", 0)
    topic_count  = st.session_state.get("topic_count", 0)
    processed    = st.session_state.get("processed",   False)
    activity_log = st.session_state.get("activity_log", [])

    has_notes = "Generated Notes"         in activity_log
    has_flash = "Generated Flashcards"    in activity_log
    has_qbank = "Generated Question Bank" in activity_log
    has_mock  = "Generated Mock Test"     in activity_log

    readiness_score = (40 if processed else 0) + (20 if has_notes else 0) + \
                      (20 if has_flash else 0)  + (20 if has_qbank else 0)

    # Readiness rows
    rows_html = _rr("Mock Test", has_mock) + _rr("Revision Sheet", processed) + \
                _rr("Question Bank", has_qbank) + _rr("Flashcards", has_flash)

    # AI recommendation
    if not processed:
        rec_t = "Upload and process a PDF to unlock exam preparation tools."
        rec_s = ""
    elif not has_notes:
        rec_t = "Start with Study Tools to build notes before attempting a mock test."
        rec_s = "<ol><li>Generate Notes</li><li>Create Flashcards</li><li>Run Mock Test</li></ol>"
    elif not has_flash:
        rec_t = "Notes ready. Generate flashcards to strengthen recall before testing."
        rec_s = "<ol><li>Create Flashcards</li><li>Revision Sheet</li><li>Mock Test</li></ol>"
    else:
        rec_t = "Sufficient material available. Recommended sequence:"
        rec_s = "<ol><li>Revision Sheet</li><li>Flashcard review</li><li>Mock Test</li></ol>"

    # ── ONE consolidated HTML block ───────────────────
    st.markdown(f"""
<div class="ep-root">
  <div class="ph">
    <h2>📝 Exam Preparation</h2>
    <p>Generate exam-ready material instantly — mock tests, revision sheets and practice questions</p>
  </div>

  <div class="lbl">Features</div>
  <div class="feat">
    <div class="fc mock">
      <div class="fi">📝</div><h4>Mock Test</h4>
      <p>Interactive exam-style questions from your material.</p>
      <ul><li>Multiple choice questions</li><li>Instant scoring</li><li>Difficulty control</li></ul>
    </div>
    <div class="fc revision">
      <div class="fi">⚡</div><h4>Revision Sheet</h4>
      <p>Condensed summary of definitions, formulas and concepts.</p>
      <ul><li>Important definitions</li><li>Core formulas</li><li>Key exam questions</li></ul>
    </div>
  </div>

  <div class="lbl">Preparation Overview</div>
  <div class="stats">
    <div class="stat"><div class="sv">{doc_count}</div><div class="sl">Documents</div></div>
    <div class="stat"><div class="sv">{chunk_count}</div><div class="sl">Knowledge Chunks</div></div>
    <div class="stat"><div class="sv">{topic_count}</div><div class="sl">Topics Available</div></div>
    <div class="stat"><div class="sv green">{readiness_score}%</div><div class="sl">Readiness Score</div></div>
  </div>

  <div class="lbl">Study Readiness</div>
  <div class="lower">
    <div class="rp"><div class="rpt">Readiness Checklist</div>{rows_html}</div>
    <div class="rec"><div class="rt">✦ AI Recommendation</div><div class="rb2">{rec_t}{rec_s}</div></div>
  </div>

  <div class="lbl">Generate Material</div>
  <div class="act">
    <div class="at">Enter a topic to generate exam material</div>
    <div class="ad">Difficulty applies to Mock Test generation</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Difficulty selector (Streamlit buttons) ───────
    if "exam_difficulty" not in st.session_state:
        st.session_state.exam_difficulty = "Mixed"

    dc1, dc2, dc3, dc4 = st.columns(4, gap="small")
    for col, level in zip([dc1,dc2,dc3,dc4], ["Easy","Medium","Hard","Mixed"]):
        with col:
            active = st.session_state.exam_difficulty == level
            if st.button(level, key=f"diff_{level}", use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.exam_difficulty = level
                st.rerun()

    # ── Topic input + generate buttons ───────────────
    topic = st.text_input(
        "Topic", key="exam_topic",
        placeholder="e.g. Thermodynamics, World War II, Machine Learning…",
        label_visibility="collapsed")

    gc1, gc2 = st.columns(2, gap="small")
    with gc1: mock_test_btn = st.button("📝 Generate Mock Test",     use_container_width=True, type="primary")
    with gc2: revision_btn  = st.button("⚡ Generate Revision Sheet", use_container_width=True)

    # ── Generation logic ──────────────────────────────
    if mock_test_btn or revision_btn:
        if not topic:
            st.warning("Please enter a topic first."); return

        docs = retrieve(topic, vector_db)
        if not docs:
            st.warning("No relevant content found for that topic."); return

        context = "\n".join(doc.page_content for doc in docs)

        if revision_btn:
            st.markdown("---")
            st.markdown("#### ⚡ Revision Sheet")
            sheet = generate_revision_sheet(context)
            render_revision_sheet(safe_json(sheet))
            if "Generated Revision Sheet" not in activity_log:
                st.session_state.activity_log.append("Generated Revision Sheet")

        if mock_test_btn:
            difficulty = st.session_state.get("exam_difficulty","Mixed")
            mock_test = generate_mock_test(context, num_2_mark=5, num_5_mark=0,
                                           num_10_mark=0, difficulty=difficulty)
            if not mock_test.get("success",True) and "mcqs" not in mock_test:
                st.error(mock_test.get("error","Mock Test Generation Failed"))
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
