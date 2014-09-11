#!/usr/bin/env python
"""
utils.py, module definition of MaTiSSe.py util functions.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import os
import re
from shutil import copyfile#copytree,rmtree
# global variables
# regular expressions
__expr__ = r"(?P<expr>.*)"
__regex_codeblock__ = re.compile(r"(?P<cblock>[`]{3}.*?[`]{3})",re.DOTALL)
__regex_over_slide_theme__ = re.compile(r"(?P<ostheme>[-]{3}slide(?P<block>.*?)[-]{3}endslide)",re.DOTALL)
def get_block(regex,source,group_name=None):
  """
  Function for getting blocks of characters matching regex from a source string.
  """
  match = re.match(regex,source)
  if match:
    if group_name:
      return match.group(group_name)
    else:
      return match.group()
  return None
def get_over_slide_theme(source):
  """
  Function for getting blocks of characters defining the overriding slide theme from a source string.
  """
  return get_block(regex=__regex_over_slide_theme__,group_name='block',source=source)
def purge_source(regex,source,group_name=None):
  """
  Function for removing blocks of characters matching regex from a source string
  and replacing with an equivalent number of spaces as the removed characters.
  """
  purged_source = source
  for match in re.finditer(regex,purged_source):
    if group_name:
      sub = ' '*len(match.group(group_name))
    else:
      sub = ''
    purged_source = re.sub(regex,sub,purged_source,1)
  return purged_source
def purge_codeblocks(source):
  """
  Function for removing code blocks from a source string and
  replacing with an equivalent number of spaces as the removed characters.
  """
  return purge_source(regex=__regex_codeblock__,group_name='cblock',source=source)
def purge_overriding_slide_themes(source):
  """
  Function for removing overriding slide themes blocks from a source string and
  replacing with an equivalent number of spaces as the removed characters.
  """
  return purge_source(regex=__regex_over_slide_theme__,group_name='ostheme',source=source)
def strip_overriding_slide_themes(source):
  """
  Function for striping outremoving overriding slide themes blocks from a source string.
  """
  return purge_source(regex=__regex_over_slide_theme__,source=source)
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
