#!/usr/bin/env python
"""
figure.py, module definition of Figure class.
"""
import re
from yattag import Doc
from box import Box


class Figure(Box):
  """
  Object for handling figure-box. It is a subclass of Box.

  The syntax is:

  $figure
  $style[style_options]
  $caption[caption_options]{caption}
  $content[content_options]{content}
  $endfigure

  Note that differently from Box class:
  1. the "content_type" and "caption_type" are automatically set to "figure" and "Figure" respectively; anyhow they can be still
     specified inside the $figure/$endfigure environment;
  2. the "caption" is at bottom by default, but it can be also positionated at the top.

  Attributes
  ----------
  regexs: dict
    dictionary of regexs
  figures_number : int
    global number of figures (equals to the number of Figure instances)
  """
  regexs = {'figure': re.compile(r"(?P<figure>\$figure(?P<env>.*?)\$endfigure)", re.DOTALL)}
  figures_number = 0

  @classmethod
  def reset(cls):
    """Reset to default state."""
    cls.figures_number = 0
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
      number of figure
    """
    super(Figure, self).__init__(ctn_type='figure')
    self.cap_type = 'Figure'
    Figure.figures_number += 1
    self.number = Figure.figures_number
    if source:
      self.get(source=source)
    return

  def to_html(self):
    """Convert self data to its html stream."""
    doc = Doc()
    with doc.tag('div', id='Figure-' + str(self.number)):
      if self.style:
        doc.attr(style=self.style)
      else:
        doc.attr(klass='figure')
      with doc.tag(self.ctn_type):
        if self.cap_position is not None and self.cap_position.upper() == 'TOP':
          self.put_caption(doc=doc, klass='figure-caption')
        if self.ctn_options:
          doc.stag('img', src=self.ctn, klass='figure-content', style=self.ctn_options, alt='Figure-' + self.ctn)
        else:
          doc.stag('img', src=self.ctn, klass='figure-content', style='width:100%;', alt='Figure-' + self.ctn)
        if self.cap_position is None or self.cap_position.upper() == 'BOTTOM':
          self.put_caption(doc=doc, klass='figure-caption')
    return doc.getvalue()
