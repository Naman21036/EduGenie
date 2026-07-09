from streamlit_option_menu import option_menu
import streamlit as st

def render_navbar():
    st.markdown(
        """
        <style>
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
                "background-color": "#111827",
                "border-radius": "14px",
                "border": "1px solid rgba(59,130,246,0.18)",
                "margin-bottom": "18px",
            },
            "icon": {
                "font-size": "14px",
                "color": "#60a5fa",
            },
            "nav-link": {
                "font-size": "13.5px",
                "font-weight": "500",
                "color": "#94a3b8",
                "border-radius": "10px",
                "padding": "8px 16px",
                "letter-spacing": "0.01em",
            },
            "nav-link-selected": {
                "background-color": "#1e293b",
                "color": "#60a5fa",
                "font-weight": "600",
            },
            "nav-link:hover": {
                "background-color": "#273449",
                "color": "#f8fafc",
            },
        },
    )
    return selected
