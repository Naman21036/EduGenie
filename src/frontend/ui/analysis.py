import json
import streamlit as st
from ingestion.retriever import retrieve
from analysis.topic_extractor import generate_topic_extractor
from analysis.topic_coverage import generate_topic_coverage
from analysis.importance_ranker import generate_importance_ranker


# ── Design system + page CSS ─────────────────────────────────────────────────
# ROOT CAUSE OF OLD EMPTY GAP:
#   Each st.markdown() call is wrapped by Streamlit in a stMarkdownContainer
#   div that carries ~1rem margin-bottom.  When 5–6 pure-visual HTML blocks are
#   stacked (module-grid, insight-bar, workspace, action-area label, action-area
#   body), those margins compound to 80-120 px of dead space.
#
# FIX: Merge every purely-visual section into ONE st.markdown() call so only a
#   single container margin fires.  Break into separate calls ONLY where a real
#   Streamlit widget (text_input, button) must be inserted between sections.

ANALYSIS_CSS = """
<style>
.an-root * { box-sizing: border-box; font-family: 'Inter', sans-serif; }

/* page header */
.an-root .ph { margin-bottom: 16px; }
.an-root .ph h2 { font-size: 1.3rem; font-weight: 700; color: #F8FAFC; margin: 0 0 3px; letter-spacing: -0.02em; }
.an-root .ph p  { font-size: 13px; color: #4B5A72; margin: 0; }

/* section label */
.an-root .lbl {
    font-size: 10.5px; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #4B5A72;
    margin: 16px 0 10px; display: flex; align-items: center; gap: 8px;
}
.an-root .lbl::after { content:""; flex:1; height:1px; background:#273449; }

/* module cards */
.an-root .mod-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; }
.an-root .mod-card {
    background: #161B2E; border: 1px solid #273449;
    border-radius: 12px; padding: 16px 18px;
    position: relative; overflow: hidden;
}
.an-root .mod-card::before {
    content:""; position:absolute; top:0; left:0; right:0;
    height:2px; border-radius:12px 12px 0 0;
}
.an-root .mod-card.c1::before { background:#3B82F6; }
.an-root .mod-card.c2::before { background:#10B981; }
.an-root .mod-card.c3::before { background:#F59E0B; }
.an-root .mod-card .mi { font-size:20px; margin-bottom:8px; }
.an-root .mod-card h4  { font-size:13.5px; font-weight:700; color:#E2E8F0; margin:0 0 4px; }
.an-root .mod-card p   { font-size:12px; color:#4B5A72; margin:0; line-height:1.5; }

/* insight stats */
.an-root .stats { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; }
.an-root .stat  { background:#161B2E; border:1px solid #273449; border-radius:10px; padding:12px 14px; }
.an-root .stat .sv { font-size:21px; font-weight:800; color:#60A5FA; letter-spacing:-0.02em; line-height:1; }
.an-root .stat .sl { font-size:11px; color:#4B5A72; margin-top:3px; }
.an-root .stat .sv.ready   { color:#10B981; font-size:14px; padding-top:4px; }
.an-root .stat .sv.waiting { color:#EF4444; font-size:14px; padding-top:4px; }

/* workspace panels */
.an-root .ws { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }
.an-root .ws-panel { background:#161B2E; border:1px solid #273449; border-radius:12px; padding:16px 18px; }
.an-root .ws-panel .wpt {
    font-size:10.5px; font-weight:700; letter-spacing:0.07em; text-transform:uppercase;
    color:#4B5A72; margin:0 0 12px; padding-bottom:9px; border-bottom:1px solid #273449;
}
.an-root .ti { display:flex; align-items:center; gap:8px; padding:6px 0; border-bottom:1px solid rgba(39,52,73,0.6); font-size:12.5px; color:#94A3B8; }
.an-root .ti:last-child { border-bottom:none; }
.an-root .ti .tib { font-size:9.5px; font-weight:700; color:#60A5FA; background:rgba(59,130,246,0.1); border-radius:4px; padding:1px 5px; flex-shrink:0; }
.an-root .cr { margin-bottom:8px; }
.an-root .cr .crl { font-size:11.5px; color:#94A3B8; margin-bottom:4px; display:flex; justify-content:space-between; }
.an-root .cr .crt { height:5px; background:#273449; border-radius:3px; overflow:hidden; }
.an-root .cr .crf { height:100%; border-radius:3px; background:#3B82F6; }
.an-root .ri { display:flex; align-items:center; gap:8px; padding:6px 0; border-bottom:1px solid rgba(39,52,73,0.6); font-size:12.5px; color:#94A3B8; }
.an-root .ri:last-child { border-bottom:none; }
.an-root .ri .rn { font-size:10.5px; font-weight:700; color:#3B82F6; width:18px; flex-shrink:0; }
.an-root .ri .rs { margin-left:auto; font-size:10.5px; font-weight:700; color:#F59E0B; }

/* generate panel */
.an-root .gen-panel { background:#161B2E; border:1px solid rgba(59,130,246,0.2); border-radius:12px; padding:14px 18px; }
.an-root .gen-panel .gpt { font-size:12.5px; font-weight:600; color:#E2E8F0; margin:0 0 3px; }
.an-root .gen-panel .gpd { font-size:11.5px; color:#4B5A72; margin:0; }
</style>
"""

