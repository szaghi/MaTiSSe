#!/usr/bin/env python
"""
theme_selector.py, module definition of ThemeSelector class.
This defines the theme of a generic "entity" selector that can be
customized by the user.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import copy
# MaTiSSe.py modules
from .theme_element import ThemeElement
# class definition
class ThemeSelector(ThemeElement):
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
    super(ThemeSelector, self).__init__(data_tag=r'theme_selector_'+self.name)
    self.data = OrderedDict()
    self.data['display'        ] = ''
    self.data['margin'         ] = ''
    self.data['padding'        ] = ''
    self.data['border'         ] = ''
    self.data['color'          ] = ''
    self.data['background'     ] = ''
    self.data['font'           ] = ''
    self.data['font-family'    ] = ''
    self.data['font-size'      ] = ''
    self.data['text-decoration'] = ''
    self.data['border-bottom'  ] = ''
    self.data['border-radius'  ] = ''
    self.data['box-shadow'     ] = ''
    self.data['white-space'    ] = ''
    self.name = self.name.replace('-',' ')
    self.css = "\n"+self.name+" {"
    if source:
      self.get_data(source)
    return
  def __deepcopy__(self):
    return copy.deepcopy(self)
