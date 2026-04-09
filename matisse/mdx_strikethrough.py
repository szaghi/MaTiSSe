"""
Strikethrough markdown extension for Python-Markdown.

Converts ``~~text~~`` to ``<del>text</del>``.
"""

import xml.etree.ElementTree as etree

import markdown
from markdown.inlinepatterns import InlineProcessor


class StrikethroughProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element("del")
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class StrikethroughExtension(markdown.Extension):
    def extendMarkdown(self, md):
        # Priority 172 — above subscript (166) so ~~text~~ is consumed before ~text~
        md.inlinePatterns.register(
            StrikethroughProcessor(r"~~(.+?)~~", md),
            "strikethrough",
            172,
        )


def makeExtension(**kwargs):
    return StrikethroughExtension(**kwargs)
