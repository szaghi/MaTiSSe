#!/usr/bin/env python3
"""
subsection.py, module definition of Subsection class.
"""

from .slide import Slide


class Subsection(object):
    """
    Subsection object.

    Attributes
    ----------
    slides_number: int
    """

    slides_number = 0

    @classmethod
    def reset(cls):
        """Reset to default state."""
        cls.slides_number = 0
        Slide.reset()

    def __init__(self, number, title=None):
        self.number = number
        self.title = title
        self.slides = []
        self.toc = []

    def __str__(self):
        strings = [str(self.title)]
        for slide in self.slides:
            strings.append(f"      {slide}")
        return "\n".join(strings)

    def update_toc(self):
        """Update TOC after a new slide (the last one) has been added."""
        self.toc.append(self.slides[-1].title)

    def add_slide(self, slide):
        """
        Add a slide to the subsection.

        Parameters
        ----------
        slide: Slide
        """
        Subsection.slides_number += 1
        self.slides.append(slide)
        self.update_toc()

    def put_html_attributes(self, doc):
        """Put html attributes of the subsection.

        Parameters
        ----------
        doc: Doc
        """
        doc.attr(("subsectionnumber", str(self.number)))
        if self.title is not None:
            doc.attr(("subsectiontitle", str(self.title)))
