from streamlit_option_menu import option_menu
import streamlit as st

st.markdown(
    """
    <div style="
        padding:12px 20px;
        border-radius:15px;
        background:linear-gradient(
            135deg,
            rgba(99,102,241,.15),
            rgba(139,92,246,.15)
        );
        border:1px solid rgba(99,102,241,.25);
        margin-bottom:15px;
    ">
        🚀 Welcome to EduGenie AI Learning Workspace
    </div>
    """,
    unsafe_allow_html=True
)
def render_navbar():

    st.markdown(
        """
        <style>

        .nav-container{
            margin-bottom:20px;
        }

        div[data-testid="stHorizontalBlock"]{
            gap:0.5rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    selected = option_menu(
        menu_title=None,

        options=[
            "Dashboard",
            "Study Tools",
            "Analysis",
            "Exam Prep",
            "Chat"
        ],

        icons=[
            "house-fill",
            "book-fill",
            "graph-up-arrow",
            "clipboard2-check-fill",
            "robot"
        ],

        default_index=0,

        orientation="horizontal",

        styles={

            "container": {
                "padding": "12px",
                "background-color": "#0f172a",
                "border-radius": "18px",
                "border": "1px solid rgba(255,255,255,0.08)",
                "box-shadow":
                "0 8px 24px rgba(0,0,0,0.25)"
            },

            "nav-link": {

                "font-size": "15px",

                "font-weight": "600",

                "text-align": "center",

                "padding": "12px 20px",

                "margin": "0px 5px",

                "border-radius": "12px",

                "color": "#cbd5e1",

                "--hover-color": "#1e293b",

            },

            "nav-link-selected": {

                "background":
                "linear-gradient(135deg,#6366f1,#8b5cf6)",

                "color": "white",

                "font-weight": "700",

                "box-shadow":
                "0 0 15px rgba(99,102,241,0.45)"
            },

            "icon": {
                "font-size": "18px"
            }
        }
    )

    return selected