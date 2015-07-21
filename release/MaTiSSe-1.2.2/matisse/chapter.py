#!/usr/bin/env python
"""
chapter.py, module definition of Chapter class.
"""
from __future__ import print_function
from collections import OrderedDict
from section import Section


class Chapter(object):
  """
  Chapter object.

  Attributes
  ----------
  sections_number: int
  """
  sections_number = 0

  @classmethod
  def reset(cls):
    """Reset to default state."""
    cls.sections_number = 0
    Section.reset()
    return

  def __init__(self, number, title=None):
    self.number = number
    self.title = title
    self.sections = []
    self.toc = OrderedDict()
    return

  def __str__(self):
    strings = [str(self.title)]
    for section in self.sections:
      strings.append("  " + str(section))
    return '\n'.join(strings)

  def update_toc(self):
    """Update TOC after a new section (the last one) has been added."""
    self.toc[self.sections[-1].title] = self.sections[-1].toc

  def add_section(self, section):
    """
    Add a section to the chapter.

    Parameters
    ----------
    section: Section
    """
    Chapter.sections_number += 1
    self.sections.append(section)
    self.update_toc()
    return

  def put_html_attributes(self, doc):
    """Put html attibutes of the chapter.

    Parameters
    ----------
    doc: Doc
    """
    doc.attr(('chapternumber', str(self.number)))
    if self.title is not None:
      doc.attr(('chaptertitle', str(self.title)))
    return
