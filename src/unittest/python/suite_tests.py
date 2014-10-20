#!/usr/bin/env python
"""Testing columns environment"""
import doctest
import os
from shutil import rmtree
import sys
import unittest
import matisse.data.data as data
import matisse.theme.theme_element as theme_element
from matisse.presentation.presentation import Presentation
from matisse.utils.source_editor import __mdx_checklist__
from matisse.utils.utils import make_output_tree

__compare_dirs__ = [dp for dp, dn, filenames in os.walk('compare/') for f in filenames if f == 'test.md']
__pyver__ = str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)
class SuiteTest(unittest.TestCase):
  """Testing suite for MaTiSSe.py."""

  def test_compares(self):
    """Testing compare tests."""
    self.maxDiff = None
    for cdir in __compare_dirs__:
      source = open('src/unittest/python/'+cdir+'/test.md').read()
      talk = Presentation(source=source)
      self.assertEqual(open('src/unittest/python/'+cdir+'/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_utils(self):
    """Testing utils module."""
    source = open('src/unittest/python/utils/test.md').read()
    talk = Presentation(source=source)
    make_output_tree(output='src/unittest/python/utils/utils/')
    talk.save('src/unittest/python/utils/utils/')
    self.assertEqual(open('src/unittest/python/utils/test'+__pyver__+'/index.html').read(),
                     open('src/unittest/python/utils/utils/index.html').read())
    rmtree('src/unittest/python/utils/utils')
    return

  def test_data_docstrings(self):
    """Testing docstrings of data module."""
    (num_failures, num_attempts) = doctest.testmod(data)
    self.assertEquals(num_failures,0)
    return

  def test_theme_element_docstrings(self):
    """Testing docstrings of theme_element module."""
    (num_failures, num_attempts) = doctest.testmod(theme_element)
    self.assertEquals(num_failures,0)
    return

if __name__ == "__main__":
  unittest.main()
