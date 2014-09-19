#!/usr/bin/env python
"""
config.py, module definition of MaTiSSe.py configuration.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import os
import sys
# class definition
class MaTiSSeConfig(object):
  """
  Object handling MaTiSSe.py configuration
  """
  def __init__(self):
    """
    Attributes
    ----------
    verbose : bool
      more verbose printing messages (default no)
    indented : bool
      indent html output file (default no, may corrupt TOC rendering)
    online_mathjax : bool
      use online rendering of LaTeX equations by means of online MathJax service;
      default no, use offline local copy of MathJax engine
    highlight : bool
      use highlight.js for syntax highlithing of code blocks
    highlight_style : str
      css style file for highlight.js; the list of available styles can be print by
      'str_highlight_styles' method
    """
    self.verbose = False
    self.indented = False
    self.online_mathjax = False
    self.highlight = True
    self.highlight_style = 'github.css'
    self.__highlight_styles = []
    self.__get_highlight_styles()
    self.__check_highlight_style()
    if self.verbose:
      print(self)
    return

  def __str__(self):
    string = ['MaTiSSe.py configuration']
    string.append('\n  Verbose mode: '+str(self.verbose))
    string.append('\n  Indent html output: '+str(self.indented))
    if self.online_mathjax:
      string.append('\n  LaTeX equations rendering by means of online MathJax service')
    else:
      string.append('\n  LaTeX equations rendering by means offline, local copy of MathJax')
    if self.highlight:
      string.append('\n  Highlight.js style: '+self.highlight_style)
    return ''.join(string)

  def __get_highlight_styles(self):
    """Method for getting the available highlight.js styles."""
    hilite_styles = os.path.join(os.path.dirname(__file__), 'utils/js/highlight/styles')
    for css in os.listdir(hilite_styles):
      if css.endswith(".css"):
        self.__highlight_styles.append(css)
    return

  def __check_highlight_style(self):
    """Method for checking if the selected highlight.js style is available."""
    if self.highlight_style != 'disable':
      avail = (self.highlight_style in self.__highlight_styles)
      if not avail:
        sys.stderr.write("Error: the selected highlight.js style '"+self.highlight_style+"' is not available")
        sys.stderr.write("\nRestore the default value 'github.css'\n")
        self.highlight_style = 'github.css'
        sys.stderr.write(self.str_highlight_styles())
    else:
      avail = False
      self.highlight = False
    return avail

  def set_highlight_style(self,style):
    """Method for setting highlight.js style performing availability check.

    Parameters
    ----------
    style : str
      style file name
    """
    self.highlight_style = style
    self.__check_highlight_style()
    return

  def str_highlight_styles(self):
    """Method for stringify the available highlight.js styles.

    Returns
    -------
    str
      string containing the list of available styles
    """
    string = ['Available highlight.js styles']
    for style in self.__highlight_styles:
      string.append(style)
    return '\n  '.join(string)+'\n'

  def is_verbose(self):
    """Method inquiring verbose mode."""
    return self.verbose

  def is_indented(self):
    """Method inquiring indent mode."""
    return self.indented

  def is_online_mathjax(self):
    """Method inquiring MathJax mode."""
    return self.online_mathjax

# global variables
__initialized__ = False
if not __initialized__:
  __config__ = MaTiSSeConfig()
  __initialized__ = True
