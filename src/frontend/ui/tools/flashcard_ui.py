import json
import streamlit as st
import streamlit.components.v1 as components
from ingestion.retriever import retrieve
from study_tools.flashcard_generator import generate_flashcards
from frontend.components.cards import render_flashcards as render_flashcard_cards

_CSS = """
<style>
.fc-root * { box-sizing: border-box; font-family: 'Inter', sans-serif; }
.fc-root .ph { margin-bottom: 14px; }
.fc-root .ph h3 { font-size: 1.1rem; font-weight: 700; color: #F8FAFC !important; margin: 0 0 2px; }
.fc-root .ph p  { font-size: 12.5px; color: #4B5A72 !important; margin: 0; }
.fc-root .lbl { font-size: 10.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: #4B5A72; margin: 14px 0 8px; display: flex; align-items: center; gap: 8px; }
.fc-root .lbl::after { content: ""; flex: 1; height: 1px; background: #273449; }
.fc-root .cfg { background: #161B2E; border: 1px solid rgba(16,185,129,.2); border-radius: 12px; padding: 13px 17px; }
.fc-root .cfg .ct { font-size: 12.5px; font-weight: 600; color: #E2E8F0 !important; margin: 0 0 2px; display: block; }
.fc-root .cfg .cd { font-size: 11.5px; color: #4B5A72 !important; margin: 0; display: block; }
/* stats row */
.fc-root .fstats { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; margin-bottom: 0; }
.fc-root .fs { background: #161B2E; border: 1px solid #273449; border-radius: 10px; padding: 10px 14px; }
.fc-root .fs .fv { font-size: 18px; font-weight: 800; color: #10B981 !important; line-height: 1; display: block; }
.fc-root .fs .fl { font-size: 10.5px; color: #4B5A72 !important; margin-top: 2px; display: block; }
</style>
"""


def _safe_parse(flashcards):
    if isinstance(flashcards, list):
        cleaned = []
        for card in flashcards:
            if isinstance(card, str):
                try: card = json.loads(card)
                except: continue
            cleaned.append(card)
        return cleaned
    if isinstance(flashcards, str):
        raw = flashcards.replace("```json","").replace("```","").strip()
        try: return json.loads(raw)
        except: return []
    return []


def render_flashcards(vector_db):

    components.html(_CSS, height=0)

    st.markdown("""
<div class="fc-root">
  <div class="ph">
    <h3>🃏 Flashcard Generator</h3>
    <p>Generate spaced repetition flashcards for active recall learning</p>
  </div>
  <div class="lbl">Configuration</div>
  <div class="cfg">
    <span class="ct">Front &amp; back format</span>
    <span class="cd">Each card contains a term or concept on the front and a detailed explanation on the back</span>
  </div>
  <div class="lbl">Generate</div>
</div>
""", unsafe_allow_html=True)

    topic = st.text_input(
        "Topic", key="flash_topic",
        placeholder="e.g. Organic Chemistry, Supply and Demand, Neural Networks…",
        label_visibility="collapsed")

    num_cards = st.slider("Number of Flashcards", min_value=1, max_value=50, value=10)

    if st.button("🃏 Generate Flashcards", use_container_width=True, type="primary"):
        if not topic.strip():
            st.warning("Please enter a topic first."); return

        docs = retrieve(topic, vector_db)
        if not docs:
            st.warning("No relevant content found for that topic."); return

        context = "\n".join(doc.page_content for doc in docs)

        with st.spinner("Generating flashcards…"):
            raw = generate_flashcards(context, num_cards)

        cards = _safe_parse(raw)
        if not cards:
            st.warning("Could not parse flashcard response."); return

        # Stats summary
        st.markdown(f"""
<div class="fc-root">
  <div class="lbl">Results</div>
  <div class="fstats">
    <div class="fs"><span class="fv">{len(cards)}</span><span class="fl">Cards Generated</span></div>
    <div class="fs"><span class="fv">{topic[:12]}{'…' if len(topic)>12 else ''}</span><span class="fl">Topic</span></div>
    <div class="fs"><span class="fv">Ready</span><span class="fl">Status</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")
        render_flashcard_cards(cards)

        log = st.session_state.get("activity_log", [])
        st.session_state.activity_log = log
        st.session_state.activity_log.append(f"Generated {len(cards)} Flashcards")
