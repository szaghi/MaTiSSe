#!/usr/bin/env python
"""
table.py, module definition of Table class.
"""
import re
from yattag import Doc
from box import Box
from markdown_utils import markdown2html


class Table(Box):
  """
  Object for handling table-box. It is a subclass of Box.

  The syntax is:

  $table
  $style[style_options]
  $caption[caption_options]{caption}
  $content[content_options]{content}
  $endtable

  Note that differently from Box class:
  1. the "content_type" and "caption_type" are automatically set to "table" and "Table" respectively; anyhow they can be still
     specified inside the $table/$endtable environment;
  2. the "caption" is at top by default, but it can be also positionated at the bottom.

  Attributes
  ----------
  tables_number : int
    global number of tables (equals to the number of Table instances)
  """
  regexs = {'table': re.compile(r"\$table(?P<env>.*?)\$endtable", re.DOTALL)}
  tables_number = 0

  @classmethod
  def reset(cls):
    """Reset to default state."""
    cls.tables_number = 0
    return

  def __init__(self, source=None):
    """
    Parameters
    ----------
    source : str, optional
      string (as single stream) containing the source

    Attributes
    ----------
    number : int
      number of table
    """
    super(Table, self).__init__(ctn_type='table')
    self.cap_type = 'Table'
    Table.tables_number += 1
    self.number = Table.tables_number
    if source:
      self.get(source=source)
    return

  def to_html(self):
    """Convert self data to its html stream."""
    doc = Doc()
    with doc.tag('div', id='table-' + str(self.number)):
      if self.style:
        doc.attr(style=self.style)
      else:
        doc.attr(klass='table')
      if self.cap_position is None or self.cap_position.upper() == 'TOP':
        self.put_caption(doc=doc, klass='table-caption')
      with doc.tag('div', klass='table-content'):
        if self.ctn_options:
          doc.attr(style=self.ctn_options)
        doc.asis(markdown2html(self.ctn, no_p=True))
      if self.cap_position is not None and self.cap_position.upper() == 'BOTTOM':
        self.put_caption(doc=doc, klass='table-caption')
    return doc.getvalue()
