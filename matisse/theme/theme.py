#!/usr/bin/env python
"""
theme.py, module definition of Theme class.
This defines the theme of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
# MaTiSSe.py modules
from .canvas import Canvas
from .heading import Heading
from .selector import Selector
from .slide.slide import Slide
from ..utils.utils import purge_overriding_slide_themes
# default theme settings
__default_css__ = """
.toc-section .emph {
  background: rgba(200,200,200,0.25);
  margin: 3%;
}
.toc-subsection .emph {
  background: rgba(200,200,200,0.25);
  margin: 3%;
}
.toc-slide .emph {
  background: rgba(200,200,200,0.25);
  margin: 3%;
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
  """Theme is an object that handles the presentation theme, its attributes and methods."""
  def __init__(self,source=None):
    """
    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Attributes
    ----------
    canvas: Canvas object
      convas over which all elements are rendered
    headings: list
      list of ThemeElement objects for handling style of html headings (h1,h2,...h6)
    titlepage: none
    slide: Slide object
      base theme of slides
    selectors: list
      list of ThemeElement objects for handling user defined custom selectors (e.g. <code> tags)
    """
    self.canvas = Canvas()
    self.headings = []
    for hds in range(6):
      self.headings.append(Heading(number=hds+1))
    self.tittlepage = None
    self.slide = Slide()
    self.selectors = []
    if source:
      purged_source = purge_overriding_slide_themes(source)
      self.get(source=purged_source)
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

  def __get_selectors(self,source):
    """Method for getting the definition of user-defined custom selectors.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    number = source.count('theme_selector_')/2
    if number>0:
      sel_regex = re.compile(r'[-]{3}theme_selector_(?P<name>[a-zA-Z][a-zA-Z0-9_\-]*)')
      names = []
      for match in re.finditer(sel_regex,source):
        names.append(match.group('name'))
      for name in names:
        self.selectors.append(Selector(name=name,source=source))
    return

  def check_specials(self):
    """Method for checking specials data entries.
    The main theme has not special entries, not being a subclass of ThemeElement.
    However the check_specials method of other contained theme elements is called.
    """
    self.canvas.check_specials()
    for hds in self.headings:
      hds.check_specials()
    self.slide.check_specials()
    if len(self.selectors)>0:
      for selector in self.selectors:
        selector.check_specials()
    return

  def get(self,source):
    """Method for getting data values from source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    self.canvas.get(source=source)
    for hds in self.headings:
      hds.get(source=source)
    self.slide.get(source=source)
    self.__get_selectors(source=source)
    self.check_specials()
    return

  def set_from(self,other):
    """Method for setting theme using data of other theme.

    Parameters
    ----------
    other : Theme object
    """
    self.canvas.set_from(other=other.canvas)
    for hds,head in enumerate(self.headings):
      head.set_from(other=other.headings[hds])
    self.slide.set_from(other=other.slide)
    self.check_specials()
    return

  def update(self,source):
    """Method for updating data from source without creating new data.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    self.canvas.get(source=source)
    for hds in self.headings:
      hds.get(source=source)
    self.slide.update(source=source)
    if len(self.selectors)>0:
      for slr in self.selectors:
        slr.get(source=source)
    self.check_specials()
    return

  def get_custom(self,chk_specials=False):
    """Method returning only the data that have been set by users (customized) overriding default values.

    Parameters
    ----------
    chk_specials : bool, optional
      if activated handle special entries differently from standard ones
    """
    custom = self.slide.get_custom(chk_specials=chk_specials)
    custom['canvas'] = self.canvas.data.get_custom(chk_specials=chk_specials)
    for hds in self.headings:
      custom['h'+str(hds.number)] = hds.data.get_custom(chk_specials=chk_specials)
    if len(self.selectors)>0:
      for selector in self.selectors:
        custom['slide-selector_'+selector.name] = selector.data.get_custom(chk_specials=chk_specials)
    return custom

  def get_css(self,only_custom=False,as_list=False):
    """Method for creating the css theme. The returned string contains the css theme.

    Parameters
    ----------
    only_custom : bool, optional
      consider only (user) customized data
    as_list : bool, optional
      return a list instead of a string

    Returns
    -------
    str
      a string containing the css code of the theme if as_list = False
    list
      a list of one string containing the css code of the theme if as_list = True
    """
    css = [__default_css__]
    css.append(self.canvas.get_css(only_custom=only_custom))
    for hds in self.headings:
      css.append(hds.get_css(only_custom=only_custom))
    css.append(self.slide.get_css(only_custom=only_custom))
    for sls in self.selectors:
      css.append(sls.get_css(only_custom=only_custom))
    if as_list:
      return css
    else:
      return ''.join(css)

  def strip(self,source):
    """Method for striping theme raw data from source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      source without the theme data
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
