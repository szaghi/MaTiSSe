"""
MathJax markdown extension.
"""
import xml.etree.ElementTree as etree

import markdown


class MathJaxInlineProcessor(markdown.inlinepatterns.InlineProcessor):
  """Match $...$ and $$...$$ delimiters and wrap them in a <mathjax> element."""

  def handleMatch(self, m, data):
    node = etree.Element('mathjax')
    node.text = markdown.util.AtomicString(m.group(1) + m.group(2) + m.group(1))
    return node, m.start(0), m.end(0)


class MathJaxExtension(markdown.Extension):
  def extendMarkdown(self, md):
    # Priority 185 > escape (180) so backslashes in LaTeX are not pre-consumed.
    md.inlinePatterns.register(
      MathJaxInlineProcessor(r'(?<!\\)(\$\$?)(.+?)\1', md),
      'mathjax',
      185,
    )


def makeExtension(configs=[]):
  return MathJaxExtension(configs)
