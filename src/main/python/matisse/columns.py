#!/usr/bin/env python
"""
columns.py, module definition of Columns class.
"""
from __future__ import print_function
import re
from yattag import Doc
from markdown_utils import markdown2html


__recolumns__ = re.compile(r"(?P<columns>\$columns(?P<env>.*?)\$endcolumns)", re.DOTALL)
__recol__ = re.compile(r"(?P<column>\$column(\[(?P<options>.*?)\])*)", re.DOTALL)


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
  regexs = {"columns": re.compile(r"(?P<columns>\$columns(?P<env>.*?)\$endcolumns)", re.DOTALL),
            "column": re.compile(r"(?P<column>\$column(\[(?P<options>.*?)\])*)", re.DOTALL)}

  def __init__(self, source=None):
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
    self.number = 0
    self.columns = []
    if source:
      self.get(source=source)
    return

  def __str__(self):
    string = []
    if self.number > 0:
      string.append('\nColumns number: ' + str(self.number))
      for col, column in enumerate(self.columns):
        string.append('\nColumn(' + str(col) + ')[options=' + str(column[1]) + ']')
    return ''.join(string)

  def get(self, source):
    """Get columns data.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    match = re.search(Columns.regexs['columns'], source)
    if match:
      source_columns = match.group('env')
      columns = []
      for match_col in re.finditer(Columns.regexs['column'], source_columns):
        columns.append([match_col.group('options'), match_col.start(), match_col.end()])
      if len(columns) > 0:
        for col, column in enumerate(columns):
          if col < len(columns) - 1:
            contents = source_columns[column[2] + 1:columns[col + 1][1]]
          else:
            contents = source_columns[column[2] + 1:]
          self.columns.append([contents, column[0]])
      self.number = len(self.columns)
    return

  def to_html(self):
    """Convert self data to its html stream."""
    if self.number > 0:
      doc = Doc()
      with doc.tag('div', klass='columns'):
        for col, column in enumerate(self.columns):
          with doc.tag('div', klass='column'):
            doc.attr(('column-number', str(col + 1)))
            style = 'display:block;float:left;'
            if column[1]:
              style += column[1]
            else:
              style += 'width:' + str(int(100.0 / self.number)) + '%;'
            doc.attr(style=style)
            doc.asis(markdown2html(source=column[0]))
      return doc.getvalue()
    return ''
