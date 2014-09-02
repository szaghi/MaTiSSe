#!/usr/bin/env python
"""
theme_slide_sidebar.py, module definition of ThemeSlideSidebar class.
This defines the theme of the slide sidebar element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import copy
# MaTiSSe.py modules
from .rawdata import Rawdata
from .theme_element import ThemeElement
# class definition
class ThemeSlideSidebar(ThemeElement):
  """
  Object for handling the presentation theme slide sidebars, their attributes and methods.
  """
  def __init__(self,
               number,
               position = 'R',
               raw_data = None,
               data = None,
               css = None,
               padding = None,
               active = None):
    self.number = number
    self.position = position
    super(ThemeSlideSidebar, self).__init__(raw_data=Rawdata(regex_start=r'[-]{3}theme_slide_sidebar_'+str(self.number),regex_end=r'[-]{3}endtheme_slide_sidebar_'+str(self.number)),
                                            data={'width'         : '0%',
                                                  'height'        : '100%',
                                                  'background'    : 'white',
                                                  'border-radius' : '0 0 10px 0',
                                                  'color'         : 'black',
                                                  'position'      : self.position,
                                                  'elements'      : []},
                                            css = "\n.slide-sidebar_"+str(self.number)+" {\n  float: left;",
                                            active=active)
    return
  def __deepcopy__(self):
    return ThemeSlideSidebar(number   = copy.deepcopy(self.number),
                             position = copy.deepcopy(self.position),
                             raw_data = copy.deepcopy(self.raw_data),
                             data     = copy.deepcopy(self.data),
                             css      = copy.deepcopy(self.css),
                             padding  = copy.deepcopy(self.padding),
                             active   = copy.deepcopy(self.active))
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
  def update_position(self):
    """
    Method for updating the position attribute accordingly the data dictionary value.
    """
    self.position = self.data['position']
    return
  def to_html(self,tag,doc,class_name=None,padding=None,style=None,content=None,elements=None):
    """
    Method for inserting slide sidebar content into html.
    """
    super(ThemeSlideSidebar, self).to_html(tag,doc,class_name='slide-sidebar_'+str(self.number),content=content,elements=elements)
    return
