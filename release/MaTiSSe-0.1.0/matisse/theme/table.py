#!/usr/bin/env python
"""
table.py, module definition of Table class.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
# modules not in the standard library
from yattag import Doc
# MaTiSSe.py modules
from ..utils.source_editor import __source_editor__ as seditor
from ..utils.source_editor import illuminate_protected as illuminate
from ..utils.source_editor import obfuscate_codeblocks as obfuscate
from ..utils.source_editor import tokenize as generic_tokenize
from .box import Box
from .theme_element import ThemeElement
# global variables
# regular expressions
__retable__ = re.compile(r"\$table(?P<env>.*?)\$endtable",re.DOTALL)
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

  @classmethod
  def reset(cls):
    """Method resetting Table to initial values."""
    cls.tables_number = 0
    cls.theme = ThemeElement(data_tag=r'theme_table')
    cls.theme.data.data['style'  ] = [None,False]
    cls.theme.data.data['caption'] = [None,False]
    cls.theme.data.data['content'] = [None,False]
    return

  def __init__(self,source=None):
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
    super(Table,self).__init__(ctn_type='table')
    self.cap_type = 'Table'
    Table.tables_number += 1
    self.number = Table.tables_number
    if source:
      self.get(source=source)
    return

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
        doc.asis(self.caption_txt())
    return

  def to_html(self):
    """Method for inserting box to the html doc."""
    doc = Doc()
    with doc.tag('div',klass='table'):
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
        doc.asis(seditor.md_convert(self.ctn))
    return doc.getvalue()

def tokenize(source):
  """Method for tokenizing source tagging tables environments.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source

  Returns
  -------
  list
    list of tokens whose elements are ['type',source_part]; type is 'table' for note environments and
    'unknown' for anything else
  """
  return generic_tokenize(source=source,re_part=__retable__,name_part='table')

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
  protected, obfuscate_source = obfuscate(source = source)
  for match in re.finditer(__retable__,obfuscate_source):
    table = Table(source=illuminate(source=match.group('env'),protected_contents=protected))
    obfuscate_source = re.sub(__retable__,table.to_html(),obfuscate_source,1)
  return illuminate(source=obfuscate_source,protected_contents=protected)
