#!/usr/bin/env python
"""
theme.py, module definition of Theme class.
This defines the theme of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import copy
# MaTiSSe.py modules
from .theme_canvas import ThemeCanvas
from .theme_heading import ThemeHeading
from .theme_slide import ThemeSlide
# default theme settings
__default_css__ = """
pre code{
    display: block;
    margin: 1%;
    white-space:pre-wrap;
}
code {
    padding: 1%;
    background: rgba(0,0,0,0.05);
    border-radius: 10px 10px 10px 10px;
    box-shadow: 4px 4px 6px rgba(0, 0, 0, .1);
}
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
  def __init__(self,source):
    self.canvas = ThemeCanvas(source=source)
    self.headings = []
    for hds in range(6):
      self.headings.append(ThemeHeading(number=hds+1,source=source))
    self.tittlepage = None
    self.slide = ThemeSlide(source=source)
    return
  def __str__(self):
    string = 'Theme settings\n'
    string += str(self.canvas)
    string += str(self.slide)
    return string
  def __deepcopy__(self):
    return copy.deepcopy(self)
  def get_css(self):
    """
    Method for creating a theme css accordingly to the user options.
    The returned string contains the css theme.
    """
    css = __default_css__
    css += self.canvas.get_css()
    for hds in self.headings:
      css += hds.get_css()
    css += self.slide.get_css()
    return css
  def strip(self,source):
    """
    Method for striping theme raw data from source.
    """
    strip_source = self.canvas.strip(source)
    strip_source = self.slide.strip(strip_source)
    return strip_source
