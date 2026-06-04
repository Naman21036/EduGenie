from streamlit_option_menu import option_menu


def render_navbar():

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
                "border": "1px solid rgba(255,255,255,0.08)"
            },
            "nav-link": {
                "font-size": "15px",
                "font-weight": "600",
                "color": "#cbd5e1",
                "border-radius": "12px",
            },
            "nav-link-selected": {
                "background":
                "linear-gradient(135deg,#6366f1,#8b5cf6)",
                "color": "white",
            }
        }
    )

    return selected