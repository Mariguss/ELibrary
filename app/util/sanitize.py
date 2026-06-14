import bleach
import markdown as md

ALLOWED_TAGS = [
    "p", "br", "strong", "em", "b", "i", "u", "s", "blockquote",
    "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6",
    "a", "img", "code", "pre", "hr", "table", "thead", "tbody", "tr", "th", "td",
]
ALLOWED_ATTRS = {
    "a": ["href", "title"],
    "img": ["src", "alt", "title"],
}


def sanitize_html(text: str) -> str:
    """Удаляет потенциально опасные теги (script и т.п.)."""
    return bleach.clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)


def render_markdown(text: str) -> str:
    """Markdown -> HTML с последующей санитизацией."""
    html = md.markdown(text or "", extensions=["extra"])
    return sanitize_html(html)