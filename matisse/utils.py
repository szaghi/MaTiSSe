#!/usr/bin/env python
"""
utils.py, module definition of MaTiSSe.py util functions.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import os
import re
from shutil import copyfile#copytree,rmtree
# regular expressions
__expr__ = r"(?P<expr>.*)"
__regex_codeblock__ = re.compile(r"(?P<cblock>[`]{3}.*?[`]{3})",re.DOTALL)
def purge_codeblocks(source):
  """
  Function for removing code blocks from a source string and replacing with an equivalent number of spaces as the removed characters.
  """
  purged_source = source
  for match in re.finditer(__regex_codeblock__,purged_source):
    sub = ' '*len(match.group('cblock'))
    purged_source = re.sub(__regex_codeblock__,sub,purged_source,1)
  return purged_source
def make_output_tree(output):
  """
  Function for creating output tree and copy MaTiSSe.py assets.
  """
  # checking output directory
  if not os.path.exists(output):
    os.makedirs(output)
  # creating css directory
  if not os.path.exists(output+'css'):
    os.makedirs(output+'css')
  # copy some useful css
  css = os.path.join(os.path.dirname(__file__), 'css/normalize.css')
  copyfile(css,output+'css/normalize.css')
  # creating jscript directory
  if not os.path.exists(output+'js'):
    os.makedirs(output+'js')
  # copy some useful scripts
  jscript = os.path.join(os.path.dirname(__file__), 'js/countDown.js')
  copyfile(jscript,output+'js/countDown.js')
  jscript = os.path.join(os.path.dirname(__file__), 'js/impress/impress.js')
  copyfile(jscript,output+'js/impress.js')
  return
