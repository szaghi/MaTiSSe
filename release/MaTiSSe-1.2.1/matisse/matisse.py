#!/usr/bin/env python
"""
MaTiSSe.py, Markdown To Impressive Scientific Slides
"""
from __future__ import print_function
import argparse
import os
import sys
from matisse_config import MatisseConfig
from presentation import Presentation

__appname__ = "MaTiSSe.py"
__description__ = "MaTiSSe.py, Markdown To Impressive Scientific Slides"
__long_description__ = "MaTiSSe.py, Markdown To Impressive Scientific Slides. It is a very simple and stupid-to-use (KISS) presentation maker based on simple markdown syntax producing high quality first-class html/css presentation with great support for scientific contents."
__version__ = "1.2.1"
__author__ = "Stefano Zaghi"
__author_email__ = "stefano.zaghi@gmail.com"
__license__ = "GNU General Public License v3 (GPLv3)"
__url__ = "https://github.com/szaghi/MaTiSSe"
__sample__ = r"""
---
theme:
  - backround: black
---

# Part 1

## Section 1

### Subsection 1

#### Slide 1

##### A H5 heading

Lorem ipsum dolor sit amet...

##### Math

$$
x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}
$$

$note
$content{Just a note enviroment}
$endnote
"""


def main():
  """Main function."""
  cliparser = argparse.ArgumentParser(prog=__appname__, description='MaTiSSe.py, Markdown To Impressive Scientific Slides')
  cliparser.add_argument('-v', '--version', action='version', help='Show version', version='%(prog)s ' + __version__)
  cliparser.add_argument('-i', '--input', required=False, action='store', default=None, help='Input file name of markdown source to be parsed')
  cliparser.add_argument('-o', '--output', required=False, action='store', default=None, help='Output directory name containing the presentation files')
  cliparser.add_argument('-t', '--theme', required=False, action='store', default=None, help='Select a builtin theme for initializing a new sample presentation')
  cliparser.add_argument('-hs', '--highlight-style', required=False, action='store', default='github.css', help='Select the highlight.js style (default github.css); select "disable" to disable highligth.js', metavar='STYLE.CSS')
  cliparser.add_argument('-s', '--sample', required=False, action='store', default=None, help='Generate a new sample presentation as skeleton of your one')
  cliparser.add_argument('--toc-at-chap-beginning', required=False, action='store', default=None, help='Insert Table of Contents at each chapter beginning (default no): to activate indicate the TOC depth', metavar='TOC-DEPTH')
  cliparser.add_argument('--toc-at-sec-beginning', required=False, action='store', default=None, help='Insert Table of Contents at each section beginning (default no): to activate indicate the TOC depth', metavar='TOC-DEPTH')
  cliparser.add_argument('--toc-at-subsec-beginning', required=False, action='store', default=None, help='Insert Table of Contents at each subsection beginning (default no): to activate indicate the TOC depth', metavar='TOC-DEPTH')
  cliparser.add_argument('--print-preamble', required=False, action='store_true', default=None, help='Print the preamble data as parsed from source')
  cliparser.add_argument('--print-css', required=False, action='store_true', default=None, help='Print the css as parsed from source (if done)')
  cliparser.add_argument('--print-options', required=False, action='store_true', default=None, help='Print the available options for each presentation element')
  cliparser.add_argument('--print-highlight-styles', required=False, action='store_true', default=None, help='Print the available highlight.js style (default github.css)')
  cliparser.add_argument('--print-themes', required=False, action='store_true', default=None, help='Print the list of the builtin themes')
  cliparser.add_argument('--verbose', required=False, action='store_true', default=False, help='More verbose printing messages (default no)')
  cliparser.add_argument('--online-MathJax', required=False, action='store_true', default=None, help='Use online rendering of LaTeX equations by means of online MathJax service; default use offline, local copy of MathJax engine')
  cliargs = cliparser.parse_args()
  config = MatisseConfig(cliargs=cliargs)
  if cliargs.print_themes:
    print(config.str_themes())
  if cliargs.input:
    if not os.path.exists(cliargs.input):
      sys.stderr.write('Error: input file "' + cliargs.input + '" not found!')
      sys.exit(1)
    else:
      if cliargs.output:
        output = cliargs.output
      else:
        output = os.path.splitext(os.path.basename(cliargs.input))[0]
      output = os.path.normpath(output)
      config.make_output_tree(output=output)
      with open(cliargs.input, 'r') as mdf:
        source = mdf.read()
      presentation = Presentation()
      if config.verbose:
        print('Parsing source ' + cliargs.input)
      if config.theme is not None:
        source = config.put_theme(source=source, output=output)
      presentation.parse(config=config, source=source)
      presentation.save(config=config, output=output)

if __name__ == '__main__':
  main()
