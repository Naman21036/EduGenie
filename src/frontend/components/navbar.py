from streamlit_option_menu import option_menu
import streamlit as st

def render_navbar():
    # Inject compact navbar CSS override
    st.markdown(
        """
        <style>
        /* ── Navbar wrapper ── */
        [data-testid="stHorizontalBlock"]:has(.nav-host) {
            gap: 0 !important;
        }
        div[class*="option-menu"] {
            font-family: 'Inter', sans-serif !important;
        }
        /* Remove default Streamlit top padding so navbar sits flush */
        .block-container {
            padding-top: 0.75rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Study Tools",
            "Analysis",
            "Exam Prep",
            "Chat",
        ],
        icons=[
            "grid-1x2",
            "journal-text",
            "bar-chart-line",
            "clipboard2-check",
            "chat-dots",
        ],
        default_index=[
            "Dashboard",
            "Study Tools",
            "Analysis",
            "Exam Prep",
            "Chat",
        ].index(
            st.session_state.get(
                "selected_page",
                "Dashboard",
            )
        ),
        orientation="horizontal",
        styles={
            "container": {
                "padding": "6px 10px",
                "background-color": "#111827",        # was #0c1120 — deeper navy matches Surface bg
                "border-radius": "14px",
                "border": "1px solid rgba(59,130,246,0.18)",  # was rgba(99,102,241,0.18) — blue instead of purple
                "margin-bottom": "18px",
            },
            "icon": {
                "font-size": "14px",
                "color": "#60a5fa",                   # was unset — explicit Primary Light blue for all icons
            },
            "nav-link": {
                "font-size": "13.5px",
                "font-weight": "500",
                "color": "#94a3b8",                   # unchanged — Muted Text, still correct
                "border-radius": "10px",
                "padding": "8px 16px",
                "letter-spacing": "0.01em",
            },
            "nav-link-selected": {
                "background-color": "#1e293b",        # was #1e1b4b — neutral slate Surface instead of indigo tint
                "color": "#60a5fa",                   # was #a5b4fc — Primary Light blue instead of lavender
                "font-weight": "600",
            },
            "nav-link:hover": {
                "background-color": "#273449",        # was #1e293b — slightly lighter Surface Hover
                "color": "#f8fafc",                   # was #e2e8f0 — full Text white on hover for contrast
            },
        },
    )
    return selected
