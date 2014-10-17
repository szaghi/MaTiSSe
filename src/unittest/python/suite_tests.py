#!/usr/bin/env python
"""Testing columns environment"""
import doctest
from shutil import rmtree
import sys
import unittest
import matisse.data.data as data
import matisse.theme.theme_element as theme_element
from matisse.presentation.presentation import Presentation
from matisse.utils.source_editor import __mdx_checklist__
from matisse.utils.utils import make_output_tree

__pyver__ = str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)
class SuiteTest(unittest.TestCase):
  """Testing suite for MaTiSSe.py."""

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

  def test_slides(self):
    """Testing Slide class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/slides/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/slides/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_subsections(self):
    """Testing Subsection class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/subsections/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/subsections/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_sections(self):
    """Testing Section class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/sections/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/sections/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_boxes(self):
    """Testing Box class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/boxes/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/boxes/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_figures(self):
    """Testing Figure class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/figures/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/figures/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_notes(self):
    """Testing Note class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/notes/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/notes/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_columns(self):
    """Testing Columns class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/columns/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/columns/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_columns_figures(self):
    """Testing Columns with Figures."""
    self.maxDiff = None
    source = open('src/unittest/python/columns_and_figures/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/columns_and_figures/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_columns_figures_notes(self):
    """Testing Columns with Figures and Notes."""
    self.maxDiff = None
    source = open('src/unittest/python/columns_and_figures_and_notes/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/columns_and_figures_and_notes/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_checklists(self):
    """Testing markdown checklists."""
    if __mdx_checklist__:
      self.maxDiff = None
      source = open('src/unittest/python/checklists/test.md').read()
      talk = Presentation(source=source)
      self.assertEqual(open('src/unittest/python/checklists/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_headers(self):
    """Testing Header class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/headers/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/headers/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_footers(self):
    """Testing Footer class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/footers/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/footers/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_sidebars(self):
    """Testing Sidebar class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/sidebars/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/sidebars/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_logo(self):
    """Testing logo inserting."""
    self.maxDiff = None
    source = open('src/unittest/python/logo/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/logo/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_timer(self):
    """Testing timer inserting."""
    self.maxDiff = None
    source = open('src/unittest/python/timer/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/timer/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_toc(self):
    """Testing toc inserting."""
    self.maxDiff = None
    source = open('src/unittest/python/toc/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/toc/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

  def test_custom_selector(self):
    """Testing Selector class."""
    self.maxDiff = None
    source = open('src/unittest/python/custom_selector/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/custom_selector/test'+__pyver__+'/index.html').read(),talk.to_html())
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
