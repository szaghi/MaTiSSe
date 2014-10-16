#!/usr/bin/env python
"""Testing columns environment"""
import unittest
from matisse.presentation.presentation import Presentation

class SuiteTest(unittest.TestCase):
  """Testing MaTiSSe.py Presentation with columns environment."""
  def test_slides(self):
    """Testing Slide class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/slides/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/slides/test/index.html').read(),talk.to_html())
    return

  def test_subsections(self):
    """Testing Subsection class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/subsections/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/subsections/test/index.html').read(),talk.to_html())
    return

  def test_sections(self):
    """Testing Section class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/sections/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/sections/test/index.html').read(),talk.to_html())
    return

  def test_boxes(self):
    """Testing Box class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/boxes/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/boxes/test/index.html').read(),talk.to_html())
    return

  def test_figures(self):
    """Testing Figure class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/figures/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/figures/test/index.html').read(),talk.to_html())
    return

  def test_notes(self):
    """Testing Note class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/notes/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/notes/test/index.html').read(),talk.to_html())
    return

  def test_columns(self):
    """Testing Columns class instances."""
    self.maxDiff = None
    source = open('src/unittest/python/columns/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/columns/test/index.html').read(),talk.to_html())
    return

  def test_columns_figures(self):
    """Testing Columns with Figures."""
    self.maxDiff = None
    source = open('src/unittest/python/columns_and_figures/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/columns_and_figures/test/index.html').read(),talk.to_html())
    return

  def test_columns_figures_notes(self):
    """Testing Columns with Figures and Notes."""
    self.maxDiff = None
    source = open('src/unittest/python/columns_and_figures_and_notes/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('src/unittest/python/columns_and_figures_and_notes/test/index.html').read(),talk.to_html())
    return

if __name__ == "__main__":
  unittest.main()
