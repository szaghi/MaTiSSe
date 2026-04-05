"""
Markdown Custom class extension for Python-Markdown
=========================================

Markdown extension that allows defining span element
with custom class for a given text. Usage:

    >>> import markdown
    >>> md = markdown.Markdown(extensions=['custom_span_class'])

    >>> md.convert('i love !!text-alert|spam!!')
    '<p>i love <span class="text-alert">spam</span></p>'

    >>> md.convert('i love !!|spam!!')
    '<p>i love !!|spam!!</p>'

    >>> md.convert('i love !!text-alert|!!')
    '<p>i love !!text-alert|!!</p>'

    >>> md.convert('i love !!   |spam!!')
    '<p>i love !!   |spam!!</p>'

copyright @2014 Konrad Wasowicz <exaroth@gmail.com>

"""

import xml.etree.ElementTree as etree

import markdown
from markdown import Extension
from markdown.inlinepatterns import InlineProcessor

CUSTOM_CLS_RE = r"[!]{2}(?P<class>.+)[|](?P<text>.+)[!]{2}"


class CustomSpanClassExtension(Extension):
    """Extension class for markdown"""

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            CustomSpanClassPattern(CUSTOM_CLS_RE, md),
            "custom_span_class",
            175,
        )


class CustomSpanClassPattern(InlineProcessor):
    def handleMatch(self, matched, data):
        """
        If string matched regexp expression create
        new span elem with given class.
        """
        cls = matched.group("class").strip()
        text = matched.group("text").strip()

        if not cls or not text:
            return None, None, None

        elem = etree.Element("span")
        elem.set("class", cls)
        elem.text = markdown.util.AtomicString(text)
        return elem, matched.start(0), matched.end(0)


def makeExtension(*args, **kwargs):
    return CustomSpanClassExtension(*args, **kwargs)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
