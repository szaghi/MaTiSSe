#!/usr/bin/env python
"""
note.py, module definition of Note class.
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
__renote__ = re.compile(r"(?P<note>\$note(?P<env>.*?)\$endnote)",re.DOTALL)
# classes definition
class Note(Box):
  """
  Object for handling note-box. It is a subclass of Box.

  The syntax is:

  $note
  $style[style_options]
  $caption[caption_options]{caption}
  $content[content_options]{content}
  $endnote

  Note that differently from Box class:
  1. the "content_type" and "caption_type" are automatically set to "note" and "Note" respectively; anyhow they can be still
     specified inside the $note/$endnote environment;
  2. no matter the order of $caption / $content statements, the caption is always placed above the content;

  Attributes
  ----------
  notes_number : int
    global number of notes (equals to the number of Note instances)
  theme: ThemeElement object
    global theme of Note boxes
  """
  notes_number = 0
  theme = ThemeElement(data_tag=r'theme_note')
  theme.data.data['style'  ] = [None,False]
  theme.data.data['caption'] = [None,False]
  theme.data.data['content'] = [None,False]

  @classmethod
  def reset(cls):
    """Method resetting Note to initial values."""
    cls.notes_number = 0
    cls.theme = ThemeElement(data_tag=r'theme_note')
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
      number of figure
    """
    super(Note,self).__init__(ctn_type='note')
    self.cap_type = 'Note'
    Note.notes_number += 1
    self.number = Note.notes_number
    if source:
      self.get(source=source)
    return

  @classmethod
  def get_theme(cls,source):
    """Method for getting theme definition note boxes.

    The syntax is:

    ---theme_note
    style   = style_options
    caption = caption_options
    content = content_options
    ---endtheme_note

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
      with doc.tag('div',klass='note caption'):
        if self.cap_options:
          doc.attr(style=self.cap_options)
        elif Note.theme.data.data['caption'][0]:
          doc.attr(style=Note.theme.data.data['caption'][0])
        doc.asis(self.caption_txt())
    return

  def to_html(self):
    """Method for inserting box to the html doc."""
    doc = Doc()
    with doc.tag('div',klass='note'):
      if self.style:
        doc.attr(style=self.style)
      elif Note.theme.data.data['style'][0]:
        doc.attr(style=Note.theme.data.data['style'][0])
      self.put_caption(doc=doc)
      with doc.tag('div',klass='note content'):
        if self.ctn_options:
          doc.attr(style=self.ctn_options)
        elif Note.theme.data.data['content'][0]:
          doc.attr(style=Note.theme.data.data['content'][0])
        doc.asis(seditor.md_convert(self.ctn))
    return doc.getvalue()

def tokenize(source):
  """Method for tokenizing source tagging notes environments.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source

  Returns
  -------
  list
    list of tokens whose elements are ['type',source_part]; type is 'note' for note environments and
    'unknown' for anything else
  """
  return generic_tokenize(source=source,re_part=__renote__,name_part='note')

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
  protected, obfuscate_source = obfuscate(source=source)
  for match in re.finditer(__renote__, obfuscate_source):
    note = Note(source=illuminate(source=match.group('env'), protected_contents=protected))
    # obfuscate_source = re.sub(__renote__, lambda x: note.to_html(), obfuscate_source, 1)
    obfuscate_source = re.sub(__renote__, note.to_html(), obfuscate_source, 1)
  return illuminate(source=obfuscate_source, protected_contents=protected)
