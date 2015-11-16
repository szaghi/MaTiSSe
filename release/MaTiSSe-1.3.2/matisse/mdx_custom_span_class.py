"""
Markdown Custom class extension for Python-Markdown
=========================================

Markdown extension that allows defining span element
with custom class for a given text. Usage:

    >>> import markdown
    >>> md = markdown.Markdown(extensions=['custom_span_class'])

    >>> md.convert('i love !!text-alert|spam!!')
    u'<p>i love <span class="text-alert">spam</span></p>'

    >>> md.convert('i love !!|spam!!')
    u'<p>i love !!|spam!!</p>'

    >>> md.convert('i love !!text-alert|!!')
    u'<p>i love !!text-alert|!!</p>'

    >>> md.convert('i love !!   |spam!!')
    u'<p>i love !!   |spam!!</p>'

copyright @2014 Konrad Wasowicz <exaroth@gmail.com>

"""


from __future__ import absolute_import
from __future__ import unicode_literals
import markdown
from markdown import Extension
from markdown.inlinepatterns import Pattern


CUSTOM_CLS_RE = r'[!]{2}(?P<class>.+)[|](?P<text>.+)[!]{2}'


class CustomSpanClassExtension(Extension):
  """ Extension class for markdown """
  def extendMarkdown(self, md, md_globals):
    md.inlinePatterns["custom_span_class"] = CustomSpanClassPattern(CUSTOM_CLS_RE, md)


class CustomSpanClassPattern(Pattern):
  def handleMatch(self, matched):

    """
    If string matched
    regexp expression create
    new span elem with given class
    """

    cls = matched.group("class")
    text = matched.group("text")

    elem = markdown.util.etree.Element("span")
    elem.set("class", cls)
    elem.text = markdown.util.AtomicString(text)
    return elem


def makeExtension(*args, **kwargs):
  return CustomSpanClassExtension(*args, **kwargs)

if __name__ == "__main__":
  import doctest
  doctest.testmod()
