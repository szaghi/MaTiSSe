#!/usr/bin/env python
"""Testing columns environment"""
import sys
import unittest
from matisse.presentation.presentation import Presentation
from matisse.utils.source_editor import __mdx_checklist__

__pyver__ = str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)
class SuiteTest(unittest.TestCase):
  """Testing MaTiSSe.py Presentation with columns environment."""
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

  def test_slides(self):
    """Testing markdown checklists."""
    if __mdx_checklist__:
      self.maxDiff = None
      source = open('src/unittest/python/checklists/test.md').read()
      talk = Presentation(source=source)
      self.assertEqual(open('src/unittest/python/checklists/test'+__pyver__+'/index.html').read(),talk.to_html())
    return

if __name__ == "__main__":
  unittest.main()
