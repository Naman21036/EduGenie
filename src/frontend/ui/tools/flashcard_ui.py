import json
import streamlit as st

from ingestion.retriever import retrieve
from study_tools.flashcard_generator import generate_flashcards
from frontend.components.cards import render_flashcards as render_flashcard_cards


FLASH_CSS = """
<style>
.flash-header { margin-bottom: 18px; }
.flash-header h3 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0 0 4px;
    letter-spacing: -0.02em;
}
.flash-header p { font-size: 13px; color: #475569; margin: 0; }

.flash-config {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 16px;
}
.flash-config .fc-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 14px;
}
</style>
"""


def _parse_flashcards(raw):
    """Normalise flashcard output — accepts list, JSON string, or dict (error)."""
    if isinstance(raw, dict):
        return None, raw.get("error", "Generation failed"), raw.get("raw_response", "")
    if isinstance(raw, str):
        cleaned = raw.replace("```json", "").replace("```", "").strip()
        try:
            raw = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            return None, f"Could not parse model output: {exc}", cleaned
    if not isinstance(raw, list):
        return None, "Unexpected output format from model.", str(raw)
    cleaned_cards = []
    for card in raw:
        if isinstance(card, str):
            try:
                card = json.loads(card)
            except Exception:
                continue
        if isinstance(card, dict):
            cleaned_cards.append(card)
    return cleaned_cards, None, None


def render_flashcards(vector_db):

    st.markdown(FLASH_CSS, unsafe_allow_html=True)

    # ── Header ───────────────────────────────────────
    st.markdown(
        '<div class="flash-header">'
        '<h3>🃏 Flashcard Generator</h3>'
        '<p>Create interactive flip cards for active recall and spaced repetition.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Configuration panel ───────────────────────────
    st.markdown(
        '<div class="flash-config"><div class="fc-title">Configuration</div></div>',
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Topic",
        key="flash_topic",
        placeholder="e.g. Mitosis, Electromagnetism, Renaissance Art…",
    )

    num_cards = st.number_input(
        "Number of Flashcards",
        min_value=1,
        max_value=50,
        value=10,
        key="flash_count",
    )

    # ── Generate ──────────────────────────────────────
    generate_btn = st.button(
        f"🃏 Generate {int(num_cards)} Flashcard{'s' if num_cards != 1 else ''}",
        key="flash_btn",
        use_container_width=True,
        type="primary",
    )

    if generate_btn:

        if not topic.strip():
            st.warning("Please enter a topic before generating flashcards.")
            return

        docs = retrieve(topic, vector_db)

        if not docs:
            st.warning("No relevant content found for that topic. Try a different keyword.")
            return

        context = "\n".join(doc.page_content for doc in docs)

        with st.spinner(f"Generating {int(num_cards)} flashcards…"):
            raw = generate_flashcards(context, num_cards)

        cards, err_msg, raw_response = _parse_flashcards(raw)

        if err_msg:
            st.error(err_msg)
            if raw_response:
                with st.expander("Raw model output"):
                    st.code(raw_response)
            return

        if not cards:
            st.error("No flashcards were returned. Please try again.")
            return

        st.markdown(
            f'<p style="font-size:13px; color:#475569; margin:16px 0 4px;">'
            f'{len(cards)} card{"s" if len(cards) != 1 else ""} generated — hover to flip</p>',
            unsafe_allow_html=True,
        )

        render_flashcard_cards(cards)

        # ── Activity log ──────────────────────────────
        if "activity_log" not in st.session_state:
            st.session_state.activity_log = []
        entry = f"Generated {len(cards)} Flashcards"
        if entry not in st.session_state.activity_log:
            st.session_state.activity_log.append(entry)
