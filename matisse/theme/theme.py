#!/usr/bin/env python
"""
theme.py, module definition of Theme class.
This defines the theme of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
import copy
# MaTiSSe.py modules
from .theme_canvas import ThemeCanvas
from .theme_heading import ThemeHeading
from .theme_selector import ThemeSelector
from .theme_slide import ThemeSlide
# default theme settings
__default_css__ = """
b, strong { font-weight: bold }
i, em { font-style: italic }
a {
  color: inherit;
  text-decoration: none;
  padding: 0 0.1em;
  transition:         0.5s;
}
a:hover,
a:focus {
  background: rgba(255,255,255,1);
  text-shadow: -1px -1px 2px rgba(100,100,100,0.5);
}
input[type=button] {
    padding:0;
    margin:0;
    border:0 none;
    background: rgba(0,0,0,0.01);
}
.countDown {
    display: block;
    padding: 0;
    margin: 0;
}
.timer {
    display:table-row;
}
.timercontrols {
    display:table-row;
}
.step {
    position: relative;
}
.impress-enabled .step {
    margin: 0;
    opacity: 0.3;
    -webkit-transition: opacity 1s;
    -moz-transition:    opacity 1s;
    -ms-transition:     opacity 1s;
    -o-transition:      opacity 1s;
    transition:         opacity 1s;
}
.impress-enabled .step.active { opacity: 1 }
"""
# class definition
class Theme(object):
  """
  Theme is an object that handles the presentation theme, its attributes and methods.
  """
  def __init__(self,source=None):
    if source:
      self.canvas = ThemeCanvas(source=source)
      self.headings = []
      for hds in range(6):
        self.headings.append(ThemeHeading(number=hds+1,source=source))
      self.tittlepage = None
      self.slide = ThemeSlide(source=source)
      self.selectors = []
      self.__get_selectors(source=source)
    else:
      self.canvas = ThemeCanvas()
      self.headings = []
      for hds in range(6):
        self.headings.append(ThemeHeading(number=hds+1))
      self.tittlepage = None
      self.slide = ThemeSlide()
      self.selectors = []
    return
  def __str__(self):
    string = 'Theme settings\n'
    string += '  Canvas\n'
    string += str(self.canvas)
    for hds,heading in enumerate(self.headings):
      string += '\n  h'+str(hds+1)+'\n'
      string += str(heading)
    string += str(self.slide)
    for selector in self.selectors:
      string += '\n  selector '+selector.name+'\n'
      string += str(selector)
    return string
  def __deepcopy__(self):
    return copy.deepcopy(self)
  def __get_selectors(self,source):
    """
    Method for getting the definition of user-defined custom selectors.
    """
    number = source.count('theme_selector_')/2
    if number>0:
      # collecting the user-defined selectors names
      sel_regex = re.compile(r'[-]{3}theme_selector_(?P<name>[a-zA-Z][a-zA-Z0-9_\-]*)')
      names = []
      for match in re.finditer(sel_regex,source):
        names.append(match.group('name'))
      for name in names:
        self.selectors.append(ThemeSelector(name=name,source=source))
    return
  def get_css(self):
    """
    Method for creating the css theme.
    The returned string contains the css theme.
    """
    css = __default_css__
    css += self.canvas.get_css()
    for hds in self.headings:
      css += hds.get_css()
    css += self.slide.get_css()
    for sls in self.selectors:
      css += sls.get_css()
    return css
  def strip(self,source):
    """
    Method for striping theme raw data from source.
    """
    strip_source = self.canvas.strip(source)
    if len(self.headings)>0:
      for hds in self.headings:
        strip_source = hds.strip(strip_source)
    strip_source = self.slide.strip(strip_source)
    if len(self.selectors)>0:
      for sls in self.selectors:
        strip_source = sls.strip(strip_source)
    return strip_source
