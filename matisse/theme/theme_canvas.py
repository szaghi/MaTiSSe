#!/usr/bin/env python
"""
theme_canvas.py, module definition of ThemeCanvas class.
This defines the theme of the canvas on top of which all slides are rendered.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import copy
# MaTiSSe.py modules
from .theme_element import ThemeElement
# class definition
class ThemeCanvas(ThemeElement):
  """
  Object for handling the presentation theme canvas, its attributes and methods.
  """
  def __init__(self,source=None):
    super(ThemeCanvas, self).__init__(data_tag=r'theme_canvas')
    self.data = OrderedDict()
    self.data['background'] = 'radial-gradient(rgb(240, 240, 240), rgb(190, 190, 190))'
    self.css = "\nbody {"
    if source:
      self.get_data(source)
    return
  def __deepcopy__(self):
    return copy.deepcopy(self)
