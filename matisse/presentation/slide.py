#!/usr/bin/env python
"""
slide.py, module definition of Slide class.
This defines a slide of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
# MaTiSSe.py modules
from ..config import __config__
#from ..theme.image import Image
from ..theme.box import parse as box_parse
from ..theme.slide.position import Position
from ..theme.theme import Theme
from ..utils.source_editor import SourceEditor
# global variables
__source_editor__ = SourceEditor()
# class definition
class Slide(object):
  """
  Slide is an object that handles a single slide, its attributes and methods.
  """
  def __init__(self,raw_body='',number=0,title='',data=None,theme=None):
    """
    Parameters
    ----------
    raw_body : str, optional
      string containing the body of the slide in raw format
    number : int, optional
      slide number in global numeration
    title : str, optional
      slide title
    data : OrderedDict object
      slide metadata

    Attributes
    ----------
    raw_body : str, optional
      string containing the body of the slide in raw format
    number : int, optional
      slide number in global numeration
    title : str, optional
      slide title
    data : OrderedDict object
      slide metadata
    overtheme : Theme object
      overriding theme of the current slide
    pos : Position object
      slide position
    """
    self.raw_body = raw_body
    self.number   = number
    self.title    = title
    self.data     = OrderedDict()
    if data:
      for key,val in data.items():
        self.data[key] = val
    self.data['slidetitle' ] = self.title
    self.data['slidenumber'] = str(self.number)
    self.overtheme = None
    self.pos = Position()
    self.__get_overtheme(theme=theme)
    return

  def __get_overtheme(self,theme=None):
    """Method for checking if the slide has a personal theme overriding the global one.

    Parameters
    ----------
    theme: Theme object, optional
      base theme used to set other overtheme data not being defined
    """
    source = __source_editor__.get_overtheme(source=self.raw_body)
    if source:
      self.overtheme = Theme(source=source)
      if theme:
        self.overtheme.set_from(other=theme)
      self.overtheme.slide.adjust_dims()
      self.raw_body = __source_editor__.strip_overtheme(self.raw_body)
      if __config__.is_verbose():
        print('Found overriding theme for slide n. '+str(self.number))
        print(self.get_css(only_custom=True))
    return

  def get_css(self,only_custom=False):
    """Method returning slide's css.

    Parameters
    ----------
    only_custom : bool, optional
      consider only (user) customized data

    Returns
    -------
    str
      a string containing the css code of the theme
    """
    css = []
    if self.overtheme:
      css = self.overtheme.slide.get_css(only_custom=only_custom,as_list=True)
    if len(css)>0:
      return ''.join(['\n#slide-'+str(self.number)+' '+c[1:] for c in css])
    else:
      return ''

  def to_html(self,position,doc,theme,toc,current):
    """Method for converting slide content into html format.

    Parameters
    ----------
    position : SlidePosition object
      current slide position
    doc : yattag.Doc object
      the main html doc
    theme : Theme object
      the base theme
    toc : TOC object
      presentation Table of Contents
    current : list
      [section number,subsection number,slide number]
    """
    with doc.tag('div'):
      doc.attr(('id','slide-'+str(self.number)))
      doc.attr(('title',self.title))
      doc.attr(('sectiontitle',self.data['sectiontitle']))
      doc.attr(('sectionnumber',self.data['sectionnumber']))
      # get slide positioning data
      actual_theme = None
      if self.overtheme:
        actual_theme = self.overtheme.slide
      else:
        actual_theme = theme
      position.set_position(theme=theme,overtheme=actual_theme)
      if self.title != '$overview':
        doc.attr(('class','step slide'))
        doc.attr(('data-x',str(position.position[0])))
        doc.attr(('data-y',str(position.position[1])))
        doc.attr(('data-z',str(position.position[2])))
        doc.attr(('data-scale',str(position.scale)))
        doc.attr(('data-rotate-x',str(position.rotation[0])))
        doc.attr(('data-rotate-y',str(position.rotation[1])))
        doc.attr(('data-rotate-z',str(position.rotation[2])))
        # inserting elements
        for header in actual_theme.headers.values():
          header.to_html(doc=doc,metadata=self.data,toc=toc,current=current)
        for sidebar in actual_theme.sidebars.values():
          if sidebar.position == 'L':
            sidebar.to_html(doc=doc,metadata=self.data,toc=toc,current=current)
        #actual_theme.content.to_html(doc=doc,padding=actual_theme.content.padding,content='\n'+__md__.convert(self.raw_body))
        #actual_theme.content.to_html(doc=doc,padding=actual_theme.content.padding,content='\n'+__md__.convert(Image().parse(source=self.raw_body)))
          actual_theme.content.to_html(doc=doc,padding=actual_theme.content.padding,content='\n'+__source_editor__.md_convert(box_parse(source=self.raw_body)))
        for sidebar in actual_theme.sidebars.values():
          if sidebar.position == 'R':
            sidebar.to_html(doc=doc,metadata=self.data,toc=toc,current=current)
        for footer in actual_theme.footers.values():
          footer.to_html(doc=doc,metadata=self.data,toc=toc,current=current)
      else:
        doc.attr(('class','step overview'))
        doc.attr(('style',''))
        doc.attr(('data-x','0'))
        doc.attr(('data-y','0'))
        doc.attr(('data-z','0'))
        doc.attr(('data-scale',str(position.scale)))
    return
