#!/usr/bin/env python3
"""
chapter.py, module definition of Chapter class.
"""

from collections import OrderedDict

from .section import Section


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

    def __init__(self, number, title=None):
        self.number = number
        self.title = title
        self.sections = []
        self.toc = OrderedDict()

    def __str__(self):
        strings = [str(self.title)]
        for section in self.sections:
            strings.append(f"  {section}")
        return "\n".join(strings)

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

    def put_html_attributes(self, doc):
        """Put html attributes of the chapter.

        Parameters
        ----------
        doc: Doc
        """
        doc.attr(("chapternumber", str(self.number)))
        if self.title is not None:
            doc.attr(("chaptertitle", str(self.title)))