_TOPICS   = ["Introduction & Overview","Core Principles","Key Mechanisms","Applications","Advanced Concepts"]
_COVERAGE = [("Introduction",88),("Theory",74),("Practice",61),("Review",45)]
_RANKING  = [("Core Principles",94),("Key Mechanisms",87),("Applications",79),("Overview",65),("Advanced",52)]


def safe_json(data):
    if isinstance(data, dict): return data
    if isinstance(data, str):
        try: return json.loads(data)
        except: return {}
    return {}


def render_topics(result):
    topics = result.get("topics", [])
    if not topics: st.info("No topics returned."); return
    for item in topics:
        with st.expander(f"📚 {item.get('topic','Unknown')}", expanded=False):
            for sub in item.get("subtopics", []):
                st.markdown(f"• {sub}")


def render_coverage(result):
    coverage = result.get("topic_coverage", [])
    if not coverage: st.info("No coverage data returned."); return
    for item in coverage:
        pct = min(max(int(item.get("coverage_percentage",0)),0),100)
        cl, cr = st.columns([4,1])
        cl.markdown(f"**{item.get('topic','Unknown')}**")
        cr.caption(f"{pct}%")
        st.progress(pct/100)
        subs = item.get("subtopics",[])
        if subs: st.caption(", ".join(subs))


def render_importance(result):
    ranked = result.get("ranked_topics",[])
    if not ranked: st.info("No ranking data returned."); return
    medals = ["🥇","🥈","🥉"]
    for idx, topic in enumerate(ranked):
        icon  = medals[idx] if idx < 3 else "⭐"
        score = min(max(int(topic.get("importance_score",0)),0),100)
        with st.expander(f"{icon} {topic.get('topic','Unknown')} — {score}/100", expanded=False):
            st.progress(score/100)
            st.caption(topic.get("reason",""))


