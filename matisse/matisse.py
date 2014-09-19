#!/usr/bin/env python
"""
MaTiSSe.py, Markdown To Impressive Scientific Slides
"""
__appname__ = "MaTiSSe.py"
__description__ = "MaTiSSe.py, Markdown To Impressive Scientific Slides"
__version__ = "v0.0.1"
__author__ = "Stefano Zaghi"
__author_email__ = "stefano.zaghi@gmail.com"
__license__ = "GNU General Public License v3 (GPLv3)"
__url__ = "https://github.com/szaghi/MaTiSSe"
# modules loading
# standard library modules: these should be present in any recent python distribution
import argparse
import os
import sys
# MaTiSSe.py modules
from .config import __config__
from .presentation.presentation import Presentation
from .utils.source_editor import SourceEditor
from .utils.utils import make_output_tree
# global variables
__source_editor__ = SourceEditor()
# setting CLI
__cliparser__ = argparse.ArgumentParser(prog=__appname__,description='MaTiSSe.py, Markdown To Impressive Scientific Slides')
__cliparser__.add_argument('-v','--version',                 action='version',                                help='Show version',version='%(prog)s '+__version__)
__cliparser__.add_argument('-i','--input',            required=False,action='store',     default=None,        help='Input file name of markdown source to be parsed')
__cliparser__.add_argument('-o','--output',           required=False,action='store',     default=None,        help='Output directory name containing the presentation files')
__cliparser__.add_argument('-hs','--highlight-style', required=False,action='store',     default='github.css',help='Select the highlight.js style (default github.css); select "disable" to disable highligth.js',metavar='STYLE.CSS')
__cliparser__.add_argument('--print-preamble',        required=False,action='store_true',default=None,        help='Print the preamble data as parsed from source')
__cliparser__.add_argument('--print-css',             required=False,action='store_true',default=None,        help='Print the css as parsed from source (if done)')
__cliparser__.add_argument('--print-options',         required=False,action='store_true',default=None,        help='Print the available options for each presentation element')
__cliparser__.add_argument('--print-highlight-styles',required=False,action='store_true',default=None,        help='Print the available highlight.js style (default github.css)')
__cliparser__.add_argument('--verbose',               required=False,action='store_true',default=False,       help='More verbose printing messages (default no)')
__cliparser__.add_argument('--indented',              required=False,action='store_true',default=False,       help='Indent html output file (default no, may corrupt TOC rendering)')
__cliparser__.add_argument('--online-MathJax',        required=False,action='store_true',default=None,        help='Use online rendering of LaTeX equations by means of online MathJax service; default use offline, local copy of MathJax engine')
def main():
  """
  Main function.
  """
  cliargs = __cliparser__.parse_args()
  __config__.verbose = cliargs.verbose
  __config__.indented = cliargs.indented
  __config__.online_mathjax = cliargs.online_MathJax
  __config__.set_highlight_style(style=cliargs.highlight_style)
  if __config__.is_verbose():
    print(__config__)
  if cliargs.input:
    if not os.path.exists(cliargs.input):
      sys.stderr.write('Error: input file "'+cliargs.input+'" not found!')
      sys.exit(1)
    else:
      with open(cliargs.input,'r') as mdf:
        source = mdf.read()
      source = __source_editor__.includes(source=source)
      if cliargs.output:
        output = cliargs.output
      else:
        output = os.path.splitext(os.path.basename(cliargs.input))[0]
      output = os.path.normpath(output)+"/"
      make_output_tree(output=output)
      if __config__.is_verbose():
        print('Parsing source '+cliargs.input)
      presentation = Presentation(source=source)
      presentation.save(output=output)
      if cliargs.print_preamble:
        print(presentation)
      if cliargs.print_css:
        print(presentation.get_css())
      if cliargs.print_options:
        print(presentation.get_options())
      if cliargs.print_highlight_styles:
        print(__config__.str_highlight_styles())
  else:
    if cliargs.print_css or cliargs.print_options:
      presentation = Presentation(defaults=True)
    if cliargs.print_css:
      print(presentation.get_css())
    if cliargs.print_options:
      print(presentation.get_options())
    if cliargs.print_highlight_styles:
      print(__config__.str_highlight_styles())
if __name__ == '__main__':
  main()
