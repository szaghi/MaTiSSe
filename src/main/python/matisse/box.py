#!/usr/bin/env python
"""
box.py, module definition of Box class.
"""
from __future__ import absolute_import
import re
from yattag import Doc
from .markdown_utils import markdown2html


class Box(object):
  """
  Object for handling a box. It is an environment that can contains anythings (figures, tables, notes...).

  The syntax is:

  $box
  $style[style_options]
  $caption(caption_type)[caption_options]{caption}
  $content(content_type)[content_options]{content}
  $endbox

  Note:
  1. "$style[...]" is optional; it defines the style's options for the whole box; "style_options" are valid
     css syntax statements  (e.g. "font-variant:small-caps;");
  2. "$caption(...)[...]{...}" is optional: it defines the box's caption; the "caption_type" defines the
     caption prefixing "class" (e.g. "Fig." for figures): any sentences are valid; the "caption_options" defines
     the style's options of only caption: they are valid css syntax statements (e.g.  "padding:0 2%;"); the
     "caption" (inside the {} parenthesis) defines the caption text; note that "caption_type" and "caption_options"
     are optional thus the following statements are valid:
     + $caption[font-variant:small-caps;]{My caption without caption_type};
     + $caption{My caption without caption_type and caption_options};
  3. "$content(...)[...]{...}" is not optional: it defines the box's content; the "content_type" defines the type
     of the content that can be 'figure', 'table', 'note' and 'box' for generic environments; the "content_options"
     defines the style's options of only content: they are valid css syntax statements (e.g.  "padding:0 2%;"); the
     "content" (inside the {} parenthesis) defines the content (being text, figures, tables, etc...); note that
     "content_type" and "content_options" are optional thus the following statements are valid:
     + $content[font-variant:small-caps;]{My content without content_type};
     + $content{My content without content_type and content_options};

  There are some helper (sub)classes based on Box class for handling specific environments such Video, Figure, Table and Note.

  Note that the themes of box environments can be defined as all other theme elements in order to not have to repeat
  the styling options for each box. To this aim this module provides the "get_themes" function. The definition of such
  a theme can be stripped out by the function "strip_themes" also provided by this module.

  See Also
  --------
  Note
  Table
  Figure
  Video

  Attributes
  ----------
  regexs: dict
    dictionary of regexs
  boxes_number : int
    global number of boxes (equals to the number of Box instances)
  """
  regexs = {'box': re.compile(r"(?P<box>\$box(?P<env>.*?)\$endbox)", re.DOTALL),
            'style': re.compile(r"\$style\[(?P<style>.*?)\]", re.DOTALL),
            'content_fig': re.compile(r"\$content(\((?P<ctn_type>.*?)\))*(\[(?P<ctn_options>.*?)\])*\{(?P<ctn>.*?)\}", re.DOTALL),
            'content': re.compile(r"\$content(\((?P<ctn_type>.*?)\))*(\[(?P<ctn_options>.*?)\])*\{(?P<ctn>.*)\}", re.DOTALL),
            'caption': re.compile(r"\$caption(\((?P<cap_type>.*?)\))*(\[(?P<cap_options>.*?)\])*(\{(?P<cap>.*?)\})*", re.DOTALL),
            'caption_pos': re.compile(r"(?P<cap_pos>position\s*:\s*(?P<cap_position>(TOP)|(BOTTOM))\;*)", re.DOTALL)}
  boxes_number = 0

  @classmethod
  def reset(cls):
    """Reset to default state."""
    cls.boxes_number = 0
    return

  def __init__(self, ctn_type='box', source=None):
    """
    Parameters
    ----------
    ctn_type : {'video', 'figure', 'table', 'note', 'box'}, optional
      box content type
    source : str, optional
      string (as single stream) containing the source

    Attributes
    ----------
    number : int
      box number
    style : str
      box style
    ctn_type : {'video', 'figure', 'table', 'note', 'box'}
      box content type
    ctn_options : str
      box content options
    ctn : str
      box content
    ctn_type : {'video', 'figure', 'table', 'note'}
      box caption type
    cap_options : str
      box caption options
    cap_postion : {'TOP', 'BOTTOM'}
      box caption position
    cap : str
      box caption
    """
    self.number = 0
    self.ctn_type = ctn_type
    self.style = None
    self.ctn_options = None
    self.cap_options = None
    self.cap_position = None
    self.cap_type = None
    self.ctn = None
    self.cap = None
    if self.ctn_type == 'box':
      Box.boxes_number += 1
      self.number = Box.boxes_number
    if source is not None:
      self.get(source=source)
    return

  def __str__(self):
    string = []
    string.append('\nStyle: ' + str(self.style))
    string.append('\nCaption(' + str(self.cap_type) + ')[options=' + str(self.cap_options) + ']: ' + str(self.cap))
    string.append('\nContent(' + str(self.ctn_type) + ')[options=' + str(self.ctn_options) + ']: ' + str(self.ctn))
    return ''.join(string)

  def get_style(self, source):
    """Get box style data.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    match = re.search(Box.regexs['style'], source)
    if match:
      style = match.group('style')
      if style:
        self.style = style.strip()
    return

  def get_caption(self, source):
    """Get box caption data.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    match = re.search(Box.regexs['caption'], source)
    if match:
      cap_type = match.group('cap_type')
      if cap_type:
        if cap_type.lower() == 'none':
          self.cap_type = None
        else:
          self.cap_type = cap_type.strip()
      cap_options = match.group('cap_options')
      if cap_options:
        self.cap_options = cap_options.strip()
        cap_position = re.search(Box.regexs['caption_pos'], self.cap_options)
        if cap_position:
          self.cap_position = cap_position.group('cap_position').strip()
          self.cap_options = self.cap_options.replace(cap_position.group('cap_pos'), '')
          if self.cap_position != 'TOP' and self.cap_position != 'BOTTOM':
            self.cap_position = None
      self.cap = match.group('cap')
      if self.cap:
        self.cap = self.cap.strip()
    return

  def get_content(self, source):
    """Get box caption data.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    if self.ctn_type == 'figure' or self.ctn_type == 'video':
      match = re.search(Box.regexs['content_fig'], source)
    else:
      match = re.search(Box.regexs['content'], source)
    if match:
      ctn_type = match.group('ctn_type')
      if ctn_type:
        self.ctn_type = ctn_type.strip()
      ctn_options = match.group('ctn_options')
      if ctn_options:
        self.ctn_options = ctn_options.strip()
      self.ctn = match.group('ctn')
      if self.ctn:
        self.ctn = self.ctn.strip()
        self.ctn = markdown2html(source=self.ctn, no_p=True)
    return

  def get(self, source):
    """
    Get box data from source.

    Parameters
    ----------
    source : str
      string containing source
    """
    self.get_style(source)
    self.get_caption(source)
    self.get_content(source)
    return

  def caption_txt(self):
    """Buildi caption text.

    Returns
    -------
    str
      caption text
    """
    if self.cap_type and self.cap:
      txt = self.cap_type + ' ' + str(self.number) + ': ' + markdown2html(source=self.cap, no_p=True)
    elif self.cap_type:
      txt = self.cap_type
    elif self.cap:
      txt = markdown2html(source=self.cap, no_p=True)
    return txt

  def put_caption(self, doc, klass='box caption'):
    """Method for inserting caption into doc.

    Parameters
    ----------
    doc : yattag.Doc object
      yattag document where to put caption
    """
    if self.cap or self.cap_type:
      with doc.tag('div', klass=klass):
        if self.cap_options:
          doc.attr(style=self.cap_options)
        doc.asis(self.caption_txt())
    return

  def to_html(self):
    """Convert self data to its html stream."""
    doc = Doc()
    with doc.tag('div', id='box-' + str(self.number)):
      if self.style:
        doc.attr(style=self.style)
      else:
        doc.attr(klass='box')
      if self.cap_position is not None and self.cap_position.upper() == 'TOP':
        self.put_caption(doc=doc, klass='box-caption')
      with doc.tag('div', klass='box-content'):
        if self.ctn_options:
          doc.attr(style=self.ctn_options)
        doc.asis(markdown2html(self.ctn, no_p=True))
      if self.cap_position is None or self.cap_position.upper() == 'BOTTOM':
        self.put_caption(doc=doc, klass='box-caption')
    return doc.getvalue()