def render_analysis(vector_db):

    st.markdown(ANALYSIS_CSS, unsafe_allow_html=True)

    doc_count   = st.session_state.get("doc_count",   0)
    chunk_count = st.session_state.get("chunk_count", 0)
    topic_count = st.session_state.get("topic_count", 0)
    processed   = st.session_state.get("processed",   False)
    status_cls  = "ready"   if processed else "waiting"
    status_txt  = "Ready"   if processed else "Waiting"

    # Build inner HTML fragments
    topic_items = "".join(
        f'<div class="ti"><span class="tib">T{i+1}</span>{t}</div>'
        for i,t in enumerate(_TOPICS))

    cov_bars = "".join(
        f'<div class="cr"><div class="crl"><span>{l}</span><span>{p}%</span></div>'
        f'<div class="crt"><div class="crf" style="width:{p}%"></div></div></div>'
        for l,p in _COVERAGE)

    rank_items = "".join(
        f'<div class="ri"><span class="rn">#{i+1}</span><span>{n}</span><span class="rs">{s}</span></div>'
        for i,(n,s) in enumerate(_RANKING))

    # ── SINGLE consolidated HTML block ───────────────
    # All purely visual sections live here → only ONE stMarkdownContainer margin.
    st.markdown(f"""
<div class="an-root">
  <div class="ph">
    <h2>📊 Content Analysis</h2>
    <p>Extract topics, measure coverage and rank by importance</p>
  </div>

  <div class="lbl">Analysis Modules</div>
  <div class="mod-grid">
    <div class="mod-card c1"><div class="mi">🧠</div><h4>Topic Extraction</h4><p>Identify all major topics and subtopics in your material.</p></div>
    <div class="mod-card c2"><div class="mi">📈</div><h4>Topic Coverage</h4><p>Visualise how thoroughly each topic is covered.</p></div>
    <div class="mod-card c3"><div class="mi">⭐</div><h4>Importance Ranking</h4><p>Score and rank topics by exam significance.</p></div>
  </div>

  <div class="lbl">Learning Insights</div>
  <div class="stats">
    <div class="stat"><div class="sv">{topic_count}</div><div class="sl">Topics Found</div></div>
    <div class="stat"><div class="sv">{chunk_count}</div><div class="sl">Chunks Analysed</div></div>
    <div class="stat"><div class="sv">{doc_count}</div><div class="sl">Pages Loaded</div></div>
    <div class="stat"><div class="sv {status_cls}">{status_txt}</div><div class="sl">Processing Status</div></div>
  </div>

  <div class="lbl">Analysis Workspace</div>
  <div class="ws">
    <div class="ws-panel"><div class="wpt">Top Topics</div>{topic_items}</div>
    <div class="ws-panel"><div class="wpt">Coverage</div>{cov_bars}</div>
    <div class="ws-panel"><div class="wpt">Importance Ranking</div>{rank_items}</div>
  </div>

  <div class="lbl">Generate Analysis</div>
  <div class="gen-panel">
    <div class="gpt">Analyse your documents</div>
    <div class="gpd">Enter a topic below and choose an analysis type</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # Streamlit widgets — must be separate calls
    topic = st.text_input(
        "Topic", key="analysis_topic",
        placeholder="e.g. Machine Learning, Cell Biology, Thermodynamics…",
        label_visibility="collapsed")

    c1, c2, c3 = st.columns(3, gap="small")
    with c1: topic_extract   = st.button("🧠 Extract Topics",    use_container_width=True)
    with c2: topic_coverage  = st.button("📈 Topic Coverage",    use_container_width=True)
    with c3: importance_rank = st.button("⭐ Rank by Importance", use_container_width=True)

    if topic_extract or topic_coverage or importance_rank:
        if not topic:
            st.warning("Please enter a topic first."); return

        docs = retrieve(topic, vector_db)
        if not docs:
            st.warning("No relevant content found for that topic."); return

        context = "\n".join(doc.page_content for doc in docs)
        st.markdown("---")

        if topic_extract:
            st.markdown("#### 🧠 Extracted Topics")
            result = generate_topic_extractor(context)
            render_topics(safe_json(result))
            if "Extracted Topics" not in st.session_state.get("activity_log",[]):
                st.session_state.activity_log.append("Extracted Topics")

        if topic_coverage:
            st.markdown("#### 📈 Topic Coverage")
            result = generate_topic_coverage(context)
            render_coverage(safe_json(result))

        if importance_rank:
            st.markdown("#### ⭐ Importance Ranking")
            topics_data = generate_topic_extractor(context)
            result = generate_importance_ranker(context, topics_data)
            render_importance(safe_json(result))
