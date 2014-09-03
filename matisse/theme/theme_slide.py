#!/usr/bin/env python
"""
theme_slide.py, module definition of ThemeSlide class.
This defines the theme of the slide element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import copy
# MaTiSSe.py modules
from .theme_element import ThemeElement
from .theme_slide_header import ThemeSlideHeader
from .theme_slide_footer import ThemeSlideFooter
from .theme_slide_sidebar import ThemeSlideSidebar
from .theme_slide_content import ThemeSlideContent
# class definition
class ThemeSlide(ThemeElement):
  """
  Object for handling the presentation theme slide, its attributes and methods.
  """
  def __init__(self,source=None):
    self.content  = ThemeSlideContent()
    self.headers  = []
    self.footers  = []
    self.sidebars = []
    super(ThemeSlide, self).__init__(data_tag=r'theme_slide_global')
    self.data = OrderedDict()
    self.data['width'           ] = '900px'
    self.data['height'          ] = '700px'
    self.data['background'      ] = 'white'
    self.data['border-radius'   ] = '10px'
    self.data['color'           ] = 'black'
    self.data['font-size'       ] = '32px'
    self.data['slide-transition']='horizontal'
    self.css = "\n.slide {\n  display: block;\n  padding: 0;\n  margin: 0;\n  font-family: 'Open Sans', Arial, sans-serif;"
    if source:
      self.content.get_data(source)
      self.get_data(source)
      has,number = self.has_header(source)
      if has:
        for hdr in range(number):
          self.headers.append(ThemeSlideHeader(number=hdr+1,source=source))
      has,number = self.has_footer(source)
      if has:
        for ftr in range(number):
          self.footers.append(ThemeSlideFooter(number=ftr+1,source=source))
      has,number = self.has_sidebar(source)
      if has:
        for sbr in range(number):
          self.sidebars.append(ThemeSlideSidebar(number=sbr+1,source=source))
      # adjusting dimensions of elements depending on other elements, i.e. content and sibars ones
      self.content.adjust_dims(headers=self.headers,footers=self.footers,sidebars=self.sidebars)
      if self.has_sidebar():
        for sidebar in self.sidebars:
          sidebar.adjust_dims(headers=self.headers,footers=self.footers)
    return
  def __str__(self):
    string = '\n  Global slide\n'
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
    return copy.deepcopy(self)
  def has_header(self,source=None):
    """
    Method for inquiring the presence of headers.
    """
    if source:
      number = source.count('theme_slide_header')/2
    else:
      number = len(self.headers)
    return number>0,number
  def has_footer(self,source=None):
    """
    Method for inquiring the presence of footers.
    """
    if source:
      number = source.count('theme_slide_footer')/2
    else:
      number = len(self.footers)
    return number>0,number
  def has_sidebar(self,source=None):
    """
    Method for inquiring the presence of sidebars.
    """
    if source:
      number = source.count('theme_slide_sidebar')/2
    else:
      number = len(self.footers)
    return number>0,number
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
  def strip(self,source):
    """
    Method for striping theme slide raw data from source.
    """
    strip_source = self.content.raw_data.strip(source)
    if len(self.headers)>0:
      for hdr in self.headers:
        strip_source = hdr.strip(strip_source)
    if len(self.footers)>0:
      for ftr in self.footers:
        strip_source = ftr.strip(strip_source)
    if len(self.sidebars)>0:
      for sdr in self.sidebars:
        strip_source = sdr.strip(strip_source)
    return strip_source
