#!/usr/bin/env python
"""
box.py, module definition of Box class.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
import sys
# modules not in the standard library
try:
  from yattag import Doc
except ImportError :
  sys.stderr.write("Error: can't import module 'yattag'")
  sys.exit(1)
# MaTiSSe.py modules
from ..data.data import Data
# global variables
# regular expressions
__rebox__ = re.compile(r"\$box(?P<box>.*?)\$endbox",re.DOTALL)
__refigure__ = re.compile(r"\$figure(?P<box>.*?)\$endfigure",re.DOTALL)
__renote__ = re.compile(r"\$note(?P<box>.*?)\$endnote",re.DOTALL)
__restl__ = re.compile(r"\$style\[(?P<style>.*?)\]",re.DOTALL)
__rectn__ = re.compile(r"\$content(\((?P<ctn_type>.*?)\))*(\[(?P<ctn_options>.*?)\])*\{(?P<ctn>.*?)\}",re.DOTALL)
__recap__ = re.compile(r"\$caption(\((?P<cap_type>.*?)\))*(\[(?P<cap_options>.*?)\])*(\{(?P<cap>.*?)\})*",re.DOTALL)
# default attributes initialization (can be overridden by theme settings)
__style__ = {'figure': None, 'table': None, 'note': None}
__ctn_options__ = {'figure': None, 'table': None, 'note': None}
#__cap_type__ = {'figure': 'Figure', 'table': 'Table', 'note': 'Note'}
__cap_options__ = {'figure': None, 'table': None, 'note': None}
# classes definition
class Box(object):
  """
  Object for handling a box. It can contains anythings (figures, tables, text...). The syntax is:

  $box
  $style[background:green;]
  $content(figure)[width:60%;]{images/matisse-universe.png}
  $caption(Figure)[font-size:80%;]{MaTiSSe.py Universe}
  $endbox
  """
  def __init__(self,ctn_type=None):
    """
    Parameters
    ----------
    ctn_type : {'figure','table','note'}, optional
      box content type

    Attributes
    ----------
    style : str
      box style
    ctn_type : {'figure','table','note'}
      box content type
    ctn_options : str
      box content options
    ctn : str
      box content
    cap_type : {'figure','table','note'}
      box caption type
    cap_options : str
      box caption options
    cap : str
      box caption
    """
    self.style = None
    self.ctn_type = ctn_type
    self.ctn_options = None
    self.ctn = None
    self.cap_type = None
    self.cap_options = None
    self.cap = None
    if self.ctn_type:
      self.style = __style__[self.ctn_type]
      self.ctn_options = __ctn_options__[self.ctn_type]
      #self.cap_type = __cap_type__[self.ctn_type]
      self.cap_options = __cap_options__[self.ctn_type]
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
    match = re.search(__recap__,source)
    if match:
      cap_type = match.group('cap_type')
      if cap_type:
        self.cap_type = cap_type.strip()
      cap_options = match.group('cap_options')
      if cap_options:
        self.cap_options = cap_options.strip()
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
    return

  def get(self,source):
    """Method for getting box data."""
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
    if self.cap_type:
      txt = self.cap_type
    else:
      if self.ctn_type and self.ctn_type == 'figure':
        txt = 'Figure'
      elif self.ctn_type and self.ctn_type == 'table':
        txt = 'Table'
      elif self.ctn_type and self.ctn_type == 'note':
        txt = 'Note'
      else:
        txt = ''
    if self.cap:
      txt += ': '+self.cap
    return txt

  def put_caption(self,doc):
    """Method for inserting caption into doc.

    Parameters
    ----------
    doc : yattag.Doc object
      yattag document where to put caption
    """
    if self.cap or self.cap_type:
      if self.ctn_type and self.ctn_type == 'figure':
        with doc.tag('figcaption'):
          if self.cap_options:
            doc.attr(style=self.cap_options)
          doc.text(self.caption_txt())
      elif self.ctn_type and self.ctn_type == 'table':
        pass
      elif self.ctn_type and self.ctn_type == 'note':
        with doc.tag('div',klass='note caption'):
          if self.cap_options:
            doc.attr(style=self.cap_options)
          doc.text(self.caption_txt())
      else:
        pass
    return

  def to_html(self):
    """Method for inserting image to the html doc."""
    doc = Doc()
    with doc.tag('div',markdown='1',klass='box'):
      if self.style:
        doc.attr(style=self.style)
      if self.ctn_type:
        if self.ctn_type == 'figure':
          with doc.tag(self.ctn_type):
            if self.ctn_options:
              doc.stag('img',src=self.ctn,klass='image',style=self.ctn_options,alt='Figure-'+self.ctn)
            else:
              doc.stag('img',src=self.ctn,klass='image',style='width:100%;',alt='Figure-'+self.ctn)
            self.put_caption(doc=doc)
        elif self.ctn_type == 'table':
          pass
        elif self.ctn_type == 'note':
          with doc.tag('div',klass='note'):
            self.put_caption(doc=doc)
            with doc.tag('div',klass='note content'):
              if self.ctn_options:
                doc.attr(style=self.ctn_options)
              doc.text(self.ctn)
      else:
        pass
    return doc.getvalue()

class Figure(Box):
  """
  Object for handling figure-box. It is a subclass of Box.
  """
  def __init__(self):
    super(Figure,self).__init__(ctn_type='figure')
    self.cap_type = 'Figure'

class Note(Box):
  """
  Object for handling note-box. It is a subclass of Box.
  """
  def __init__(self):
    super(Note,self).__init__(ctn_type='note')
    self.cap_type = 'Note'

# functions definition
def get_themes(source):
  """Method for getting themes definition of boxes styles.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source
  """
  data = Data(regex_start=r'[-]{3}theme_box_note',regex_end=r'[-]{3}endtheme_box_note')
  data.data['style'  ] = [None,False]
  data.data['caption'] = [None,False]
  data.data['content'] = [None,False]
  data.get(source=source)
  if data.data['style'][0]:
    __style__['note'] = data.data['style'][0]
  if data.data['content'][0]:
    __ctn_options__['note'] = data.data['content'][0]
  if data.data['caption'][0]:
    __cap_options__['note'] = data.data['caption'][0]
  return

def strip_themes(source):
  """Method for striping themes data from source.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source

  Returns
  -------
  str
    source without the themes data
  """
  data = Data(regex_start=r'[-]{3}theme_box_note',regex_end=r'[-]{3}endtheme_box_note')
  return data.strip(source)

def parse(source):
  """Method for parsing source substituting boxes with their own html equivalent.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source
  number : int, optional
    number of image in the global numeration

  Returns
  -------
  str
    source string parsed
  int
    number of currently parsed images
  """
  parsed_source = source
  # parsing generic boxes
  for match in re.finditer(__rebox__,parsed_source):
    box = Box()
    box.get(source=match.group('box'))
    parsed_source = re.sub(__rebox__,box.to_html(),parsed_source,1)
  # parsing box-figures
  for match in re.finditer(__refigure__,parsed_source):
    figure = Figure()
    figure.get(source=match.group('box'))
    parsed_source = re.sub(__refigure__,figure.to_html(),parsed_source,1)
  # parsing box-notes
  for match in re.finditer(__renote__,parsed_source):
    note = Note()
    note.get(source=match.group('box'))
    parsed_source = re.sub(__renote__,note.to_html(),parsed_source,1)
  return parsed_source
