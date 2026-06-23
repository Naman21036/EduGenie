import streamlit as st
from chatbot.chatbot import chat, plain_text_content
import html


def _sanitize_chat_history():
    st.session_state.chat_history = [
        {
            "role": msg["role"],
            "content": plain_text_content(msg["content"]),
        }
        for msg in st.session_state.chat_history
    ]


# ── Page-level CSS ───────────────────────────────────────────────────────────

CHAT_CSS = """
<style>
/* ── Page header ── */
.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}
.chat-header-left h2 {
    font-size: 1.35rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 4px;
    letter-spacing: -0.02em;
}
.chat-header-left p {
    font-size: 13px;
    color: #475569;
    margin: 0;
}
.kb-status {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}
.kb-status.ready {
    background: rgba(34,197,94,0.1);
    color: #4ade80;
    border: 1px solid rgba(74,222,128,0.2);
}
.kb-status.waiting {
    background: rgba(239,68,68,0.1);
    color: #f87171;
    border: 1px solid rgba(248,113,113,0.2);
}
.kb-dot { width: 6px; height: 6px; border-radius: 50%; }
.kb-dot.ready { background: #4ade80; }
.kb-dot.waiting { background: #f87171; }

/* ── Layout columns ── */
.chat-layout { display: flex; gap: 20px; align-items: flex-start; }

/* ── Welcome state ── */
.welcome-wrap {
    text-align: center;
    padding: 40px 20px 28px;
}
.welcome-wrap .wc-icon {
    font-size: 40px;
    margin-bottom: 14px;
}
.welcome-wrap h3 {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 8px;
}
.welcome-wrap p {
    font-size: 13.5px;
    color: #475569;
    margin: 0 auto 24px;
    max-width: 360px;
    line-height: 1.6;
}

/* ── Suggested prompt cards ── */
.prompt-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    max-width: 520px;
    margin: 0 auto;
}
.prompt-card {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 16px;
    text-align: left;
    cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
}
.prompt-card:hover {
    border-color: rgba(59,130,246,0.35);
    background: #111827;
}
.prompt-card .pc-icon { font-size: 18px; margin-bottom: 6px; }
.prompt-card .pc-title {
    font-size: 12.5px;
    font-weight: 600;
    color: #e2e8f0;
    margin: 0 0 3px;
}
.prompt-card .pc-desc {
    font-size: 11.5px;
    color: #475569;
    margin: 0;
}

/* ── Message thread ── */
.chat-thread {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 4px 0 16px;
}
.msg-row {
    display: flex;
    gap: 10px;
    align-items: flex-start;
}
.msg-row.user { flex-direction: row-reverse; }

.msg-avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    margin-top: 2px;
}
.msg-avatar.user-av { background: #2563eb; }
.msg-avatar.bot-av  { background: #1e293b; border: 1px solid rgba(59,130,246,0.25); }

.msg-bubble {
    max-width: 72%;
    padding: 11px 16px;
    border-radius: 16px;
    font-size: 14px;
    line-height: 1.65;
}
.msg-bubble.user {
    background: linear-gradient(135deg,#2563eb,#0891b2);
    color: #ffffff;
    border-bottom-right-radius: 4px;
}
.msg-bubble.bot {
    background: #111827;
    color: #cbd5e1;
    border: 1px solid rgba(255,255,255,0.06);
    border-bottom-left-radius: 4px;
}

/* ── Knowledge panel ── */
.kb-panel {
    background: #0c1120;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 20px;
    width: 220px;
    flex-shrink: 0;
}
.kb-panel .kp-title {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: #475569;
    margin: 0 0 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.kb-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 12.5px;
}
.kb-row:last-child { border-bottom: none; }
.kb-row .kr-label { color: #475569; }
.kb-row .kr-val   { color: #60a5fa; font-weight: 600; }
.kb-row .kr-val.ready { color: #4ade80; }

/* ── Input row ── */
.input-row {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-top: 12px;
}

/* ── Section label ── */
.section-label {
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin: 20px 0 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.05);
}
/* Chat Page Button Override */

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


def _page_header(processed, doc_count, chunk_count):
    kb_cls = "ready" if processed else "waiting"
    kb_txt = f"Knowledge base ready · {doc_count} pages · {chunk_count} chunks" if processed else "No documents loaded"

    st.markdown(
        f"""
        <div class="chat-header">
            <div class="chat-header-left">
                <h2>🤖 EduGenie Assistant</h2>
                <p>Ask questions from your uploaded documents</p>
            </div>
            <div class="kb-status {kb_cls}">
                <div class="kb-dot {kb_cls}"></div>
                {kb_txt}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _knowledge_panel(doc_count, chunk_count, topic_count, file_names, processed):
    file_label = file_names[0] if file_names else "—"
    if len(file_names) > 1:
        file_label += f" +{len(file_names)-1}"
    status_txt = "Ready"   if processed else "Waiting"
    status_cls = "ready"   if processed else ""

    st.markdown(
        f"""
        <div class="kb-panel">
            <div class="kp-title">Knowledge Base</div>
            <div class="kb-row">
                <span class="kr-label">File</span>
                <span class="kr-val" style="font-size:11px;max-width:110px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{file_label}</span>
            </div>
            <div class="kb-row">
                <span class="kr-label">Pages</span>
                <span class="kr-val">{doc_count}</span>
            </div>
            <div class="kb-row">
                <span class="kr-label">Chunks</span>
                <span class="kr-val">{chunk_count}</span>
            </div>
            <div class="kb-row">
                <span class="kr-label">Topics</span>
                <span class="kr-val">{topic_count}</span>
            </div>
            <div class="kb-row">
                <span class="kr-label">Status</span>
                <span class="kr-val {status_cls}">{status_txt}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


SUGGESTED_PROMPTS = [
    ("📄", "Summarise the document", "Give me a concise overview of the main content"),
    ("🧠", "Explain key concepts", "What are the most important ideas covered?"),
    ("🎯", "Generate exam questions", "Create 5 exam-style questions from this material"),
    ("📚", "Create revision notes", "Produce structured revision notes for this topic"),
]


def _welcome_state():
    st.markdown(
        """
        <div class="welcome-wrap">
            <div class="wc-icon">✦</div>
            <h3>How can I help you today?</h3>
            <p>Ask anything about your uploaded PDFs — I can summarise, explain, quiz and more.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-label">Suggested prompts</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2, gap="small")
    for i, (icon, title, desc) in enumerate(SUGGESTED_PROMPTS):
        with cols[i % 2]:
            # Visual card
            st.markdown(
                f"""
                <div class="prompt-card">
                    <div class="pc-icon">{icon}</div>
                    <div class="pc-title">{title}</div>
                    <div class="pc-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Functional button underneath
            if st.button(
                title,
                key=f"prompt_{i}",
                use_container_width=True,
            ):
                st.session_state["_prefill_prompt"] = desc


def _render_messages(chat_history):
    parts = ['<div class="chat-thread">']

    for msg in chat_history:
        role = msg["role"]
        content = html.escape(msg["content"])
        content = content.replace("\n", "<br>")

        if role == "user":
            parts.append(
                '<div class="msg-row user">'
                '<div class="msg-avatar user-av">👤</div>'
                f'<div class="msg-bubble user">{content}</div>'
                '</div>'
            )
        else:
            parts.append(
                '<div class="msg-row">'
                '<div class="msg-avatar bot-av">✦</div>'
                f'<div class="msg-bubble bot">{content}</div>'
                '</div>'
            )

    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def render_chatbot(vector_db):

    # Inject CSS once
    st.markdown(CHAT_CSS, unsafe_allow_html=True)

    # Read state
    doc_count   = st.session_state.get("doc_count", 0)
    chunk_count = st.session_state.get("chunk_count", 0)
    topic_count = st.session_state.get("topic_count", 0)
    file_names  = st.session_state.get("file_names", [])
    processed   = st.session_state.get("processed", False)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    _sanitize_chat_history()
    print("DEBUG chat_history:", st.session_state.chat_history)

    # ── Header ───────────────────────────────────────
    _page_header(processed, doc_count, chunk_count)

    # ── Two-column layout: chat | knowledge panel ────
    chat_col, panel_col = st.columns([5, 1], gap="medium")

    with panel_col:
        _knowledge_panel(doc_count, chunk_count, topic_count, file_names, processed)

    with chat_col:
        chat_history = st.session_state.chat_history

        if not chat_history:
            _welcome_state()
        else:
            _render_messages(chat_history)

        st.markdown("")  # breathing room

        # ── Input row ────────────────────────────────
        clear_col, _ = st.columns([1, 5])
        with clear_col:
            if st.button("🗑 Clear", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()

    # ── Chat input (full width, below columns) ───────
    # Pre-fill from suggested prompt click
    prefill = st.session_state.pop("_prefill_prompt", "")

    question = st.chat_input(
        "Ask a question about your documents…",
    )

    # Accept either typed input or prefill
    final_question = question or prefill

    if final_question:
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": plain_text_content(final_question),
            }
        )

        prior_history = st.session_state.chat_history[:-1]

        with st.spinner("Thinking…"):
            answer = chat(
                final_question,
                vector_db,
                prior_history,
            )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": plain_text_content(answer),
            }
        )

        # Log activity once
        if "AI Chat" not in st.session_state.get("activity_log", []):
            st.session_state.activity_log.append("AI Chat")

        st.rerun()
