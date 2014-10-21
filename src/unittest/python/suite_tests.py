#!/usr/bin/env python
"""Testing columns environment"""
import doctest
import os
from shutil import rmtree
import sys
import unittest
import matisse.data.data as data
import matisse.presentation as presentation
import matisse.theme as theme
import matisse.utils as utils
from matisse.presentation.presentation import Presentation
from matisse.utils.source_editor import __mdx_checklist__
from matisse.utils.utils import make_output_tree

__compare_dirs__ = [dp for dp, dn, filenames in os.walk('src/unittest/python/compare/') for f in filenames if f == 'test.md']
__pyver__ = str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)
class SuiteTest(unittest.TestCase):
  """Testing suite for MaTiSSe.py."""

  def test_compares(self):
    """Testing compare tests."""
    self.maxDiff = None
    num_failures = 0
    failed = []
    for cdir in __compare_dirs__:
      if cdir.endswith('checklists') and not __mdx_checklist__:
        continue
      source = open(cdir+'/test.md').read()
      talk = Presentation(source=source)
      if open(cdir+'/test'+__pyver__+'/index.html').read() != talk.to_html():
        num_failures += 1
        failed.append(cdir)
    if len(failed)>0:
      print(failed)
    self.assertEquals(num_failures,0)
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

  def test_docstrings(self):
    """Testing docstrings into modules."""
    num_failures = doctest.testmod(data)[0]
    self.assertEquals(num_failures,0)
    num_failures = doctest.testmod(presentation.metadata)[0]
    self.assertEquals(num_failures,0)
    num_failures = doctest.testmod(theme.slide.header)[0]
    self.assertEquals(num_failures,0)
    num_failures = doctest.testmod(theme.slide.footer)[0]
    self.assertEquals(num_failures,0)
    num_failures = doctest.testmod(theme.slide.sidebar)[0]
    self.assertEquals(num_failures,0)
    num_failures = doctest.testmod(theme.slide.content)[0]
    self.assertEquals(num_failures,0)
    num_failures = doctest.testmod(theme.slide.position)[0]
    self.assertEquals(num_failures,0)
    num_failures = doctest.testmod(theme.slide.slide)[0]
    self.assertEquals(num_failures,0)
    num_failures = doctest.testmod(theme.theme)[0]
    self.assertEquals(num_failures,0)
    num_failures = doctest.testmod(theme.theme_element)[0]
    self.assertEquals(num_failures,0)
    num_failures = doctest.testmod(utils.source_editor)[0]
    self.assertEquals(num_failures,0)
    return

if __name__ == "__main__":
  unittest.main()
