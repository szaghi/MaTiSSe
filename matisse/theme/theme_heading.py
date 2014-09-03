#!/usr/bin/env python
"""
theme_heading.py, module definition of ThemeHeading class.
This defines the theme of the headings.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import copy
# MaTiSSe.py modules
from .theme_element import ThemeElement
# default size of each heading of the standard 6 headings (h1, h2, etc...)
__sizes__ = ['220%','200%','180%','160%','140%','120%']
# class definition
class ThemeHeading(ThemeElement):
  """
  Object for handling the presentation theme headings, its attributes and methods.
  """
  def __init__(self,number,source=None):
    self.number = number
    super(ThemeHeading, self).__init__(data_tag=r'theme_heading_'+str(self.number))
    self.data = OrderedDict()
    self.data['margin'   ] = '0'
    self.data['padding'  ] = '0'
    self.data['border'   ] = '0'
    self.data['font'     ] = 'inherit'
    self.data['font-size'] =  __sizes__[self.number-1]
    self.css = "\nh"+str(self.number)+" {"
    if source:
      self.get_data(source)
    return
  def __deepcopy__(self):
    return copy.deepcopy(self)
