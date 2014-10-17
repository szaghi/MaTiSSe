#!/usr/bin/env python
"""
heading.py, module definition of Heading class.
This defines the theme of the headings.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
# MaTiSSe.py modules
from .theme_element import ThemeElement
# default size of each heading of the standard 6 headings (h1, h2, etc...)
__sizes__ = ['220%','200%','180%','160%','140%','120%']
# class definition
class Heading(ThemeElement):
  """
  Object for handling the presentation theme headings, its attributes and methods.
  """
  def __init__(self,number,source=None):
    self.number = number
    super(Heading,self).__init__(data_tag=r'theme_heading_'+str(self.number))
    #self.data.data['margin'         ] = ['inherit',                False]
    #self.data.data['padding'        ] = ['inherit',                False]
    #self.data.data['background'     ] = ['inherit',                False]
    #self.data.data['color'          ] = ['inherit',                False]
    #self.data.data['font'           ] = ['inherit',                False]
    #self.data.data['font-weight'    ] = ['inherit',                False]
    self.data.data['font-size'      ] = [ __sizes__[self.number-1],False]
    #self.data.data['font-family'    ] = ['inherit',                False]
    #self.data.data['text-decoration'] = ['inherit',                False]
    #self.data.data['text-transform' ] = ['inherit',                False]
    #self.data.data['text-shadow'    ] = ['inherit',                False]
    #self.data.data['letter-spacing' ] = ['inherit',                False]
    #self.data.data['line-height'    ] = ['inherit',                False]
    #self.data.data['border'         ] = ['inherit',                False]
    #self.data.data['border-radius'  ] = ['inherit',                False]
    #self.data.data['box-shadow'     ] = ['inherit',                False]
    if source:
      self.get(source)
    return

  def get_options(self):
    """Method for getting the available data options."""
    string = ['\n\nh'+str(self.number)]
    string.append(self.data.get_options())
    return ''.join(string)

  def get_css(self,only_custom=False,as_list=False):
    """Method for getting css from data.
    """
    css = "\nh"+str(self.number)+" {"
    css += self.data.get_css(only_custom=only_custom)
    css += "\n}\n"
    if as_list:
      return [css]
    else:
      return css
