"""
Quarto-style inline span extension for Python-Markdown.

Converts ``[text]{attrs}`` to a ``<span>`` element with the given
classes and/or attributes, mirroring Quarto's span syntax.

Supported attribute forms inside ``{...}``:
  ``.classname``      → added to the ``class`` attribute
  ``key="value"``     → set as an HTML attribute
  ``key=value``       → set as an HTML attribute (unquoted value)
  ``#id``             → sets the ``id`` attribute

Examples::

  [underlined text]{.underline}   → <span class="underline">underlined text</span>
  [highlighted]{.mark}            → <span class="mark">highlighted</span>
  [CAPS]{.smallcaps}              → <span class="smallcaps">CAPS</span>
  [note]{.myclass #fn1}           → <span class="myclass" id="fn1">note</span>
"""

import re
import xml.etree.ElementTree as etree

import markdown
from markdown.inlinepatterns import InlineProcessor

# Matches [text]{attrs} — text must be non-empty; attrs block is non-empty
_PATTERN = r"\[(?P<text>[^\[\]]+)\]\{(?P<attrs>[^}]+)\}"

_RE_CLASS = re.compile(r"\.([A-Za-z][\w-]*)")
_RE_ID = re.compile(r"#([A-Za-z][\w-]*)")
_RE_KV_QUOTED = re.compile(r'([\w-]+)=["\']([^"\']*)["\']')
_RE_KV_BARE = re.compile(r"([\w-]+)=([^\s}\"\']+)")


def _parse_attrs(raw: str) -> dict:
    """Parse a Quarto/Pandoc attribute string into a dict suitable for etree."""
    attrs: dict = {}

    classes = _RE_CLASS.findall(raw)
    if classes:
        attrs["class"] = " ".join(classes)

    id_match = _RE_ID.search(raw)
    if id_match:
        attrs["id"] = id_match.group(1)

    # Remove class/id tokens before parsing key=value pairs to avoid false matches
    cleaned = _RE_CLASS.sub("", raw)
    cleaned = _RE_ID.sub("", cleaned)

    for key, val in _RE_KV_QUOTED.findall(cleaned):
        attrs[key] = val
    for key, val in _RE_KV_BARE.findall(cleaned):
        if key not in attrs:
            attrs[key] = val

    return attrs


class QuartoSpanProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        attrs = _parse_attrs(m.group("attrs"))
        if not attrs:
            return None, None, None
        el = etree.Element("span")
        for key, val in attrs.items():
            el.set(key, val)
        el.text = m.group("text")
        return el, m.start(0), m.end(0)


class QuartoSpanExtension(markdown.Extension):
    def extendMarkdown(self, md):
        # Priority 155 — below all other inline formatters but above default link (160)
        # We want links [text](url) to win over spans [text]{attrs} at the same pos,
        # so use priority just below superscript (167).
        md.inlinePatterns.register(
            QuartoSpanProcessor(_PATTERN, md),
            "quarto_span",
            155,
        )


def makeExtension(**kwargs):
    return QuartoSpanExtension(**kwargs)
