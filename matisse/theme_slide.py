#!/usr/bin/env python
"""
theme_slide.py, module definition of ThemeSlide class.
This defines the theme of the slide element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import copy
# MaTiSSe.py modules
from .rawdata import Rawdata
from .theme_element import ThemeElement
from .theme_slide_content import ThemeSlideContent
# class definition
class ThemeSlide(ThemeElement):
  """
  Object for handling the presentation theme slide, its attributes and methods.
  """
  def __init__(self,
               tag_name        = 'div',
               tag_attrs       = None,
               content         = None,
               headers         = None,
               headers_number  = None,
               footers         = None,
               footers_number  = None,
               sidebars        = None,
               sidebars_number = None,
               raw_data        = None,
               data            = None,
               css             = None,
               padding         = None,
               active          = True):
    self.tag_name        = tag_name
    if not tag_attrs:
      self.tag_attrs     = [['class','step slide'],['data-from-markdown','']]
    else:
      self.tag_attrs     = tag_attrs
    if not content:
      self.content       = ThemeSlideContent()
    else:
      self.content       = content
    if not headers:
      self.headers       = []
    else:
      self.headers       = headers
    self.headers_number  = len(self.headers)
    if not footers:
      self.footers       = []
    else:
      self.footers       = footers
    self.footers_number  = len(self.footers)
    if not sidebars:
      self.sidebars      = []
    else:
      self.sidebars      = sidebars
    self.sidebars_number = len(self.sidebars)
    super(ThemeSlide, self).__init__(raw_data=Rawdata(regex_start=r'[-]{3}theme_slide_global',regex_end=r'[-]{3}endtheme_slide_global'),
                                     data={'width'         : '900px',
                                           'height'        : '700px',
                                           'background'    : 'white',
                                           'border-radius' : '10px',
                                           'color'         : 'black',
                                           'font-size'     : '32px'},
                                     css = "\n.slide {\n  display: block;\n  padding: 0;\n  margin: 0;\n  font-family: 'Open Sans', Arial, sans-serif;",
                                     active=active)
    return
  def __str__(self):
    string = 'Slide theme settings\n'

    string += '\n  Global slide\n'
    string += super(ThemeSlide, self).__str__()
    if self.has_header():
      for i,header in enumerate(self.headers):
        string += '\n  Header n.'+str(i+1)+'\n'+str(header)
    if self.has_footer():
      for i,footer in enumerate(self.footers):
        string += '\n  Footer n.'+str(i+1)+'\n'+str(footer)
    if self.has_sidebar():
      for i,sidebar in enumerate(self.sidebars):
        string += '\n  Sidebar n.'+str(i+1)+'\n'+str(sidebar)
    string += '\n  Content\n'+str(self.content)
    return string
  def __deepcopy__(self):
    return ThemeSlide(tag_name        = copy.deepcopy(self.tag_name),
                      tag_attrs       = copy.deepcopy(self.tag_attrs),
                      content         = copy.deepcopy(self.content),
                      headers         = copy.deepcopy(self.headers),
                      headers_number  = copy.deepcopy(self.headers_number),
                      footers         = copy.deepcopy(self.footers),
                      footers_number  = copy.deepcopy(self.footers_number),
                      sidebars        = copy.deepcopy(self.sidebars),
                      sidebars_number = copy.deepcopy(self.sidebars_number),
                      raw_data        = copy.deepcopy(self.raw_data),
                      data            = copy.deepcopy(self.data),
                      css             = copy.deepcopy(self.css),
                      padding         = copy.deepcopy(self.padding),
                      active          = copy.deepcopy(self.active))
  def count_headers(self,source):
    """
    Method for counting the number of headers activated.
    """
    self.headers_number = source.count('theme_slide_header')/2
    return
  def count_footers(self,source):
    """
    Method for counting the number of footers activated.
    """
    self.footers_number = source.count('theme_slide_footer')/2
    return
  def count_sidebars(self,source):
    """
    Method for counting the number of sidebars activated.
    """
    self.sidebars_number = source.count('theme_slide_sidebar')/2
    return
  def has_header(self):
    """
    Method for inquiring the presence of headers.
    """
    header = False
    if len(self.headers)>0:
      for hdr in self.headers:
        header = hdr.active
        if header:
          return header
    return header
  def has_footer(self):
    """
    Method for inquiring the presence of footers.
    """
    footer = False
    if len(self.footers)>0:
      for ftr in self.footers:
        footer = ftr.active
        if footer:
          return footer
    return footer
  def has_sidebar(self):
    """
    Method for inquiring the presence of sidebars.
    """
    sidebar = False
    if len(self.sidebars)>0:
      for sbr in self.sidebars:
        sidebar = sbr.active
        if sidebar:
          return sidebar
    return sidebar
  def get_css(self):
    """
    Method for setting theme values. The theme skeleton is passed as string.
    """
    css = ''
    if self.has_header():
      for header in self.headers:
        css += header.get_css()
    if self.has_footer():
      for footer in self.footers:
        css += footer.get_css()
    if self.has_sidebar():
      for sidebar in self.sidebars:
        css += sidebar.get_css()
    css += self.content.get_css()
    css += super(ThemeSlide,self).get_css()
    return css
