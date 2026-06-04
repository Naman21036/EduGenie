import streamlit as st
import streamlit.components.v1 as components
import json


def render_flashcards(cards):

    html = f"""
    <!DOCTYPE html>

    <html>

    <head>

    <style>

    body{{
        background:transparent;
        font-family:Inter,sans-serif;
    }}

    .grid{{
        display:grid;
        grid-template-columns:
        repeat(
            auto-fit,
            minmax(
                320px,
                1fr
            )
        );
        gap:24px;
        padding:10px;
    }}

    .card{{
        background:transparent;
        width:100%;
        height:250px;
        perspective:1000px;
    }}

    .card-inner{{
        position:relative;
        width:100%;
        height:100%;
        text-align:center;
        transition:transform .8s;
        transform-style:preserve-3d;
        cursor:pointer;
    }}

    .card:hover .card-inner{{
        transform:
        rotateY(
            180deg
        );
    }}

    .card-front,
    .card-back{{
        position:absolute;
        width:100%;
        height:100%;

        backface-visibility:hidden;

        border-radius:20px;

        display:flex;
        align-items:center;
        justify-content:center;

        padding:20px;

        box-sizing:border-box;

        border:
        1px solid
        rgba(
            255,
            255,
            255,
            .1
        );

        backdrop-filter:
        blur(
            20px
        );
    }}

    .card-front{{
        background:
        linear-gradient(
            135deg,
            #312e81,
            #4f46e5
        );

        color:white;
        font-size:1.2rem;
        font-weight:600;
    }}

    .card-back{{
        background:
        linear-gradient(
            135deg,
            #0f172a,
            #1e293b
        );

        color:white;

        transform:
        rotateY(
            180deg
        );

        overflow:auto;
    }}

    .hint{{
        text-align:center;
        margin-bottom:20px;
        color:#94a3b8;
    }}

    </style>

    </head>

    <body>

    <div class="hint">
        Hover over a card to reveal the answer
    </div>

    <div class="grid">
    """

    for card in cards:
        if not isinstance(
            card,
            dict
        ):
            continue

        front = card.get(
            "front",
            ""
        )

        back = card.get(
            "back",
            ""
        )

        html += f"""

        <div class="card">

            <div class="card-inner">

                <div class="card-front">

                    {front}

                </div>

                <div class="card-back">

                    {back}

                </div>

            </div>

        </div>

        """

    html += """
    </div>

    </body>

    </html>
    """

    components.html(
        html,
        height=800,
        scrolling=True
    )