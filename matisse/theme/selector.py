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
  data_tag = r'theme_selector_'

  @classmethod
  def count(cls,source):
    """Method for computing the number of custom selectors defined into the source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    sel = ThemeElement(data_tag=Selector.data_tag)
    return sel.data.count(source)

  def __init__(self,name,source=None):
    self.name = name
    super(Selector,self).__init__(data_tag=Selector.data_tag+self.name)
    self.data.data['display'        ] = ['inherit',False]
    self.data.data['margin'         ] = ['inherit',False]
    self.data.data['padding'        ] = ['inherit',False]
    self.data.data['background'     ] = ['inherit',False]
    self.data.data['color'          ] = ['inherit',False]
    self.data.data['font'           ] = ['inherit',False]
    self.data.data['font-weight'    ] = ['inherit',False]
    self.data.data['font-size'      ] = ['inherit',False]
    self.data.data['font-family'    ] = ['inherit',False]
    self.data.data['text-decoration'] = ['inherit',False]
    self.data.data['text-transform' ] = ['inherit',False]
    self.data.data['text-shadow'    ] = ['inherit',False]
    self.data.data['letter-spacing' ] = ['inherit',False]
    self.data.data['line-height'    ] = ['inherit',False]
    self.data.data['border'         ] = ['inherit',False]
    self.data.data['border-radius'  ] = ['inherit',False]
    self.data.data['box-shadow'     ] = ['inherit',False]
    self.data.data['white-space'    ] = ['inherit',False]
    self.data.data['overflow-x'     ] = ['inherit',False]
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
