#!/usr/bin/env python
"""Testing columns environment"""
import unittest
from matisse.config import __config__
from matisse.presentation.presentation import Presentation

class ColumnsTest(unittest.TestCase):
  """Testing MaTiSSe.py Presentation with columns environment."""

  def test_slides(self):
    """Testing Slide class instances."""
    source = open('tests/slides/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('tests/slides/test/index.html').read(),talk.to_html())
    talk.reset()
    return

  def test_subsections(self):
    """Testing Subsection class instances."""
    source = open('tests/subsections/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('tests/subsections/test/index.html').read(),talk.to_html())
    talk.reset()
    return

  def test_sections(self):
    """Testing Section class instances."""
    source = open('tests/sections/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('tests/sections/test/index.html').read(),talk.to_html())
    talk.reset()
    return

  def test_boxes(self):
    """Testing Box class instances."""
    source = open('tests/boxes/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('tests/boxes/test/index.html').read(),talk.to_html())
    talk.reset()
    return

  def test_figures(self):
    """Testing Figure class instances."""
    source = open('tests/figures/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('tests/figures/test/index.html').read(),talk.to_html())
    talk.reset()
    return

  def test_notes(self):
    """Testing Note class instances."""
    source = open('tests/notes/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('tests/notes/test/index.html').read(),talk.to_html())
    talk.reset()
    return

  def test_columns(self):
    """Testing Columns class instances."""
    source = open('tests/columns/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('tests/columns/test/index.html').read(),talk.to_html())
    talk.reset()
    return

  def test_columns_figures(self):
    """Testing Columns with Figures."""
    source = open('tests/columns_and_figures/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('tests/columns_and_figures/test/index.html').read(),talk.to_html())
    talk.reset()
    return

  def test_columns_figures_notes(self):
    """Testing Columns with Figures and Notes."""
    source = open('tests/columns_and_figures_and_notes/test.md').read()
    talk = Presentation(source=source)
    self.assertEqual(open('tests/columns_and_figures_and_notes/test/index.html').read(),talk.to_html())
    talk.reset()
    return

if __name__ == "__main__":
  unittest.main()
