"""Shared SVG icon helpers for production UI (no emoji)."""

ICON_CSS = """
<style>
.ui-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    vertical-align: middle;
    color: currentColor;
    line-height: 0;
}
.ui-icon svg {
    width: 100%;
    height: 100%;
    stroke: currentColor;
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
}
.ui-icon--xs { width: 14px; height: 14px; }
.ui-icon--sm { width: 16px; height: 16px; }
.ui-icon--md { width: 20px; height: 20px; }
.ui-icon--lg { width: 24px; height: 24px; }
.ui-icon--xl { width: 28px; height: 28px; }
.ui-icon--accent { color: #60a5fa; }
.ui-icon--muted { color: #64748b; }
.ui-icon--white { color: #ffffff; }
.rank-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 1.25rem;
    height: 1.25rem;
    padding: 0 0.35rem;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.02em;
    background: rgba(59, 130, 246, 0.15);
    color: #93c5fd;
    margin-right: 0.35rem;
}
.rank-badge.top {
    background: rgba(59, 130, 246, 0.22);
    color: #bfdbfe;
}
</style>
"""

_SVG = {
    "logo": (
        '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>'
        '<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>'
        '<path d="M8 7h8"/><path d="M8 11h8"/>'
    ),
    "document": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="16" y1="13" x2="8" y2="13"/>'
        '<line x1="16" y1="17" x2="8" y2="17"/>'
    ),
    "notes": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="16" y1="13" x2="8" y2="13"/>'
        '<line x1="16" y1="17" x2="8" y2="17"/>'
    ),
    "mcq": (
        '<path d="M9 11l3 3L22 4"/>'
        '<path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'
    ),
    "flashcards": (
        '<rect x="8" y="2" width="13" height="18" rx="2"/>'
        '<path d="M3 6h13a2 2 0 0 1 2 2v12"/>'
    ),
    "question_bank": (
        '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>'
        '<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>'
        '<path d="M8 7h6"/><path d="M8 11h6"/><path d="M8 15h4"/>'
    ),
    "chat": (
        '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'
    ),
    "analysis": (
        '<line x1="18" y1="20" x2="18" y2="10"/>'
        '<line x1="12" y1="20" x2="12" y2="4"/>'
        '<line x1="6" y1="20" x2="6" y2="14"/>'
    ),
    "exam": (
        '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>'
        '<rect x="8" y="2" width="8" height="4" rx="1"/>'
        '<path d="M9 14l2 2 4-4"/>'
    ),
    "revision": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
        '<line x1="12" y1="18" x2="12" y2="12"/>'
        '<line x1="9" y1="15" x2="15" y2="15"/>'
    ),
    "mock_test": (
        '<path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2"/>'
        '<rect x="9" y="3" width="6" height="4" rx="1"/>'
        '<line x1="9" y1="12" x2="15" y2="12"/>'
        '<line x1="9" y1="16" x2="13" y2="16"/>'
    ),
    "topics": (
        '<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/>'
        '<line x1="7" y1="7" x2="7.01" y2="7"/>'
    ),
    "coverage": (
        '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/>'
        '<path d="M22 12A10 10 0 0 0 12 2v10z"/>'
    ),
    "ranking": (
        '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>'
        '<polyline points="17 6 23 6 23 12"/>'
    ),
    "study": (
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
    ),
    "user": (
        '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>'
        '<circle cx="12" cy="7" r="4"/>'
    ),
    "assistant": (
        '<rect x="3" y="11" width="18" height="10" rx="2"/>'
        '<circle cx="12" cy="5" r="2"/>'
        '<path d="M12 7v4"/>'
        '<line x1="8" y1="16" x2="8" y2="16"/>'
        '<line x1="16" y1="16" x2="16" y2="16"/>'
    ),
    "summarize": (
        '<line x1="21" y1="10" x2="7" y2="10"/>'
        '<line x1="21" y1="6" x2="3" y2="6"/>'
        '<line x1="21" y1="14" x2="3" y2="14"/>'
        '<line x1="21" y1="18" x2="7" y2="18"/>'
    ),
    "concepts": (
        '<circle cx="12" cy="12" r="10"/>'
        '<line x1="12" y1="16" x2="12" y2="12"/>'
        '<line x1="12" y1="8" x2="12.01" y2="8"/>'
    ),
    "questions": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>'
        '<line x1="12" y1="17" x2="12.01" y2="17"/>'
    ),
    "pages": (
        '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<polyline points="14 2 14 8 20 8"/>'
    ),
    "chunks": (
        '<rect x="3" y="3" width="7" height="7"/>'
        '<rect x="14" y="3" width="7" height="7"/>'
        '<rect x="14" y="14" width="7" height="7"/>'
        '<rect x="3" y="14" width="7" height="7"/>'
    ),
    "insight": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="M12 16v-4"/><path d="M12 8h.01"/>'
    ),
}


def inject_icon_styles():
    """Return CSS for icons; inject once per page via st.markdown."""
    return ICON_CSS


def icon(name, size="md", css_class=""):
    """Render a named SVG icon as HTML."""
    paths = _SVG.get(name)
    if not paths:
        return ""

    size_class = f"ui-icon--{size}" if size else "ui-icon--md"
    extra = f" {css_class}" if css_class else ""
    return (
        f'<span class="ui-icon {size_class}{extra}" aria-hidden="true">'
        f'<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">'
        f"{paths}"
        f"</svg></span>"
    )


def rank_badge(index):
    """Return a numeric rank badge for ordered lists (replaces medal emojis)."""
    rank = index + 1
    cls = "rank-badge top" if rank <= 3 else "rank-badge"
    return f'<span class="{cls}">{rank}</span>'
