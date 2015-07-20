#!/usr/bin/env python
"""
markdown_utils.py, module definition of markdown utils functions.
"""
import markdown
from mdx_mathjax import MathJaxExtension
from mdx_custom_span_class import CustomSpanClassExtension
try:
  from markdown_checklist.extension import ChecklistExtension
  __mdx_checklist__ = True
except ImportError:
  __mdx_checklist__ = False


def markdown2html(source, no_p=False):
  """Convert markdown source to html.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source
  no_p : bool, optional
    if True the converted contents is not inserted into the <p></p> tags

  Returns
  -------
  str
    converted source
  """
  if __mdx_checklist__:
    mkd = markdown.Markdown(output_format='html5',
                            extensions=['smarty',
                                        'extra',
                                        CustomSpanClassExtension(),
                                        ChecklistExtension(),
                                        MathJaxExtension()])
  else:
    mkd = markdown.Markdown(output_format='html5',
                            extensions=['smarty',
                                        'extra',
                                        MathJaxExtension()])
  markup = mkd.reset().convert(source)
  if no_p:
    p_start = '<p>'
    p_end = '</p>'
    if markup.startswith(p_start) and markup.endswith(p_end):
      markup = markup[len(p_start):-len(p_end)]
  return markup
