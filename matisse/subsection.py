#!/usr/bin/env python
"""
subsection.py, module definition of Subsection class.
This defines a subsection of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
# MaTiSSe.py modules
from .slide import Slide
from .utils import __expr__,purge_codeblocks
# regular expressions
__regex_slide__ = re.compile(r"[^#]###\s+"+__expr__)
# class definition
class Subsection(object):
  """
  Subsection is an object that handles a single subsection, its attributes and methods.
  """
  def __init__(self,raw_body='',number=0,title='',slides=None,data=None):
    self.raw_body = raw_body
    self.number   = number
    self.title    = title
    self.slides   = slides
    self.data     = dict({'subsectiontitle'  : self.title,
                          'subsectionnumber' : str(self.number)}.items()+data.items())
    return
  def get_slides(self,slides_number):
    """
    Method for getting the slides contained into the subsection.
    """
    slides = []
    self.slides = []
    # remove code blocks from string parsed in searching slides
    purged_source = purge_codeblocks(self.raw_body)
    for match in re.finditer(__regex_slide__,purged_source):
      slides.append([match.group('expr'),match.start(),match.end()])
    for sdn,slide in enumerate(slides):
      slides_number += 1
      if sdn < len(slides)-1:
        self.slides.append(Slide(raw_body = self.raw_body[slide[2]+1:slides[sdn+1][1]],
                                 number   = slides_number,
                                 title    = slide[0],
                                 data     = self.data))
      else:
        self.slides.append(Slide(raw_body = self.raw_body[slide[2]+1:],
                                 number   = slides_number,
                                 title    = slide[0],
                                 data     = self.data))
    return slides_number
  def to_html(self,tag,doc,theme):
    """
    Method for converting section slides content into html format.
    """
    if self.slides:
      for slide in self.slides:
        slide.to_html(tag,doc,theme)
    return
