import json
import streamlit as st
from ingestion.retriever import retrieve
from analysis.topic_extractor import generate_topic_extractor
from analysis.topic_coverage import generate_topic_coverage
from analysis.importance_ranker import generate_importance_ranker


#CSS 

ANALYSIS_CSS = """
<style>
/* ── Page header ── */
.an-header { margin-bottom: 22px; }
.an-header h2 {
    font-size: 1.35rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 4px;
    letter-spacing: -0.02em;
}
.an-header p { font-size: 13px; color: #475569; margin: 0; }

/* ── Section label ── */
.an-label {
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
.an-label::after { content:""; flex:1; height:1px; background:rgba(255,255,255,0.05); }

/* ── Module cards (top row) ── */
.module-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; }
.module-card {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.module-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 14px 14px 0 0;
}
.module-card.extract::before { background: #3b82f6; }
.module-card.coverage::before { background: #22c55e; }
.module-card.ranking::before  { background: #f59e0b; }
.module-card .mc-icon { font-size: 22px; margin-bottom: 10px; }
.module-card h4 { font-size: 14px; font-weight: 700; color: #e2e8f0; margin: 0 0 5px; }
.module-card p  { font-size: 12px; color: #475569; margin: 0; line-height: 1.5; }

/* ── Insight stat bar ── */
.insight-bar { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; }
.insight-box {
    background: #0c1120;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 14px 16px;
}
.insight-box .ib-val { font-size: 22px; font-weight: 800; color: #60a5fa; letter-spacing:-0.02em; }
.insight-box .ib-lbl { font-size: 11px; color: #475569; margin-top: 3px; }
.insight-box.status .ib-val { font-size: 14px; padding-top: 3px; }
.insight-box.status .ib-val.ready   { color: #4ade80; }
.insight-box.status .ib-val.waiting { color: #f87171; }

/* ── Workspace panel (used inside st.columns, one per column) ── */
.ws-panel {
    background: #0c1120;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 18px 20px;
    min-height: 220px;
}
.ws-panel .wp-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #475569;
    margin: 0 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
/* Topic list */
.topic-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 13px;
    color: #94a3b8;
}
.topic-item:last-child { border-bottom: none; }
.topic-item .ti-badge {
    font-size: 10px;
    font-weight: 700;
    color: #3b82f6;
    background: rgba(59,130,246,0.12);
    border-radius: 4px;
    padding: 1px 6px;
    flex-shrink: 0;
}
/* Coverage bars */
.cov-row { margin-bottom: 10px; }
.cov-label { font-size: 12px; color: #94a3b8; margin-bottom: 5px; display:flex; justify-content:space-between; }
.cov-track { height: 6px; background: rgba(255,255,255,0.06); border-radius: 4px; overflow: hidden; }
.cov-fill  { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #3b82f6, #06b6d4); }
/* Rank list */
.rank-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 13px;
    color: #94a3b8;
}
.rank-item:last-child { border-bottom: none; }
.rank-item .ri-num {
    font-size: 11px;
    font-weight: 700;
    color: #3b82f6;
    width: 20px;
    flex-shrink: 0;
}
.rank-item .ri-score {
    margin-left: auto;
    font-size: 11px;
    font-weight: 700;
    color: #f59e0b;
}
/* Empty state (inside a ws-panel) */
.ws-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px 16px;
    text-align: center;
    gap: 8px;
}
.ws-empty-icon { font-size: 26px; opacity: 0.35; line-height: 1; }
.ws-empty-title {
    font-size: 13px;
    font-weight: 600;
    color: #475569;
    margin: 4px 0 0;
}
.ws-empty-sub {
    font-size: 12px;
    color: #334155;
    line-height: 1.5;
    margin: 0;
}

/* ── Action area ── */
.action-area {
    background: #0c1120;
    border: 1px solid rgba(59,130,246,0.18);
    border-radius: 14px;
    padding: 20px 22px;
}
.action-area .aa-title {
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


#Result renderers (clean Streamlit native)

def render_topics(result):
    topics = result.get("topics", [])
    if not topics:
        st.info("No topics returned.")
        return
    for item in topics:
        with st.expander(f"🏷️ {item.get('topic', 'Unknown')}", expanded=False):
            for sub in item.get("subtopics", []):
                st.markdown(f"• {sub}")


def render_coverage(result):
    coverage = result.get("topic_coverage", [])
    if not coverage:
        st.info("No coverage data returned.")
        return
    for item in coverage:
        pct = min(max(int(item.get("coverage_percentage", 0)), 0), 100)
        st.markdown(f"**{item.get('topic','Unknown')}**")
        st.progress(pct)
        st.caption(f"{pct}% · {item.get('coverage_level','Unknown')}")
        subs = item.get("subtopics", [])
        if subs:
            st.caption(", ".join(subs))


def render_importance(result):
    ranked = result.get("ranked_topics", [])
    if not ranked:
        st.info("No ranking data returned.")
        return
    medals = ["🥇", "🥈", "🥉"]
    for idx, topic in enumerate(ranked):
        icon = medals[idx] if idx < 3 else "⭐"
        score = min(max(int(topic.get("importance_score", 0)), 0), 100)
        with st.expander(f"{icon} {topic.get('topic','Unknown')} — {score}/100", expanded=False):
            st.progress(score)
            st.caption(topic.get("reason", ""))


def _panel_topics(topics_result):
    topics = (topics_result or {}).get("topics", [])
    if not topics:
        body = (
            '<div class="ws-empty">'
            '<div class="ws-empty-icon">🔍</div>'
            '<p class="ws-empty-title">No topics extracted yet</p>'
            '<p class="ws-empty-sub">Run Topic Extraction to populate this panel.</p>'
            '</div>'
        )
    else:
        rows = []
        for i, item in enumerate(topics[:6]):
            label = item.get("topic", "")
            rows.append(
                f'<div class="topic-item">'
                f'<span class="ti-badge">T{i + 1}</span>'
                f'{label}'
                f'</div>'
            )
        body = "".join(rows)

    return (
        '<div class="ws-panel">'
        '<div class="wp-title">Top Topics</div>'
        + body +
        '</div>'
    )


def _panel_coverage(coverage_result):
    coverage = (coverage_result or {}).get("topic_coverage", [])
    if not coverage:
        body = (
            '<div class="ws-empty">'
            '<div class="ws-empty-icon">🗺️</div>'
            '<p class="ws-empty-title">No coverage data yet</p>'
            '<p class="ws-empty-sub">Run Topic Coverage to populate this panel.</p>'
            '</div>'
        )
    else:
        rows = []
        for item in coverage[:5]:
            pct = min(max(int(item.get("coverage_percentage", 0)), 0), 100)
            label = item.get("topic", "")
            rows.append(
                '<div class="cov-row">'
                '<div class="cov-label">'
                f'<span>{label}</span><span>{pct}%</span>'
                '</div>'
                '<div class="cov-track">'
                f'<div class="cov-fill" style="width:{pct}%"></div>'
                '</div>'
                '</div>'
            )
        body = "".join(rows)

    return (
        '<div class="ws-panel">'
        '<div class="wp-title">Coverage Visualisation</div>'
        + body +
        '</div>'
    )


def _panel_ranking(importance_result):
    ranked = (importance_result or {}).get("ranked_topics", [])
    if not ranked:
        body = (
            '<div class="ws-empty">'
            '<div class="ws-empty-icon">🏆</div>'
            '<p class="ws-empty-title">No rankings yet</p>'
            '<p class="ws-empty-sub">Run Importance Ranking to populate this panel.</p>'
            '</div>'
        )
    else:
        rows = []
        for i, item in enumerate(ranked[:5]):
            topic = item.get("topic", "")
            score = min(max(int(item.get("importance_score", 0)), 0), 100)
            rows.append(
                '<div class="rank-item">'
                f'<span class="ri-num">#{i + 1}</span>'
                f'<span>{topic}</span>'
                f'<span class="ri-score">{score}</span>'
                '</div>'
            )
        body = "".join(rows)

    return (
        '<div class="ws-panel">'
        '<div class="wp-title">Importance Ranking</div>'
        + body +
        '</div>'
    )


# Main render

def render_analysis(vector_db):

    st.markdown(ANALYSIS_CSS, unsafe_allow_html=True)

    doc_count   = st.session_state.get("doc_count", 0)
    chunk_count = st.session_state.get("chunk_count", 0)
    topic_count = st.session_state.get("topic_count", 0)
    processed   = st.session_state.get("processed", False)

    # Page header
    st.markdown(
        '<div class="an-header">'
        '<h2>📊 Content Analysis</h2>'
        '<p>Understand your learning material — extract topics, measure coverage, rank by importance</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    #Analysis modules
    st.markdown('<div class="an-label">Analysis Modules</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="module-grid">'
        '<div class="module-card extract">'
        '<div class="mc-icon">🔍</div>'
        '<h4>Topic Extraction</h4>'
        '<p>Identify all major topics and subtopics present in your documents.</p>'
        '</div>'
        '<div class="module-card coverage">'
        '<div class="mc-icon">🗺️</div>'
        '<h4>Topic Coverage</h4>'
        '<p>Visualise how thoroughly each topic is covered across your material.</p>'
        '</div>'
        '<div class="module-card ranking">'
        '<div class="mc-icon">🏆</div>'
        '<h4>Importance Ranking</h4>'
        '<p>Score and rank topics by their significance and exam relevance.</p>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    #Learning insights
    st.markdown('<div class="an-label">Learning Insights</div>', unsafe_allow_html=True)

    status_cls = "ready" if processed else "waiting"
    status_txt = "Ready" if processed else "Waiting"

    # Build insight bar as plain string concatenation — no multiline f-string
    insight_html = (
        '<div class="insight-bar">'
        '<div class="insight-box">'
        f'<div class="ib-val">{topic_count}</div>'
        '<div class="ib-lbl">Topics Found</div>'
        '</div>'
        '<div class="insight-box">'
        f'<div class="ib-val">{chunk_count}</div>'
        '<div class="ib-lbl">Chunks Analysed</div>'
        '</div>'
        '<div class="insight-box">'
        f'<div class="ib-val">{doc_count}</div>'
        '<div class="ib-lbl">Pages Loaded</div>'
        '</div>'
        '<div class="insight-box status">'
        f'<div class="ib-val {status_cls}">{status_txt}</div>'
        '<div class="ib-lbl">Processing Status</div>'
        '</div>'
        '</div>'
    )
    st.markdown(insight_html, unsafe_allow_html=True)

    #Analysis workspace 
    st.markdown('<div class="an-label">Analysis Workspace</div>', unsafe_allow_html=True)

    topics_result     = st.session_state.get("analysis_topics_result", None)
    coverage_result   = st.session_state.get("analysis_coverage_result", None)
    importance_result = st.session_state.get("analysis_importance_result", None)

    ws_col1, ws_col2, ws_col3 = st.columns(3, gap="small")

    with ws_col1:
        st.markdown(_panel_topics(topics_result), unsafe_allow_html=True)

    with ws_col2:
        st.markdown(_panel_coverage(coverage_result), unsafe_allow_html=True)

    with ws_col3:
        st.markdown(_panel_ranking(importance_result), unsafe_allow_html=True)

    #Action area 
    st.markdown('<div class="an-label">Generate Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="action-area">'
        '<div class="aa-title">Enter a topic to analyse your documents</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Topic",
        key="analysis_topic",
        placeholder="e.g. Electrostatic Discharge, Machine Learning, Cell Biology…",
        label_visibility="collapsed",
    )

    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        topic_extract   = st.button("🔍 Extract Topics",     use_container_width=True)
    with col2:
        topic_coverage  = st.button("🗺️ Topic Coverage",     use_container_width=True)
    with col3:
        importance_rank = st.button("🏆 Rank by Importance",  use_container_width=True)

    #Results
    if topic_extract or topic_coverage or importance_rank:
        if not topic:
            st.warning("Please enter a topic first.")
            return

        docs = retrieve(topic, vector_db)
        if not docs:
            st.warning("No relevant content found for that topic.")
            return

        context = "\n".join(doc.page_content for doc in docs)

        if topic_extract:
            st.markdown("---")
            st.markdown("#### 🔍 Extracted Topics")
            result = generate_topic_extractor(context)
            parsed = safe_json(result)
            st.session_state["analysis_topics_result"] = parsed
            render_topics(parsed)

        if topic_coverage:
            st.markdown("---")
            st.markdown("#### 🗺️ Topic Coverage")
            result = generate_topic_coverage(context)
            parsed = safe_json(result)
            st.session_state["analysis_coverage_result"] = parsed
            render_coverage(parsed)

        if importance_rank:
            st.markdown("---")
            st.markdown("#### 🏆 Importance Ranking")
            topics_raw = generate_topic_extractor(context)
            result = generate_importance_ranker(context, topics_raw)
            parsed = safe_json(result)
            st.session_state["analysis_importance_result"] = parsed
            render_importance(parsed)

        # Rerun so workspace panels reflect the new results immediately
        st.rerun()
