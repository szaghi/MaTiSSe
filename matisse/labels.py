#!/usr/bin/env python3
"""
labels.py — Label registry and cross-reference support (Phase 7a of issue #62).

Labels are collected during a first pass over all slide contents by
``Presentation.collect_labels()``.  The ``@PREFIX-id`` reference syntax is
then substituted during rendering via ``LabelRegistry.substitute_refs()``.

Supported prefixes and display strings:

    fig   → Figure
    tbl   → Table
    eq    → Equation
    sec   → Section
    thm   → Theorem
    lem   → Lemma
    cor   → Corollary
    prp   → Proposition
    def   → Definition
    exm   → Example
    exr   → Exercise
    rem   → Remark
    dia   → Diagram
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_KIND_LABELS = {
    "fig": "Figure",
    "tbl": "Table",
    "eq":  "Equation",
    "sec": "Section",
    "thm": "Theorem",
    "lem": "Lemma",
    "cor": "Corollary",
    "prp": "Proposition",
    "def": "Definition",
    "exm": "Example",
    "exr": "Exercise",
    "rem": "Remark",
    "dia": "Diagram",
}

_ALL_PREFIXES = "|".join(sorted(_KIND_LABELS, key=len, reverse=True))

# Regex that detects ``{#PREFIX-id}`` attribute blocks in raw Markdown source.
_LABEL_RE = re.compile(
    rf"\{{#(?P<prefix>{_ALL_PREFIXES})-(?P<id>[^\s}}]+)[^}}]*\}}"
)

# Regex that detects ``@PREFIX-id`` reference tokens in HTML/Markdown.
_REF_RE = re.compile(
    rf"@(?P<prefix>{_ALL_PREFIXES})-(?P<id>[^\s,;.!?\"')\]}}]+)"
)


@dataclass
class LabelEntry:
    """One registered label."""

    label: str          # full label, e.g. "fig-results"
    kind: str           # prefix, e.g. "fig"
    number: int         # sequential number within this kind
    html_id: str        # HTML element id used for the ``<a href>`` link


class LabelRegistry:
    """Collects labels during a pre-pass and resolves ``@label`` references.

    Usage::

        registry = LabelRegistry()
        registry.collect_from_source(slide.contents)
        ...
        html = registry.substitute_refs(html)
    """

    def __init__(self):
        self._entries: dict[str, LabelEntry] = {}
        self._counters: dict[str, int] = {}

    def register(self, prefix: str, label_id: str) -> LabelEntry:
        """Register *prefix*-*label_id* and return the assigned entry.

        If the label was already registered the existing entry is returned
        unchanged (idempotent).
        """
        full = f"{prefix}-{label_id}"
        if full in self._entries:
            return self._entries[full]
        self._counters.setdefault(prefix, 0)
        self._counters[prefix] += 1
        entry = LabelEntry(
            label=full,
            kind=prefix,
            number=self._counters[prefix],
            html_id=full,
        )
        self._entries[full] = entry
        return entry

    def resolve(self, label: str) -> str:
        """Return the human-readable reference string for *label*.

        Returns e.g. ``"Figure 2"`` for ``"fig-results"``.  If the label is
        not registered, returns ``"??"`` and prints a warning.
        """
        if label in self._entries:
            entry = self._entries[label]
            kind_label = _KIND_LABELS.get(entry.kind, entry.kind.title())
            return f"{kind_label} {entry.number}"
        print(f"Warning: unresolved cross-reference '@{label}'")
        return "??"

    def collect_from_source(self, source: str) -> None:
        """Scan *source* for ``{#PREFIX-id}`` labels and register them."""
        for m in _LABEL_RE.finditer(source):
            self.register(m.group("prefix"), m.group("id"))

    def substitute_refs(self, html: str) -> str:
        """Replace ``@PREFIX-id`` tokens in *html* with hyperlinks.

        Tokens that are NOT registered produce a ``??`` link with a warning.
        """

        def _replace(m: re.Match) -> str:
            full = f"{m.group('prefix')}-{m.group('id')}"
            text = self.resolve(full)
            return f'<a href="#{full}" class="cross-ref">{text}</a>'

        return _REF_RE.sub(_replace, html)
