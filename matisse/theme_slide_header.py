#!/usr/bin/env python
"""
theme_slide_header.py, module definition of ThemeSlideHeader class.
This defines the theme of the slide header element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import copy
# MaTiSSe.py modules
from .rawdata import Rawdata
from .theme_element import ThemeElement
# class definition
class ThemeSlideHeader(ThemeElement):
  """
  Object for handling the presentation theme slide header, its attributes and methods.
  """
  def __init__(self,
               number,
               raw_data = None,
               data = None,
               css = None,
               padding = None,
               active = None):
    self.number = number
    super(ThemeSlideHeader, self).__init__(raw_data=Rawdata(regex_start=r'[-]{3}theme_slide_header_'+str(self.number),regex_end=r'[-]{3}endtheme_slide_header_'+str(self.number)),
                                           data={'height'        : '0%',
                                                 'background'    : 'white',
                                                 'border-radius' : '10px 10px 0 0',
                                                 'color'         : 'black',
                                                 'elements'      : []},
                                           css = "\n.slide-header_"+str(self.number)+" {\n  padding:0;",
                                           active=active)
    return
  def __deepcopy__(self):
    return ThemeSlideHeader(number   = copy.deepcopy(self.number),
                            raw_data = copy.deepcopy(self.raw_data),
                            data     = copy.deepcopy(self.data),
                            css      = copy.deepcopy(self.css),
                            padding  = copy.deepcopy(self.padding),
                            active   = copy.deepcopy(self.active))
  def to_html(self,tag,doc,class_name=None,padding=None,style=None,content=None,elements=None):
    """
    Method for inserting slide header content into html.
    """
    super(ThemeSlideHeader, self).to_html(tag,doc,class_name='slide-header_'+str(self.number),content=content,elements=elements)
    return
