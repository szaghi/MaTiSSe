#!/usr/bin/env python
"""
theme_slide_content.py, module definition of ThemeSlideContent class.
This defines the theme of the slide content element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import copy
# MaTiSSe.py modules
from .rawdata import Rawdata
from .theme_element import ThemeElement
# class definition
class ThemeSlideContent(ThemeElement):
  """
  Object for handling the presentation theme slide content, its attributes and methods.
  """
  def __init__(self,
               raw_data = None,
               data     = None,
               css      = None,
               padding  = None,
               active   = True):
    super(ThemeSlideContent, self).__init__(raw_data=Rawdata(regex_start=r'[-]{3}theme_slide_content',regex_end=r'[-]{3}endtheme_slide_content'),
                                            data={'width'         : '100%',
                                                  'height'        : '100%',
                                                  'background'    : 'white',
                                                  'border-radius' : '0 0 0 0',
                                                  'color'         : 'black',
                                                  'font-size'     : '100%',
                                                  'padding'       : '0'},
                                            css = "\n.slide-content {\n  float: left;",
                                            active=active)
    return
  def __deepcopy__(self):
    return ThemeSlideContent(raw_data = copy.deepcopy(self.raw_data),
                             data     = copy.deepcopy(self.data),
                             css      = copy.deepcopy(self.css),
                             padding  = copy.deepcopy(self.padding),
                             active   = copy.deepcopy(self.active))
  def adjust_dims(self,headers,footers,sidebars):
    """
    Method for adjusting content dimensions accordingly to the settings of other elements of the slide theme.
    """
    # setting padded container
    s_w = int(self.data['width'].strip('%')) # slide content width (in percent %); should be always 100% initially
    s_h = int(self.data['height'].strip('%')) # slide content height (in percent %); should be always 100% initially
    for header in headers:
      if header.active:
        s_h -= int(header.data['height'].strip('%'))
    for footer in footers:
      if footer.active:
        s_h -= int(footer.data['height'].strip('%'))
    for sidebar in sidebars:
      if sidebar.active:
        s_w -= int(sidebar.data['width'].strip('%'))
    self.data['width'] = str(s_w)+'%'
    self.data['height'] = str(s_h)+'%'
    return
  def to_html(self,tag,doc,class_name=None,padding=None,style=None,content=None,elements=None):
    """
    Method for inserting slide content into html.
    """
    super(ThemeSlideContent, self).to_html(tag,doc,class_name='slide-content',padding=self.padding,content=content,elements=elements)
    return
