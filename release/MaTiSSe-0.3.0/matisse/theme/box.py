#!/usr/bin/env python
"""
box.py, module definition of Box class.
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
#from ..utils.source_editor import obfuscate_codes as obfuscate
from ..utils.source_editor import tokenize as generic_tokenize
# global variables
# regular expressions
__rebox__ = re.compile(r"(?P<box>\$box(?P<env>.*?)\$endbox)", re.DOTALL)
__restl__ = re.compile(r"\$style\[(?P<style>.*?)\]", re.DOTALL)
__rectn__ = re.compile(r"\$content(\((?P<ctn_type>.*?)\))*(\[(?P<ctn_options>.*?)\])*\{(?P<ctn>.*?)\}", re.DOTALL)
__recap__ = re.compile(r"\$caption(\((?P<cap_type>.*?)\))*(\[(?P<cap_options>.*?)\])*(\{(?P<cap>.*?)\})*", re.DOTALL)
__recappos__ = re.compile(r"(?P<cap_pos>position\s*:\s*(?P<cap_position>(TOP)|(BOTTOM))\;*)", re.DOTALL)


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

  There are some helper (sub)classes based on Box class for handling specific environments such Figure, Table and Note.

  Note that the themes of box environments can be defined as all other theme elements in order to not have to repeat
  the styling options for each box. To this aim this module provides the "get_themes" function. The definition of such
  a theme can be stripped out by the function "strip_themes" also provided by this module.

  See Also
  --------
  Figure
  Table
  Note

  Attributes
  ----------
  boxes_number : int
    global number of boxes (equals to the number of Box instances)
  """
  boxes_number = 0

  @classmethod
  def reset(cls):
    """Method resetting Box to initial values."""
    cls.boxes_number = 0
    return

  def __init__(self, ctn_type='box', source=None):
    """
    Parameters
    ----------
    ctn_type : {'figure','table','note','box'}, optional
      box content type
    source : str, optional
      string (as single stream) containing the source

    Attributes
    ----------
    number : int
      box number
    style : str
      box style
    ctn_type : {'figure','table','note','box'}
      box content type
    ctn_options : str
      box content options
    ctn : str
      box content
    cap_type : {'figure','table','note'}
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
    if source:
      self.get(source=source)
    return

  def __str__(self):
    string = []
    string.append('\nStyle: '+str(self.style))
    string.append('\nCaption('+str(self.cap_type)+')[options='+str(self.cap_options)+']: '+str(self.cap))
    string.append('\nContent('+str(self.ctn_type)+')[options='+str(self.ctn_options)+']: '+str(self.ctn))
    return ''.join(string)

  def __get_style(self,source):
    """Method for getting box style data."""
    match = re.search(__restl__,source)
    if match:
      style = match.group('style')
      if style:
        self.style = style.strip()
    return

  def __get_caption(self,source):
    """Method for getting box caption data."""
    match = re.search(__recap__, source)
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
        cap_position = re.search(__recappos__, self.cap_options)
        if cap_position:
          self.cap_position = cap_position.group('cap_position').strip()
          self.cap_options = self.cap_options.replace(cap_position.group('cap_pos'), '')
          if self.cap_position != 'TOP' and self.cap_position != 'BOTTOM':
            self.cap_position = None
      self.cap = match.group('cap')
      if self.cap:
        self.cap = self.cap.strip()
    return

  def __get_content(self,source):
    """Method for getting box content data."""
    match = re.search(__rectn__,source)
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
        if self.ctn_type == 'box' or self.ctn_type == 'note':
          self.ctn = seditor.md_convert(self.ctn)
    return

  def get(self, source):
    """
    Get box data from source.

    Parameters
    ----------
    source : str
      string containing source
    """
    self.__get_style(source)
    self.__get_caption(source)
    self.__get_content(source)
    return

  def caption_txt(self):
    """Method for building caption text.

    Returns
    -------
    str
      caption text
    """
    if self.cap_type and self.cap:
      txt = self.cap_type+' '+str(self.number)+': '+seditor.md_convert(source=self.cap,no_p=True)
    elif self.cap_type:
      txt = self.cap_type
    elif self.cap:
      txt = seditor.md_convert(source=self.cap,no_p=True)
    return txt

  def put_caption(self,doc):
    """Method for inserting caption into doc.

    Parameters
    ----------
    doc : yattag.Doc object
      yattag document where to put caption
    """
    if self.cap or self.cap_type:
      with doc.tag('div',klass='box caption'):
        if self.cap_options:
          doc.attr(style=self.cap_options)
        doc.asis(self.caption_txt())
    return

  def to_html(self):
    """Method for inserting box to the html doc."""
    doc = Doc()
    with doc.tag('div',klass='box'):
      if self.style:
        doc.attr(style=self.style)
      if self.cap_position == 'TOP':
        self.put_caption(doc=doc)
      with doc.tag('div',klass='box content'):
        if self.ctn_options:
          doc.attr(style=self.ctn_options)
        doc.asis(self.ctn)
      if self.cap_position is None or self.cap_position == 'BOTTOM':
        self.put_caption(doc=doc)
    return doc.getvalue()

def tokenize(source):
  """Method for tokenizing source tagging boxes environments.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source

  Returns
  -------
  list
    list of tokens whose elements are ['type',source_part]; type is 'box' for box environments and
    'unknown' for anything else
  """
  return generic_tokenize(source=source,re_part=__rebox__,name_part='box')

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
  for match in re.finditer(__rebox__,obfuscate_source):
    box = Box(source=illuminate(source=match.group('env'),protected_contents=protected))
    obfuscate_source = re.sub(__rebox__,box.to_html(),obfuscate_source,1)
  return illuminate(source=obfuscate_source,protected_contents=protected)
