#!/usr/bin/env python
"""
figure.py, module definition of Figure class.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
# modules not in the standard library
from yattag import Doc
# MaTiSSe.py modules
from ..utils.source_editor import obfuscate_codeblocks as obfuscate
from ..utils.source_editor import illuminate_protected as illuminate
from ..utils.source_editor import tokenize as generic_tokenize
from .box import Box
from .theme_element import ThemeElement
# global variables
# regular expressions
__refigure__ = re.compile(r"(?P<figure>\$figure(?P<env>.*?)\$endfigure)", re.DOTALL)
# classes definition
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
  2. no matter the order of $caption / $content statements, the caption is always placed below the content;

  Attributes
  ----------
  figures_number : int
    global number of figures (equals to the number of Figure instances)
  theme: ThemeElement object
    global theme of Figure boxes
  """
  figures_number = 0
  theme = ThemeElement(data_tag=r'theme_figure')
  theme.data.data['style'] = [None, False]
  theme.data.data['caption'] = [None, False]
  theme.data.data['content'] = [None, False]

  @classmethod
  def reset(cls):
    """Method resetting Figure to initial values."""
    cls.figures_number = 0
    cls.theme = ThemeElement(data_tag=r'theme_figure')
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
    super(Figure, self).__init__(ctn_type='figure')
    self.cap_type = 'Figure'
    Figure.figures_number += 1
    self.number = Figure.figures_number
    if source:
      self.get(source=source)
    return

  @classmethod
  def get_theme(cls,source):
    """Method for getting theme definition figure boxes.

    The syntax is:

    ---theme_figure
    style   = style_options
    caption = caption_options
    content = content_options
    ---endtheme_figure

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
      with doc.tag('figcaption'):
        if self.cap_options:
          doc.attr(style=self.cap_options)
        elif Figure.theme.data.data['caption'][0]:
          doc.attr(style=Figure.theme.data.data['caption'][0])
        doc.asis(self.caption_txt())
    return

  def to_html(self):
    """Method for inserting box to the html doc."""
    doc = Doc()
    with doc.tag('div',klass='figure'):
      doc.attr(('id','Figure-'+str(self.number)))
      if self.style:
        doc.attr(style=self.style)
      elif Figure.theme.data.data['style'][0]:
        doc.attr(style=Figure.theme.data.data['style'][0])
      with doc.tag(self.ctn_type):
        if self.ctn_options:
          doc.stag('img',src=self.ctn,klass='image',style=self.ctn_options,alt='Figure-'+self.ctn)
        elif Figure.theme.data.data['content'][0]:
          doc.stag('img',src=self.ctn,klass='image',style=Figure.theme.data.data['content'][0],alt='Figure-'+self.ctn)
        else:
          doc.stag('img',src=self.ctn,klass='image',style='width:100%;',alt='Figure-'+self.ctn)
        self.put_caption(doc=doc)
    return doc.getvalue()

def tokenize(source):
  """Method for tokenizing source tagging figures environments.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source

  Returns
  -------
  list
    list of tokens whose elements are ['type',source_part]; type is 'figure' for figure environments and
    'unknown' for anything else
  """
  return generic_tokenize(source=source,re_part=__refigure__,name_part='figure')

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
  for match in re.finditer(__refigure__, obfuscate_source):
    figure = Figure(source=illuminate(source=match.group('env'), protected_contents=protected))
    # obfuscate_source = re.sub(__refigure__, lambda x: figure.to_html(), obfuscate_source, 1)
    obfuscate_source = re.sub(__refigure__, figure.to_html(), obfuscate_source, 1)
  return illuminate(source=obfuscate_source, protected_contents=protected)
