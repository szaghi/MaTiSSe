#!/usr/bin/env python
"""
section.py, module definition of Section class.
"""
from __future__ import absolute_import
from __future__ import print_function
from collections import OrderedDict
from .subsection import Subsection


class Section(object):
  """
  Section object.

  Attributes
  ----------
  subsections_number: int
  """
  subsections_number = 0

  @classmethod
  def reset(cls):
    """Reset to default state."""
    cls.subsections_number = 0
    Subsection.reset()
    return

  def __init__(self, number, title=None):
    self.number = number
    self.title = title
    self.subsections = []
    self.toc = OrderedDict()
    return

  def __str__(self):
    strings = [str(self.title)]
    for subsection in self.subsections:
      strings.append("    " + str(subsection))
    return '\n'.join(strings)

  def update_toc(self):
    """Update TOC after a new subsection (the last one) has been added."""
    self.toc[self.subsections[-1].title] = self.subsections[-1].toc

  def add_subsection(self, subsection):
    """
    Add a subsection to the section.

    Parameters
    ----------
    section: Subsection
    """
    Section.subsections_number += 1
    self.subsections.append(subsection)
    self.update_toc()
    return

  def put_html_attributes(self, doc):
    """Put html attibutes of the section.

    Parameters
    ----------
    doc: Doc
    """
    doc.attr(('sectionnumber', str(self.number)))
    if self.title is not None:
      doc.attr(('sectiontitle', str(self.title)))
    return
