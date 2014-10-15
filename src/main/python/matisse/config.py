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

  Attributes
  ----------
  __highlight_styles : list
    list of available highlight.js styles
  """
  __highlight_styles = []

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
    toc_at_sec_beginning : bool
      insert a slide with TOC at the beginning of each section (default false)
    toc_at_subsec_beginning : bool
      insert a slide with TOC at the beginning of each subsection (default false)
    """
    self.verbose = False
    self.indented = False
    self.online_mathjax = False
    self.highlight = True
    self.highlight_style = 'github.css'
    self.toc_at_sec_beginning = None
    self.toc_at_subsec_beginning = None
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
    string.append('\n  Insert TOC at sections beginning: '+str(self.toc_at_sec_beginning))
    string.append('\n  Insert TOC at subsections beginning: '+str(self.toc_at_subsec_beginning))
    return ''.join(string)

  @staticmethod
  def __get_highlight_styles():
    """Method for getting the available highlight.js styles."""
    hilite_styles = os.path.join(os.path.dirname(__file__), 'utils/js/highlight/styles')
    for css in os.listdir(hilite_styles):
      if css.endswith(".css"):
        MaTiSSeConfig.__highlight_styles.append(css)
    return

  def __check_highlight_style(self):
    """Method for checking if the selected highlight.js style is available."""
    if self.highlight_style != 'disable':
      avail = (self.highlight_style in MaTiSSeConfig.__highlight_styles)
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

  def update(self,cliargs):
    """Method for updating config state from command line arguments.

    Parameters
    ----------
    cliargs : argparse parsed object
      command line arguments parsed
    """
    self.verbose = cliargs.verbose
    self.indented = cliargs.indented
    self.online_mathjax = cliargs.online_MathJax
    self.set_highlight_style(style = cliargs.highlight_style)
    self.toc_at_sec_beginning = cliargs.toc_at_sec_beginning
    self.toc_at_subsec_beginning = cliargs.toc_at_subsec_beginning
    return

  def printf(self):
    """Method for printing config data. It checks verbosity."""
    if self.verbose:
      print(self)
    return

# global variables
__initialized__ = False
if not __initialized__:
  __config__ = MaTiSSeConfig()
  __initialized__ = True
