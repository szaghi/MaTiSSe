#!/usr/bin/env python
"""
columns.py, module definition of Columns class.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
# modules not in the standard library
from yattag import Doc,indent
# MaTiSSe.py modules
from ..config import __config__
from ..utils.source_editor import obfuscate_codeblocks as obfuscate
from ..utils.source_editor import illuminate_protected as illuminate
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
      with doc.tag('div',klass='columns',markdown='1'):
        for col,column in enumerate(self.columns):
          with doc.tag('div',klass='column',markdown='1'):
            doc.attr(('column-number',str(col+1)))
            style = 'display:block;float:left;'
            if column[1]:
              style += column[1]
            doc.attr(style=style)
            doc.asis(column[0])
      return doc.getvalue()
    return ''

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
  protected, obfuscate_source = obfuscate(source = source)
  matches = []
  for match in re.finditer(__recolumns__,obfuscate_source):
    matches.append([match.start(),match.end(),illuminate(source=match.group('env'),protected_contents=protected)])
  if len(matches)>0:
    parsed_source = ''
    for mtc,match in enumerate(matches):
      columns = Columns(source=match[2])
      if mtc == 0:
        start = 0
      else:
        start = matches[mtc-1][1]+1
      if match[0]!=start:
        if __config__.indented:
          parsed_source += obfuscate_source[start:match[0]-1] + indent(columns.to_html())
        else:
          parsed_source += obfuscate_source[start:match[0]-1] + columns.to_html()
    if matches[-1][1]<len(obfuscate_source):
      parsed_source += obfuscate_source[matches[-1][1]+1:]
    return illuminate(source=parsed_source,protected_contents=protected)
  else:
    return source
