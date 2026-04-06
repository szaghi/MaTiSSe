#!/usr/bin/env python3
"""
callout.py — Callout block environments (Phase 1 of issue #62).

Syntax::

    ::: {.callout-note}
    ## Optional title
    Content here.
    :::

    ::: {.callout-warning title="Be careful"}
    This will overwrite your data.
    :::

Supported types: note, tip, warning, caution, important.
"""

import re

from yattag import Doc

from .markdown_utils import markdown2html

# Left-border colours per callout type (applied inline as CSS variables).
_CALLOUT_COLORS = {
    "note": "#0070c0",
    "tip": "#2e8b57",
    "warning": "#e69500",
    "caution": "#cc0000",
    "important": "#7b2d8b",
}

_CALLOUT_ICONS = {
    "note": "ℹ",
    "tip": "💡",
    "warning": "⚠",
    "caution": "🔴",
    "important": "❗",
}


class Callout:
    """Semantic callout block (note / tip / warning / caution / important).

    Fenced-div syntax::

        ::: {.callout-TYPE}
        ## Optional heading
        Body content (Markdown).
        :::

        ::: {.callout-TYPE title="Inline title"}
        Body content.
        :::
    """

    TYPES = ("note", "tip", "warning", "caution", "important")

    regexs = {
        "callout": re.compile(
            r":::[ \t]*\{\.callout-(?P<ctype>note|tip|warning|caution|important)"
            r"(?P<extra>[^}]*)\}[ \t]*\n"
            r"(?P<content>.*?)"
            r"\n:::[ \t]*(?=\n|$)",
            re.DOTALL,
        )
    }
    callouts_number = 0

    @classmethod
    def reset(cls):
        """Reset to default state."""
        cls.callouts_number = 0

    def __init__(self, source=None):
        Callout.callouts_number += 1
        self.number = Callout.callouts_number
        self.ctype = "note"
        self.title = None
        self.content = ""
        if source:
            self.get(source=source)

    def get(self, source):
        """Parse callout block from *source*."""
        m = self.regexs["callout"].search(source)
        if not m:
            return
        self.ctype = m.group("ctype")
        extra = m.group("extra") or ""
        # Title from inline attr: title="..." or title='...'
        tm = re.search(r'title=["\']([^"\']*)["\']', extra)
        if tm:
            self.title = tm.group(1)
        content = m.group("content").strip()
        # Title from first ## heading inside the block
        hm = re.match(r"##[ \t]+(?P<h>[^\n]+)\n?", content)
        if hm:
            if self.title is None:
                self.title = hm.group("h").strip()
            content = content[hm.end() :].strip()
        self.content = content

    def to_html(self, backend="impress"):
        """Return the callout HTML fragment."""
        color = _CALLOUT_COLORS.get(self.ctype, "#666")
        icon = _CALLOUT_ICONS.get(self.ctype, "")
        title_text = self.title if self.title is not None else self.ctype.title()
        doc = Doc()
        with doc.tag(
            "div",
            klass=f"callout callout-{self.ctype}",
            id=f"callout-{self.number}",
            style=f"border-left: 4px solid {color};",
        ):
            with doc.tag("div", klass="callout-title"):
                doc.asis(f'<span class="callout-icon">{icon}</span> {title_text}')
            with doc.tag("div", klass="callout-body"):
                doc.asis(markdown2html(self.content))
        return doc.getvalue()
