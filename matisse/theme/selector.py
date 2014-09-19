#!/usr/bin/env python
"""
selector.py, module definition of Selector class.
This defines the theme of a generic "entity" selector that can be
customized by the user.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
# MaTiSSe.py modules
from .theme_element import ThemeElement
# class definition
class Selector(ThemeElement):
  """
  Object for handling a generic entity selector, its attributes and methods.
  This can be useful for user customized entities.

  Note that for supporting nested css selectors the selector name can use
  the "-" symbol to compose nested selectors, e.g.:
  name = 'pre-span' defines a nested selector for the <pre><span>...</span></pre>
  selectors resulting in a css like "pre span {...}".
  """
  def __init__(self,name,source=None):
    self.name = name
    super(Selector,self).__init__(data_tag=r'theme_selector_'+self.name)
    self.data.data['display'        ] = ['',    False]
    self.data.data['margin'         ] = ['',    False]
    self.data.data['padding'        ] = ['',    False]
    self.data.data['text-decoration'] = ['',    False]
    self.data.data['border-bottom'  ] = ['',    False]
    self.data.data['box-shadow'     ] = ['',    False]
    self.data.data['white-space'    ] = ['',    False]
    self.data.data['overflow-x'     ] = ['auto',False]
    self._name = self.name.replace('-',' ')
    if source:
      self.get(source)
    return

  def get_options(self):
    """Method for getting the available data options."""
    string = ['\n\nSelector '+self._name]
    string.append(self.data.get_options())
    return ''.join(string)

  def get_css(self,only_custom=False,as_list=False):
    """Method for getting css from data.
    """
    css = "\n"+self._name+" {"
    css += self.data.get_css(only_custom=only_custom)
    css += "\n}\n"
    if as_list:
      return [css]
    else:
      return css
