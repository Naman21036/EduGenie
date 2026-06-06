import streamlit as st


def render_sidebar():

    with st.sidebar:

        # ── Sidebar base styles ──────────────────────────
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
                border-right: 1px solid rgba(59,130,246,0.15);
            }
            [data-testid="stSidebar"] .stMarkdown p,
            [data-testid="stSidebar"] .stMarkdown span {
                color: #94a3b8;
                font-size: 13px;
            }
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {
                color: #e2e8f0;
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 0.07em;
                text-transform: uppercase;
                margin: 0 0 8px;
            }
            /* Wordmark */
            .sb-wordmark {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 18px 4px 14px;
                border-bottom: 1px solid rgba(255,255,255,0.06);
                margin-bottom: 20px;
            }
            .sb-wordmark .icon {
                width: 34px;
                height: 34px;
                border-radius: 10px;
                background: linear-gradient(135deg, #3b82f6, #06b6d4);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                flex-shrink: 0;
            }
            .sb-wordmark .name {
                font-size: 16px;
                font-weight: 700;
                color: #e2e8f0;
                letter-spacing: -0.01em;
            }
            .sb-wordmark .tag {
                font-size: 11px;
                color: #3b82f6;
                font-weight: 500;
                margin-top: 1px;
            }
            /* Status pill */
            .sb-status {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                margin-bottom: 20px;
            }
            .sb-status.ready {
                background: rgba(16,185,129,0.12);
                color: #34d399;
                border: 1px solid rgba(52,211,153,0.2);
            }
            .sb-status.waiting {
                background: rgba(239,68,68,0.1);
                color: #f87171;
                border: 1px solid rgba(248,113,113,0.2);
            }
            .sb-dot { width: 6px; height: 6px; border-radius: 50%; }
            .sb-dot.ready { background: #34d399; }
            .sb-dot.waiting { background: #f87171; }
            /* Section label */
            .sb-label {
                font-size: 10.5px;
                font-weight: 700;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: #475569;
                margin: 18px 0 8px;
                padding-bottom: 6px;
                border-bottom: 1px solid rgba(255,255,255,0.04);
            }
            /* Stat row */
            .sb-stats {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 8px;
                margin-bottom: 6px;
            }
            .sb-stat {
                background: #111827;
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 10px;
                padding: 10px 12px;
            }
            .sb-stat .val {
                font-size: 20px;
                font-weight: 700;
                color: #60a5fa;
                line-height: 1;
            }
            .sb-stat .lbl {
                font-size: 11px;
                color: #64748b;
                margin-top: 3px;
            }
            .sb-stat-full {
                background: #111827;
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 10px;
                padding: 10px 14px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 6px;
            }
            .sb-stat-full .lbl { font-size: 12px; color: #64748b; }
            .sb-stat-full .val { font-size: 16px; font-weight: 700; color: #60a5fa; }
            /* Activity items */
            .sb-activity-item {
                display: flex;
                align-items: flex-start;
                gap: 8px;
                padding: 7px 0;
                border-bottom: 1px solid rgba(255,255,255,0.04);
                font-size: 12px;
                color: #94a3b8;
            }
            .sb-activity-item .dot {
                width: 5px;
                height: 5px;
                border-radius: 50%;
                background: #3b82f6;
                margin-top: 5px;
                flex-shrink: 0;
            }
            /* Process Documents button — override Streamlit primary theme color */
            [data-testid="stSidebar"] .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #3b82f6, #06b6d4) !important;
                border: none !important;
                color: white !important;
                font-weight: 600 !important;
                border-radius: 12px !important;
            }
            [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
                filter: brightness(1.08);
            }
            /* File uploader — neutralise any purple focus/border remnants */
            [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
                border-color: rgba(59,130,246,0.25) !important;
            }
            [data-testid="stSidebar"] [data-testid="stFileUploader"] section:hover {
                border-color: rgba(59,130,246,0.50) !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # ── Wordmark ─────────────────────────────────────
        st.markdown(
            """
            <div class="sb-wordmark">
                <div class="icon">🎓</div>
                <div>
                    <div class="name">EduGenie</div>
                    <div class="tag">AI Learning Platform</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Status ───────────────────────────────────────
        is_ready = st.session_state.get("processed", False)
        status_class = "ready" if is_ready else "waiting"
        status_text = "Ready" if is_ready else "Waiting for upload"

        st.markdown(
            f"""
            <div class="sb-status {status_class}">
                <div class="sb-dot {status_class}"></div>
                {status_text}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Upload section ───────────────────────────────
        st.markdown(
            '<div class="sb-label">Document Upload</div>',
            unsafe_allow_html=True,
        )

        uploaded_files = st.file_uploader(
            "Drop PDF files here",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        process = st.button(
            "⚡  Process Documents",
            use_container_width=True,
            type="primary",
        )

        # ── Workspace stats ──────────────────────────────
        st.markdown(
            '<div class="sb-label">Workspace Stats</div>',
            unsafe_allow_html=True,
        )

        doc_count = st.session_state.get("doc_count", 0)
        chunk_count = st.session_state.get("chunk_count", 0)
        topic_count = st.session_state.get("topic_count", 0)

        st.markdown(
            f"""
            <div class="sb-stats">
                <div class="sb-stat">
                    <div class="val">{doc_count}</div>
                    <div class="lbl">Pages</div>
                </div>
                <div class="sb-stat">
                    <div class="val">{chunk_count}</div>
                    <div class="lbl">Chunks</div>
                </div>
            </div>
            <div class="sb-stat-full">
                <span class="lbl">Topics Extracted</span>
                <span class="val">{topic_count}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Quick actions ────────────────────────────────
        st.markdown(
            '<div class="sb-label">Quick Actions</div>',
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("🗑 Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.success("Chat cleared")

        with col_b:
            if st.button("🔄 Reset", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

        # ── Recent activity ──────────────────────────────
        activity_log = st.session_state.get("activity_log", [])

        if activity_log:
            st.markdown(
                '<div class="sb-label">Recent Activity</div>',
                unsafe_allow_html=True,
            )
            items_html = ""
            for item in reversed(activity_log[-6:]):
                items_html += f"""
                <div class="sb-activity-item">
                    <div class="dot"></div>
                    <span>{item}</span>
                </div>
                """
            st.markdown(items_html, unsafe_allow_html=True)

    return uploaded_files, process
