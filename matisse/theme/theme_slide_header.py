#!/usr/bin/env python
"""
theme_slide_header.py, module definition of ThemeSlideHeader class.
This defines the theme of the slide header element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import copy
# MaTiSSe.py modules
from .theme_element import ThemeElement
# class definition
class ThemeSlideHeader(ThemeElement):
  """
  Object for handling the presentation theme slide header, its attributes and methods.
  """
  def __init__(self,number,source=None):
    self.number = number
    super(ThemeSlideHeader, self).__init__(data_tag=r'theme_slide_header_'+str(self.number))
    self.data = OrderedDict()
    self.data['height'       ] = '0%'
    self.data['background'   ] = 'white'
    self.data['border-radius'] = '10px 10px 0 0'
    self.data['color'        ] = 'black'
    self.data['elements'     ] = []
    self.data['padding'      ] = '0'
    self.css = "\n.slide-header_"+str(self.number)+" {\n  padding:0;"
    if source:
      self.get_data(source)
    return
  def __deepcopy__(self):
    return copy.deepcopy(self)
  def to_html(self,tag,doc,class_name=None,padding=None,style=None,content=None,elements=None):
    """
    Method for inserting slide header content into html.
    """
    super(ThemeSlideHeader, self).to_html(tag,doc,class_name='slide-header_'+str(self.number),content=content,elements=elements)
    return
