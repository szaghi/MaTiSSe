#!/usr/bin/env python
"""
columns.py, module definition of Columns class.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
# modules not in the standard library
from yattag import Doc
# MaTiSSe.py modules
from .box    import parse as box_parse
from .figure import parse as figure_parse
from .note   import parse as note_parse
from .table  import parse as table_parse
from ..utils.source_editor import __source_editor__ as seditor
from ..utils.source_editor import obfuscate_codeblocks as obfuscate
from ..utils.source_editor import illuminate_protected as illuminate
from ..utils.source_editor import tokenize as generic_tokenize
# global variables
# regular expressions
__recolumns__ = re.compile(r"(?P<columns>\$columns(?P<env>.*?)\$endcolumns)",re.DOTALL)
__recol__ = re.compile(r"(?P<column>\$column(\[(?P<options>.*?)\])*)",re.DOTALL)
# classes definition
class Columns(object):
  """
  Object for handling columns environment.

  The syntax is:

  $columns
  $column[width:30%;background:green;]
  the first column contents
  $column[width:60%;background:white;]
  the second column contents
  $column[width:10%;background:red;]
  the third column contents
  $endcolumns
  """
  def __init__(self,source=None):
    """
    Parameters
    ----------
    source : str, optional
      string (as single stream) containing the source

    Attributes
    ----------
    number : int
      columns number
    columns : list
      list of list containing contents and options [cont,opts] of columns
    """
    self.number   = 0
    self.columns  = []
    if source:
      self.get(source=source)
    return

  def __str__(self):
    string = []
    if self.number > 0:
      string.append('\nColumns number: '+str(self.number))
      for col,column in enumerate(self.columns):
        string.append('\nColumn('+str(col)+')[options='+str(column[1])+']')
    return ''.join(string)

  def get(self,source=''):
    """Method for getting box style data.

    Parameters
    ----------
    source : str, optional
      string (as single stream) containing the source
    """
    protected, obfuscate_source = obfuscate(source = source)
    columns = []
    for match in re.finditer(__recol__,obfuscate_source):
      columns.append([match.group('options'),match.start(),match.end()])
    if len(columns)>0:
      for col,column in enumerate(columns):
        if col < len(columns)-1:
          contents = obfuscate_source[column[2]+1:columns[col+1][1]]
        else:
          contents = obfuscate_source[column[2]+1:]
        self.columns.append([illuminate(source=contents,protected_contents=protected),column[0]])
    self.number = len(self.columns)
    return

  def to_html(self):
    """Method for inserting columns to the html doc."""
    if self.number > 0:
      doc = Doc()
      with doc.tag('div',klass='columns'):
        for col,column in enumerate(self.columns):
          with doc.tag('div',klass='column'):
            doc.attr(('column-number',str(col+1)))
            style = 'display:block;float:left;'
            if column[1]:
              style += column[1]
            else:
              style += 'width:'+str(int(100.0/self.number))+'%;'
            doc.attr(style=style)
            content = box_parse(column[0])
            content = figure_parse(content)
            content = table_parse(content)
            content = note_parse(content)
            doc.asis(seditor.md_convert(content))
      return doc.getvalue()
    return ''

def tokenize(source):
  """Method for tokenizing source tagging columns environments.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source

  Returns
  -------
  list
    list of tokens whose elements are ['type',source_part]; type is 'columns' for columns environments and
    'unknown' for anything else
  """
  return generic_tokenize(source=source,re_part=__recolumns__,name_part='columns')

def parse(source):
  """Method for parsing source substituting boxes with their own html equivalent.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source

  Returns
  -------
  str
    source string parsed
  """
  protected, obfuscate_source = obfuscate(source=source)
  for match in re.finditer(__recolumns__, obfuscate_source):
    columns = Columns(source=illuminate(source=match.group('env'), protected_contents=protected))
    # obfuscate_source = re.sub(__recolumns__, lambda x: columns.to_html(), obfuscate_source, 1)
    obfuscate_source = re.sub(__recolumns__, columns.to_html(), obfuscate_source, 1)
  return illuminate(source=obfuscate_source, protected_contents=protected)
