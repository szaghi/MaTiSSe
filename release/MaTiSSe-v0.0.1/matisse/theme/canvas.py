#!/usr/bin/env python
"""
canvas.py, module definition of Canvas class.
This defines the theme of the canvas on top of which all slides are rendered.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
# MaTiSSe.py modules
from .theme_element import ThemeElement
# class definition
class Canvas(ThemeElement):
  """
  Object for handling the presentation theme canvas, its attributes and methods.
  """
  def __init__(self,source=None):
    super(Canvas,self).__init__(data_tag=r'theme_canvas')
    self.data.data['background'] = ['radial-gradient(rgb(240, 240, 240), rgb(190, 190, 190))',False]
    if source:
      self.get(source)
    return

  def get_options(self):
    """Method for getting the available data options."""
    string = ['\n\nCanvas']
    string.append(self.data.get_options())
    return ''.join(string)

  def get_css(self,only_custom=False,as_list=False):
    """Method for getting css from data.
    """
    css = "\nbody {"
    css += self.data.get_css(only_custom=only_custom)
    css += "\n}\n"
    if as_list:
      return [css]
    else:
      return css
