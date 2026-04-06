#!/usr/bin/env python3
"""
figure_group.py — Subfigure layout environment (Phase 6 of issue #62).

Syntax::

    ::: {#fig-comparison layout-ncol=2}

    $figure
    $source[width:100%]{images/before.png}
    $caption{Before treatment}
    $endfigure

    $figure
    $source[width:100%]{images/after.png}
    $caption{After treatment}
    $endfigure

    Comparison of cell morphology before and after treatment.
    :::

The optional ``layout="[[60,40],[100]]"`` attribute specifies explicit
percentage widths per row.  Each row is a JSON-style list of percentages.

The last paragraph inside the fenced div becomes the group caption; each
``$figure`` inside receives a sub-label: (a), (b), (c), …
"""

import json
import re

from yattag import Doc

from .figure import Figure

_SUBLABELS = "abcdefghijklmnopqrstuvwxyz"


class FigureGroup:
    """A group of figures arranged in a CSS-Grid layout with sub-labels."""

    regexs = {
        "figure_group": re.compile(
            r":::[ \t]*\{#(?P<gid>fig-[^\s}]+)(?P<extra>[^}]*)\}[ \t]*\n"
            r"(?P<content>.*?)"
            r"\n:::[ \t]*(?=\n|$)",
            re.DOTALL,
        )
    }
    groups_number: int = 0

    @classmethod
    def reset(cls):
        """Reset to default state."""
        cls.groups_number = 0

    def __init__(self, source=None):
        FigureGroup.groups_number += 1
        self.number = FigureGroup.groups_number
        self.gid = ""
        self.ncol: int = 1
        self.layout: list | None = None  # [[60,40],[100]] style
        self.figures: list[Figure] = []
        self.group_caption = ""
        if source:
            self.get(source=source)

    def get(self, source):
        """Parse figure group from *source*."""
        m = self.regexs["figure_group"].search(source)
        if not m:
            return
        self.gid = m.group("gid")
        extra = m.group("extra") or ""
        # layout-ncol=N
        ncol_m = re.search(r"layout-ncol\s*=\s*(\d+)", extra)
        if ncol_m:
            self.ncol = int(ncol_m.group(1))
        # layout="[[...]]"
        lay_m = re.search(r'layout\s*=\s*["\'](\[\[.*?\]\])["\']', extra)
        if lay_m:
            try:
                self.layout = json.loads(lay_m.group(1))
            except (ValueError, TypeError):
                pass
        content = m.group("content").strip()
        # Extract nested $figure blocks
        fig_re = Figure.regexs["figure"]
        fig_sources = []
        last_end = 0
        rest_parts = []
        for fm in fig_re.finditer(content):
            rest_parts.append(content[last_end : fm.start()])
            fig_sources.append(fm.group(0))
            last_end = fm.end()
        rest_parts.append(content[last_end:])
        # The remaining text (non-figure) is the group caption
        remainder = "".join(rest_parts).strip()
        # Last non-empty paragraph is the caption
        paras = [p.strip() for p in re.split(r"\n\s*\n", remainder) if p.strip()]
        self.group_caption = paras[-1] if paras else ""
        # Parse figures
        for fs in fig_sources:
            self.figures.append(Figure(source=fs))

    def _grid_css(self) -> str:
        """Return CSS ``grid-template-columns`` value."""
        if self.layout:
            # Use first row of the explicit layout
            row = self.layout[0]
            return " ".join(f"{w}%" for w in row)
        return f"repeat({self.ncol}, 1fr)"

    def to_html(self, backend="impress"):
        """Return the figure group HTML fragment."""
        doc = Doc()
        grid_cols = self._grid_css()
        with doc.tag(
            "figure",
            klass="figure-group",
            id=self.gid,
            style=f"display:grid; grid-template-columns:{grid_cols}; gap:1em;",
        ):
            for i, fig in enumerate(self.figures):
                label = f"({_SUBLABELS[i]})" if i < len(_SUBLABELS) else f"({i + 1})"
                fig_html = fig.to_html()
                # Inject the sub-label before the figure HTML
                with doc.tag("div", klass="subfigure"):
                    doc.asis(fig_html)
                    with doc.tag("span", klass="subfig-label"):
                        doc.text(label)
            if self.group_caption:
                with doc.tag("figcaption", klass="fig-group-caption"):
                    doc.text(self.group_caption)
        return doc.getvalue()
