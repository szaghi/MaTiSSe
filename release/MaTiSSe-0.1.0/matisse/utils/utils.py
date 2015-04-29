#!/usr/bin/env python
"""
utils.py, module definition of MaTiSSe.py util functions.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import os
from shutil import copyfile, copytree, rmtree
# MaTiSSe.py modules
from ..config import __config__
# global variables
# regular expressions
__expr__ = r"(?P<expr>.*)"


def make_output_tree(output):
  """
  Function for creating output tree and copy MaTiSSe.py assets.
  """
  # checking output directory
  if not os.path.exists(output):
    os.makedirs(output)
  # creating css directory
  if not os.path.exists(output + 'css'):
    os.makedirs(output + 'css')
  # normalize.css
  css = os.path.join(os.path.dirname(__file__), 'css/normalize.css')
  copyfile(css, output + 'css/normalize.css')
  # creating jscript directory
  if not os.path.exists(output + 'js'):
    os.makedirs(output + 'js')
  # MathJax engine
  if not __config__.online_mathjax:
    if os.path.exists(output + 'js/MathJax'):
      rmtree(output + 'js/MathJax')
    jscript = os.path.join(os.path.dirname(__file__), 'js/MathJax')
    copytree(jscript, output + 'js/MathJax')
  # highlight.js
  if __config__.highlight:
    if os.path.exists(output + 'js/highlight'):
      rmtree(output + 'js/highlight')
    jscript = os.path.join(os.path.dirname(__file__), 'js/highlight')
    copytree(jscript, output + 'js/highlight')
  # countDown.js
  jscript = os.path.join(os.path.dirname(__file__), 'js/countDown.js')
  copyfile(jscript, output + 'js/countDown.js')
  # impress.js
  jscript = os.path.join(os.path.dirname(__file__), 'js/impress/impress.js')
  copyfile(jscript, output + 'js/impress.js')
  return
