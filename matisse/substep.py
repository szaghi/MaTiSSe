#!/usr/bin/env python3
"""
substep.py — Substep environment for the impress.js Substep plugin.

Elements wrapped in a ``$substep`` / ``$endsubstep`` block are emitted
with ``class="substep"`` so that the impress.js Substep plugin reveals
them one at a time as the presenter presses the forward key.

Syntax::

    $substep
    Content revealed at step N.
    $endsubstep

    $substep[order:1]
    Appears together with other order-1 substeps.
    $endsubstep
"""

import re

from yattag import Doc

from .markdown_utils import markdown2html


class Substep:
    """
    Object for handling incremental-reveal substep blocks.

    The impress.js Substep plugin hides elements with ``class="substep"``
    initially and reveals them one at a time on forward navigation.  An
    optional ``data-substep-order`` attribute groups substeps that should
    appear simultaneously.
    """

    regexs = {
        "substep": re.compile(
            r"(?P<substep>\$substep(?:\[(?P<options>[^\]]*)\])?\n?(?P<env>.*?)\$endsubstep)",
            re.DOTALL,
        )
    }
    substeps_number = 0

    @classmethod
    def reset(cls):
        """Reset to default state."""
        cls.substeps_number = 0

    def __init__(self, source=None):
        Substep.substeps_number += 1
        self.number = Substep.substeps_number
        self.content = ""
        self.order = None
        if source:
            self.get(source=source)

    def get(self, source):
        """Parse substep block from *source*."""
        match = self.regexs["substep"].search(source)
        if match:
            options = match.group("options")
            if options:
                m = re.search(r"order\s*:\s*(\d+)", options)
                if m:
                    self.order = int(m.group(1))
            self.content = (match.group("env") or "").strip()

    def to_html(self):
        """Return the substep HTML fragment."""
        doc = Doc()
        with doc.tag("div", klass="substep"):
            if self.order is not None:
                doc.attr(("data-substep-order", str(self.order)))
            doc.asis(markdown2html(self.content))
        return doc.getvalue()
