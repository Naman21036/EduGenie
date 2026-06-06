import streamlit as st
import streamlit.components.v1 as components


def render_flashcards(cards):
    """Render a grid of flip cards using components.html.

    Card front: blue/cyan gradient (replaces old purple #312e81 → #4f46e5).
    Card back: dark surface (unchanged).
    All flip animation logic is preserved exactly.
    """

    grid_items = ""
    for card in cards:
        if not isinstance(card, dict):
            continue
        front = card.get("front", "")
        back  = card.get("back", "")
        # Escape braces that aren't part of Python f-string interpolation
        grid_items += (
            f'<div class="card">'
            f'<div class="card-inner">'
            f'<div class="card-front">{front}</div>'
            f'<div class="card-back">{back}</div>'
            f'</div>'
            f'</div>'
        )

    html = f"""<!DOCTYPE html>
<html>
<head>
<style>
body {{
    background: transparent;
    font-family: Inter, sans-serif;
    margin: 0;
    padding: 0;
}}
.hint {{
    text-align: center;
    margin-bottom: 20px;
    color: #94a3b8;
    font-size: 13px;
}}
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    padding: 10px;
}}
.card {{
    background: transparent;
    width: 100%;
    height: 220px;
    perspective: 1000px;
}}
.card-inner {{
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.7s ease;
    transform-style: preserve-3d;
    cursor: pointer;
}}
.card:hover .card-inner {{
    transform: rotateY(180deg);
}}
.card-front,
.card-back {{
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    box-sizing: border-box;
    border: 1px solid rgba(255,255,255,0.08);
}}
.card-front {{
    background: linear-gradient(135deg, #1e3a8a, #3b82f6);
    color: white;
    font-size: 1.05rem;
    font-weight: 600;
    line-height: 1.45;
}}
.card-back {{
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #e2e8f0;
    transform: rotateY(180deg);
    overflow: auto;
    font-size: 0.9rem;
    line-height: 1.55;
}}
</style>
</head>
<body>
<div class="hint">Hover over a card to reveal the answer</div>
<div class="grid">
{grid_items}
</div>
</body>
</html>"""

    components.html(html, height=800, scrolling=True)
