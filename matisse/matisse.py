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
import sys
import os
import argparse
# MaTiSSe.py modules
from .utils.utils import make_output_tree
from .presentation.presentation import Presentation
# setting CLI
__cliparser__ = argparse.ArgumentParser(prog=__appname__,description='MaTiSSe.py, Markdown To Impressive Scientific Slides')
__cliparser__.add_argument('-v','--version',                    action='version',                                  help='Show version',version='%(prog)s '+__version__)
__cliparser__.add_argument('input',                             action='store',               default=None,        help='Input file name of markdown source to be parsed')
__cliparser__.add_argument('-o','--output',      required=False,action='store',               default=None,        help='Output directory name containing the presentation files')
__cliparser__.add_argument('--print-preamble',   required=False,action='store_true',          default=None,        help='Print the preamble data as parsed from source')
# global variables for tracking slide position
__current_slide_position__ = [0,0] # x-y position in px
def main():
  """
  Main function.
  """
  cliargs = __cliparser__.parse_args()
  if cliargs.input:
    if not os.path.exists(cliargs.input):
      print('Error: input file "'+cliargs.input+'" not found!')
      sys.exit(1)
    else:
      with open(cliargs.input,'r') as mdf:
        source = mdf.read()
      if cliargs.output:
        output = cliargs.output
      else:
        output = os.path.splitext(os.path.basename(cliargs.input))[0]
      output = os.path.normpath(output)+"/"
      make_output_tree(output=output)
      presentation = Presentation(source=source)
      presentation.save(output=output)
      if cliargs.print_preamble:
        pass
if __name__ == '__main__':
  main()

#try:
  #from multiprocessing import Pool
  #__parallel__ = True
#except ImportError :
  #sys.stderr.write("Error: can't import module 'multiprocessing'")
  #sys.stderr.write("Parallel features are disabled")
#  __parallel__ = False
