#!/usr/bin/env python
"""
note.py, module definition of Note class.
"""
import re
from yattag import Doc
from box import Box
from markdown_utils import markdown2html


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
  2. the "caption" is at top by default, but it can be also positionated at the bottom.

  Attributes
  ----------
  notes_number : int
    global number of notes (equals to the number of Note instances)
  """
  regexs = {'note': re.compile(r"(?P<note>\$note(?P<env>.*?)\$endnote)", re.DOTALL)}
  notes_number = 0

  @classmethod
  def reset(cls):
    """Reset to default state."""
    cls.notes_number = 0
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
      note number
    """
    super(Note, self).__init__(ctn_type='note')
    self.cap_type = 'Note'
    Note.notes_number += 1
    self.number = Note.notes_number
    if source:
      self.get(source=source)
    return

  def to_html(self):
    """Convert self data to its html stream."""
    doc = Doc()
    with doc.tag('div', id='note-' + str(self.number)):
      if self.style:
        doc.attr(style=self.style)
      else:
        doc.attr(klass='note')
      if self.cap_position is None or self.cap_position.upper() == 'TOP':
        self.put_caption(doc=doc, klass='note-caption')
      with doc.tag('div', klass='note-content'):
        if self.ctn_options:
          doc.attr(style=self.ctn_options)
        doc.asis(markdown2html(self.ctn, no_p=True))
      if self.cap_position is not None and self.cap_position.upper() == 'BOTTOM':
        self.put_caption(doc=doc, klass='note-caption')
    return doc.getvalue()
