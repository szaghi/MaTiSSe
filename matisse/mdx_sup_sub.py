"""
Superscript and subscript markdown extension for Python-Markdown.

Converts:
  ``^text^``  →  ``<sup>text</sup>``
  ``~text~``  →  ``<sub>text</sub>``

Priority ordering keeps strikethrough (172) ahead of subscript (166) so that
``~~del~~`` is consumed before the single-tilde subscript pattern can see it.
MathJax runs at 185, so ``^`` and ``~`` inside ``$...$`` are never touched.
"""

import xml.etree.ElementTree as etree

import markdown
from markdown.inlinepatterns import InlineProcessor


class SuperscriptProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element("sup")
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class SubscriptProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element("sub")
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class SupSubExtension(markdown.Extension):
    def extendMarkdown(self, md):
        # Superscript: ^text^ — [^^]+ avoids matching across caret pairs
        md.inlinePatterns.register(
            SuperscriptProcessor(r"\^([^\^]+)\^", md),
            "superscript",
            167,
        )
        # Subscript: ~text~ — [^~]+ avoids matching double-tilde (strikethrough)
        md.inlinePatterns.register(
            SubscriptProcessor(r"~([^~]+)~", md),
            "subscript",
            166,
        )


def makeExtension(**kwargs):
    return SupSubExtension(**kwargs)
