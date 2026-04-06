#!/usr/bin/env python3
"""
theorem.py — Theorem, lemma, and proof environments (Phase 3 of issue #62).

Syntax::

    ::: {#thm-cauchy}
    ## Cauchy–Schwarz inequality
    $$|\\langle u, v\\rangle|^2 \\leq \\|u\\|^2 \\|v\\|^2$$
    :::

    ::: {.proof}
    By compactness of the unit sphere...
    $\\square$
    :::

    ::: {#def-lipschitz}
    ## Lipschitz continuity
    A function $f$ is $L$-Lipschitz if...
    :::

Supported prefixes (determine type and display label):
  thm → Theorem     lem → Lemma       cor → Corollary
  prp → Proposition def → Definition  exm → Example
  exr → Exercise    rem → Remark

The ``.proof`` type is unnumbered and ends with ∎.
"""

import re

from yattag import Doc

from .markdown_utils import markdown2html

# Human-readable labels per environment prefix.
_THEOREM_LABELS = {
    "thm": "Theorem",
    "lem": "Lemma",
    "cor": "Corollary",
    "prp": "Proposition",
    "def": "Definition",
    "exm": "Example",
    "exr": "Exercise",
    "rem": "Remark",
}

_THEOREM_PREFIXES = "|".join(_THEOREM_LABELS)


class Theorem:
    """Theorem-like environment with auto-numbering.

    Counters are class-level dicts keyed by prefix (``thm``, ``lem``, …).
    Call ``Theorem.reset()`` between presentations to clear all counters.
    """

    regexs = {
        "theorem": re.compile(
            rf":::[ \t]*\{{(?:#(?P<prefix>{_THEOREM_PREFIXES})-(?P<id>[^\s}}]+)|(?P<proof>\.proof))"
            r"(?P<extra>[^}]*)\}[ \t]*\n"
            r"(?:##[ \t]*(?P<title>[^\n]*)\n)?"
            r"(?P<content>.*?)"
            r"\n:::[ \t]*(?=\n|$)",
            re.DOTALL,
        )
    }

    # Per-prefix counters; shared across all instances in one presentation.
    _counters: dict = {}
    theorems_number: int = 0

    @classmethod
    def reset(cls):
        """Reset counters and instance count."""
        cls._counters = {}
        cls.theorems_number = 0

    def __init__(self, source=None):
        Theorem.theorems_number += 1
        self.number = Theorem.theorems_number
        self.prefix = None       # e.g. "thm"
        self.env_id = ""         # e.g. "cauchy"
        self.is_proof = False
        self.title = None
        self.content = ""
        self.env_number = None   # sequential number within prefix
        if source:
            self.get(source=source)

    def get(self, source):
        """Parse theorem block from *source*."""
        m = self.regexs["theorem"].search(source)
        if not m:
            return
        if m.group("proof"):
            self.is_proof = True
        else:
            self.prefix = m.group("prefix")
            self.env_id = m.group("id") or ""
            # Assign counter
            if self.prefix not in Theorem._counters:
                Theorem._counters[self.prefix] = 0
            Theorem._counters[self.prefix] += 1
            self.env_number = Theorem._counters[self.prefix]
        self.title = (m.group("title") or "").strip() or None
        self.content = (m.group("content") or "").strip()

    def to_html(self, backend="impress"):
        """Return the theorem HTML fragment."""
        doc = Doc()

        if self.is_proof:
            klass = "theorem theorem-proof"
            html_id = f"proof-{self.number}"
        else:
            klass = f"theorem theorem-{self.prefix}"
            html_id = f"{self.prefix}-{self.env_id}" if self.env_id else f"{self.prefix}-{self.env_number}"

        with doc.tag("div", klass=klass, id=html_id):
            if self.is_proof:
                with doc.tag("div", klass="theorem-header"):
                    doc.asis("<em>Proof.</em>")
            else:
                label = _THEOREM_LABELS.get(self.prefix, self.prefix.title())
                header_parts = [f"{label} {self.env_number}"]
                if self.title:
                    header_parts.append(f" ({self.title})")
                with doc.tag("div", klass="theorem-header"):
                    doc.asis(
                        f'<strong>{"".join(header_parts)}</strong>'
                    )
            with doc.tag("div", klass="theorem-body"):
                content_html = markdown2html(self.content)
                doc.asis(content_html)
                if self.is_proof:
                    # Append QED symbol if not already present
                    if "∎" not in self.content and "\\square" not in self.content:
                        doc.asis('<span class="qed">∎</span>')
        return doc.getvalue()
