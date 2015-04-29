#!/usr/bin/env python
"""
metadata.py, module definition of Metadata class.
This defines the presentation metadata object.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import ast
import re
# modules not in the standard library
from yattag import Doc
# MaTiSSe.py modules
from ..data.data import Data
from ..utils.source_editor import __source_editor__ as seditor
from ..utils.source_editor import obfuscate_codeblocks as obfuscate
from ..utils.source_editor import illuminate_protected as illuminate
# class definition
class Metadata(object):
  """
  Object for handling the presentation metadata.
  """
  def __init__(self,source=None):
    """
    Parameters
    ----------
    source : str, optional
      string (as single stream) containing the source

    Attributes
    ----------
    data : Data object
      presentation metadata

    >>> source = '---metadata max_time = 60 ---endmetadata'
    >>> meta = Metadata(source)
    >>> meta.data.data['max_time'][0]
    '60'
    """
    _skip = [seditor.regex_codeblock,seditor.regex_codeinline]
    self.data = Data(regex_start='[-]{3}metadata',regex_end='[-]{3}endmetadata',skip=_skip,special_keys=['__all__'])
    self.data.data['title'              ] = ['',  False]
    self.data.data['subtitle'           ] = ['',  False]
    self.data.data['authors'            ] = [[],  False]
    self.data.data['authors_short'      ] = [[],  False]
    self.data.data['emails'             ] = [[],  False]
    self.data.data['affiliations'       ] = [[],  False]
    self.data.data['affiliations_short' ] = [[],  False]
    self.data.data['logo'               ] = ['',  False]
    self.data.data['location'           ] = ['',  False]
    self.data.data['location_short'     ] = ['',  False]
    self.data.data['date'               ] = ['',  False]
    self.data.data['conference'         ] = ['',  False]
    self.data.data['conference_short'   ] = ['',  False]
    self.data.data['session'            ] = ['',  False]
    self.data.data['session_short'      ] = ['',  False]
    self.data.data['max_time'           ] = ['25',False]
    self.data.data['total_slides_number'] = ['',  False]
    self.data.data['dirs_to_copy'       ] = [[],  False]
    self.data.data['toc'                ] = ['',  False]
    if source:
      self.get(source)
    return

  def __str__(self):
    string = 'Metadata\n'
    string += str(self.data)
    return string

  def get(self,source):
    """Method for getting the presentation metadata.

    Return the source without the metadata.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      source without metadata
    """
    self.data.get(source)
    for key,val in self.data.data.items():
      if val[1]:
        if (key == 'authors' or
            key == 'authors_short' or
            key == 'emails' or
            key == 'affiliations' or
            key == 'affiliations_short' or
            key == 'dirs_to_copy'):
          self.data.data[key] = [ast.literal_eval(str(val[0])),True]
    return self.data.strip(source)

  def get_options(self):
    """Method for getting the available data options.

    Returns
    -------
    str
      string with option_names = values pairs (without True/False custom tag)

    >>> meta = Metadata()
    >>> meta.get_options().split('\\n')[16]
    'max_time = 25'
    """
    string = ['Presentation metadata']
    string.append(self.data.get_options())
    return ''.join(string)

  def get_value(self,metadata):
    """Method for getting metadata value (returned as string).

    Parameters
    ----------
    metadata : str
      metadata key

    Returns
    -------
    str
      metadata value

    >>> source = '---metadata authors = ["S. Zaghi","J. Doe"] ---endmetadata'
    >>> meta = Metadata(source)
    >>> meta.get_value(metadata='authors')
    'S. Zaghi and J. Doe'
    """
    if metadata in self.data.data:
      if metadata == 'authors' or metadata == 'authors_short':
        value = ' and '.join(self.data.data[metadata][0])
      elif metadata == 'emails' or metadata == 'affiliations' or metadata == 'affiliations_short' or metadata == 'dirs_to_copy':
        value = ', '.join(self.data.data[metadata][0])
      else:
        value = str(self.data.data[metadata][0])
    return value

  def put_logo(self,doc,style):
    """Method for putting logo element.

    Parameters
    ----------
    doc : yattag.Doc object
      the currently open yattag.Doc object
    metadata : OrderedDict object
      dictionary of metadata
    style : str
      style applied to element
    """
    with doc.tag('figure'):
      if style:
        doc.stag('img',src=self.get_value('logo'),alt=self.get_value('logo'),style=style)
      else:
        doc.stag('img',src=self.get_value('logo'),alt=self.get_value('logo'))
    return

  def to_html(self,metadata,style=None):
    """Method for producing and html string of selected metadata.

    Parameters
    ----------
    metadata : str
      metadata key
    style : str, optional
      css style of metadata tag

    Returns
    -------
    str
      html string containing the metadata

    >>> source = '---metadata authors = ["S. Zaghi","J. Doe"] ---endmetadata'
    >>> meta = Metadata(source)
    >>> meta.to_html(metadata='authors')
    '<span class="metadata">S. Zaghi and J. Doe</span>'
    """
    doc = Doc()
    if metadata == 'logo':
      self.put_logo(doc=doc,style=style)
    else:
      with doc.tag('span',klass='metadata'):
        if style:
          doc.attr(style=style)
        doc.asis(self.get_value(metadata))
    return doc.getvalue()

  def parse(self,source):
    """Method for parsing source and substituting metadata placeholders with theis html equivalent.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      source string parsed

    >>> source = '---metadata authors = ["S. Zaghi","J. Doe"] ---endmetadata $authors'
    >>> meta = Metadata(source)
    >>> meta.parse(source)
    '---metadata authors = ["S. Zaghi","J. Doe"] ---endmetadata <span class="metadata">S. Zaghi and J. Doe</span>'
    """
    protected, obfuscate_source = obfuscate(source = source)
    for meta in self.data.data:
      if meta !='toc':
        regex = re.compile(r"\$"+meta+r"(\[(?P<style>.*?)\])*",re.DOTALL)
        for match in re.finditer(regex,obfuscate_source):
          style = None
          if match.group('style'):
            style = str(match.group('style'))
          obfuscate_source = re.sub(regex,self.to_html(metadata=meta,style=style),obfuscate_source,1)
    return illuminate(source=obfuscate_source,protected_contents=protected)
