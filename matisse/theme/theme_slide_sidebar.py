#!/usr/bin/env python
"""
theme_slide_sidebar.py, module definition of ThemeSlideSidebar class.
This defines the theme of the slide sidebar element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import copy
# MaTiSSe.py modules
from .theme_element import ThemeElement
# class definition
class ThemeSlideSidebar(ThemeElement):
  """
  Object for handling the presentation theme slide sidebars, their attributes and methods.
  """
  def __init__(self,number,position='R',source=None):
    self.number = number
    self.position = position
    super(ThemeSlideSidebar, self).__init__(data_tag=r'theme_slide_sidebar_'+str(self.number))
    self.data = OrderedDict()
    self.data['width'        ] = '0%'
    self.data['height'       ] = '100%'
    self.data['background'   ] = 'white'
    self.data['border-radius'] = '0 0 10px 0'
    self.data['color'        ] = 'black'
    self.data['position'     ] = self.position
    self.data['elements'     ] = []
    self.data['padding'      ] = '0'
    self.css = "\n.slide-sidebar_"+str(self.number)+" {\n  float: left;"
    if source:
      self.get_data(source)
    return
  def __deepcopy__(self):
    return copy.deepcopy(self)
  def adjust_dims(self,headers,footers):
    """
    Method for adjusting sidebar dimensions accordingly to the settings of other elements of the slide theme.
    """
    s_h = int(self.data['height'].strip('%')) # slide sidebar height (in percent %); should be always 100% initially
    for header in headers:
      if header.active:
        s_h -= int(header.data['height'].strip('%'))
    for footer in footers:
      if footer.active:
        s_h -= int(footer.data['height'].strip('%'))
    self.data['height'] = str(s_h)+'%'
    return
  def to_html(self,tag,doc,class_name=None,padding=None,style=None,content=None,elements=None):
    """
    Method for inserting slide sidebar content into html.
    """
    super(ThemeSlideSidebar, self).to_html(tag,doc,class_name='slide-sidebar_'+str(self.number),content=content,elements=elements)
    return
