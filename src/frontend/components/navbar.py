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
                "background-color": "#0c1120",
                "border-radius": "14px",
                "border": "1px solid rgba(99,102,241,0.18)",
                "margin-bottom": "18px",
            },
            "icon": {
                "font-size": "14px",
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
                "background-color": "#1e1b4b",
                "color": "#a5b4fc",
                "font-weight": "600",
            },
            "nav-link:hover": {
                "background-color": "#1e293b",
                "color": "#e2e8f0",
            },
        },
    )

    return selected