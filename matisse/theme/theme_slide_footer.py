#!/usr/bin/env python
"""
theme_slide_footer.py, module definition of ThemeSlideFooter class.
This defines the theme of the slide footer element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import copy
# MaTiSSe.py modules
from .theme_element import ThemeElement
# class definition
class ThemeSlideFooter(ThemeElement):
  """
  Object for handling the presentation theme slide footer, its attributes and methods.
  """
  def __init__(self,number,source=None):
    self.number = number
    super(ThemeSlideFooter, self).__init__(data_tag=r'theme_slide_footer_'+str(self.number))
    self.data = OrderedDict()
    self.data['height'       ] = '0%'
    self.data['background'   ] = 'white'
    self.data['border-radius'] = '0 0 10px 10px'
    self.data['color'        ] = 'black'
    self.data['elements'     ] = []
    self.data['padding'      ] = '0'
    self.css = "\n.slide-footer_"+str(self.number)+" {\n  clear: both;"
    if source:
      self.get_data(source)
    return
  def __deepcopy__(self):
    return copy.deepcopy(self)
  def to_html(self,tag,doc,class_name=None,padding=None,style=None,content=None,elements=None):
    """
    Method for inserting slide footer content into html.
    """
    super(ThemeSlideFooter, self).to_html(tag,doc,class_name='slide-footer_'+str(self.number),content=content,elements=elements)
    return
