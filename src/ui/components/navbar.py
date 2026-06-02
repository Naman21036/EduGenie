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
            "house",
            "book",
            "bar-chart",
            "clipboard",
            "chat-dots"
        ],
        orientation="horizontal",
        default_index=0
    )

    return selected