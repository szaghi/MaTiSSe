#!/usr/bin/env python
"""
table.py, module definition of Table class.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
import sys
# modules not in the standard library
try:
  from yattag import Doc
except ImportError :
  sys.stderr.write("Error: can't import module 'yattag'")
  sys.exit(1)
# MaTiSSe.py modules
from .box import Box
from .theme_element import ThemeElement
# global variables
# regular expressions
__retable__ = re.compile(r"\$table(?P<box>.*?)\$endtable",re.DOTALL)
# classes definition
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
  2. no matter the order of $caption / $content statements, the caption is always placed above the content;

  Attributes
  ----------
  tables_number : int
    global number of tables (equals to the number of Table instances)
  theme: ThemeElement object
    global theme of Table boxes
  """
  tables_number = 0
  theme = ThemeElement(data_tag=r'theme_table')
  theme.data.data['style'  ] = [None,False]
  theme.data.data['caption'] = [None,False]
  theme.data.data['content'] = [None,False]

  def __init__(self):
    """
    Attributes
    ----------
    number : int
      number of table
    """
    super(Table,self).__init__(ctn_type='table')
    self.cap_type = 'Table'
    Table.tables_number += 1
    self.number = Table.tables_number

  @classmethod
  def get_theme(cls,source):
    """Method for getting theme definition table boxes.

    The syntax is:

    ---theme_table
    style   = style_options
    caption = caption_options
    content = content_options
    ---endtheme_table

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    cls.theme.get(source=source)
    return

  @classmethod
  def strip_theme(cls,source):
    """Method for striping theme data from source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      source without the themes data
    """
    return cls.theme.strip(source=source)

  def put_caption(self,doc):
    """Method for inserting caption into doc.

    Parameters
    ----------
    doc : yattag.Doc object
      yattag document where to put caption
    """
    if self.cap or self.cap_type:
      with doc.tag('div',klass='table caption'):
        if self.cap_options:
          doc.attr(style=self.cap_options)
        elif Table.theme.data.data['caption'][0]:
          doc.attr(style=Table.theme.data.data['caption'][0])
        doc.text(self.caption_txt())
    return

  def to_html(self):
    """Method for inserting box to the html doc."""
    doc = Doc()
    with doc.tag('div',markdown='1',klass='table'):
      if self.style:
        doc.attr(style=self.style)
      elif Table.theme.data.data['style'][0]:
        doc.attr(style=Table.theme.data.data['style'][0])
      self.put_caption(doc=doc)
      with doc.tag('div',klass='table content'):
        if self.ctn_options:
          doc.attr(style=self.ctn_options)
        elif Table.theme.data.data['content'][0]:
          doc.attr(style=Table.theme.data.data['content'][0])
        doc.text(self.ctn)
    return doc.getvalue()

def parse(source):
  """Method for parsing source substituting figures with their own html equivalent.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source

  Returns
  -------
  str
    source string parsed
  """
  parsed_source = source
  for match in re.finditer(__retable__,parsed_source):
    table = Table()
    table.get(source=match.group('box'))
    parsed_source = re.sub(__retable__,table.to_html(),parsed_source,1)
  return parsed_source
