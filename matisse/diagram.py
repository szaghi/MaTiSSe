#!/usr/bin/env python3
"""
diagram.py — Mermaid and Graphviz diagram environments (Phase 2 of issue #62).

Syntax::

    ```{mermaid}
    %%| fig-cap: "Build pipeline"
    flowchart LR
      A[Source] --> B{Parser} --> C[HTML]
    ```

    ```{dot}
    %%| fig-cap: "Module dependencies"
    digraph G { matisse -> parser; matisse -> theme; }
    ```

For Mermaid diagrams the presenter must include the Mermaid CDN script in the
page (see ``ImpressBackend`` / ``RevealBackend`` for injection logic).  For
Graphviz / dot diagrams, d3-graphviz is used.

Set ``Diagram.has_mermaid`` or ``Diagram.has_graphviz`` to detect at render
time whether the CDN scripts are needed (both are class-level flags reset by
``Diagram.reset()``).
"""

import re

from yattag import Doc

# CDN script snippets (injected by renderers when the flags are set)
MERMAID_CDN_SCRIPT = """\
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true });
</script>"""

GRAPHVIZ_CDN_SCRIPTS = """\
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@hpcc-js/wasm-graphviz/dist/graphviz.umd.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3-graphviz@5/build/d3-graphviz.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.graphviz').forEach(function(el) {
      d3.select(el).graphviz().renderDot(el.textContent.trim());
    });
  });
</script>"""


class Diagram:
    """Mermaid or Graphviz/dot diagram block.

    Recognises fenced code blocks whose info string is ``{mermaid}`` or
    ``{dot}``.  An optional ``%%| fig-cap:`` first-line annotation is stripped
    from the source before rendering.

    Class-level flags ``has_mermaid`` and ``has_graphviz`` are set whenever a
    diagram of the respective type is instantiated; they are checked by
    renderers to decide whether to inject CDN scripts.
    """

    regexs = {
        "diagram": re.compile(
            r"```\{(?P<engine>mermaid|dot)\}[ \t]*\n"
            r"(?:%%\|[ \t]*fig-cap:[ \t]*['\"]?(?P<caption>[^\n'\"]*)['\"]?[ \t]*\n)?"
            r"(?P<source>.*?)```",
            re.DOTALL,
        )
    }
    has_mermaid: bool = False
    has_graphviz: bool = False
    diagrams_number: int = 0

    @classmethod
    def reset(cls):
        """Reset to default state."""
        cls.diagrams_number = 0
        cls.has_mermaid = False
        cls.has_graphviz = False

    def __init__(self, source=None):
        Diagram.diagrams_number += 1
        self.number = Diagram.diagrams_number
        self.engine = "mermaid"
        self.caption = ""
        self.source = ""
        if source:
            self.get(source=source)

    def get(self, source):
        """Parse diagram block from *source*."""
        m = self.regexs["diagram"].search(source)
        if not m:
            return
        self.engine = m.group("engine")
        self.caption = (m.group("caption") or "").strip()
        self.source = (m.group("source") or "").strip()
        # Update class-level flags
        if self.engine == "mermaid":
            Diagram.has_mermaid = True
        else:
            Diagram.has_graphviz = True

    def to_html(self, backend="impress"):
        """Return the diagram HTML fragment."""
        doc = Doc()
        with doc.tag("figure", klass=f"diagram diagram-{self.engine}", id=f"diagram-{self.number}"):
            if self.engine == "mermaid":
                with doc.tag("pre", klass="mermaid"):
                    doc.text(self.source)
            else:
                with doc.tag("div", klass="graphviz"):
                    doc.text(self.source)
            if self.caption:
                with doc.tag("figcaption"):
                    doc.text(self.caption)
        return doc.getvalue()
