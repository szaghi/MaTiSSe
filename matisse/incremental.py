#!/usr/bin/env python3
"""
incremental.py — Incremental list environment (Phase 4 of issue #62).

Syntax::

    ::: {.incremental}
    - First item revealed alone
    - Then this one
    - Then this
    :::

Each list item gets ``class="fragment"`` (reveal.js) or ``class="substep"``
(impress.js) so the presenter reveals them one at a time.

Also see the ``PAUSE_RE`` constant exported from this module: it matches the
`` . . . `` paragraph-pause token used to split slide content into fragments.
"""

import re

from yattag import Doc

from .markdown_utils import markdown2html

# A standalone ". . ." line (may have surrounding whitespace / blank lines).
PAUSE_RE = re.compile(r"(?:^|\n)[ \t]*\. \. \.[ \t]*(?=\n|$)")


class IncrementalList:
    """A ``{.incremental}`` fenced list whose items are revealed one at a time."""

    regexs = {
        "incremental": re.compile(
            r":::[ \t]*\{\.incremental\}[ \t]*\n"
            r"(?P<content>.*?)"
            r"\n:::[ \t]*(?=\n|$)",
            re.DOTALL,
        )
    }
    incremental_number: int = 0

    @classmethod
    def reset(cls):
        """Reset to default state."""
        cls.incremental_number = 0

    def __init__(self, source=None):
        IncrementalList.incremental_number += 1
        self.number = IncrementalList.incremental_number
        self.items: list[str] = []
        if source:
            self.get(source=source)

    def get(self, source):
        """Parse incremental list from *source*."""
        m = self.regexs["incremental"].search(source)
        if not m:
            return
        content = m.group("content").strip()
        # Split on list-item markers ("- " at line start)
        raw_items = re.split(r"(?:^|\n)(?:[-*][ \t]+)", content)
        self.items = [it.strip() for it in raw_items if it.strip()]

    def to_html(self, backend="impress"):
        """Return the incremental list HTML.

        Each ``<li>`` receives ``class="fragment"`` for reveal.js or
        ``class="substep"`` for impress.js.
        """
        item_class = "fragment" if backend == "reveal" else "substep"
        doc = Doc()
        with doc.tag("ul", klass=f"incremental-list"):
            for item in self.items:
                with doc.tag("li", klass=item_class):
                    doc.asis(markdown2html(item, no_p=True))
        return doc.getvalue()
