#!/usr/bin/env python
"""
subsection.py, module definition of Subsection class.
This defines a subsection of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import re
# MaTiSSe.py modules
from ..config import __config__
from ..utils.source_editor import __source_editor__
from .regexs import  __regex_slide__
from .slide import Slide
# class definition
class Subsection(object):
  """
  Subsection is an object that handles a single subsection, its attributes and methods.

  Attributes
  ----------
  subsections_number : int
    global number of subsections (equals to the number of Subsection instances)
  """
  subsections_number = 0

  @classmethod
  def reset(cls):
    """Method resetting Subsection to initial values."""
    cls.subsections_number = 0
    return

  def __init__(self,raw_body='',title='',data=None,local_number=1):
    """
    Parameters
    ----------
    raw_body : str, optional
      string containing the body of the subsection in raw format
    title : str, optional
      subsection title
    data : OrderedDict object, optional
      subsection metadata
    local_number : int, optional
      subsection number in local-to-section numeration

    Attributes
    ----------
    raw_body : str
      subslide number in global numeration
    number : int
      subsection number in global numeration
    local_number : int
      subsection number in local-to-section numeration
    title : str
      subsection title
    data : OrderedDict object
      subsection metadata
    slides : list
      list of slides
    remainder : str
      remainder data that are not data slides
    """
    Subsection.subsections_number += 1
    self.raw_body     = raw_body
    self.number       = Subsection.subsections_number
    self.local_number = local_number
    self.title        = title
    self.data         = OrderedDict()
    if data:
      for key,val in data.items():
        self.data[key] = val
    self.data['subsectiontitle' ] = self.title
    self.data['subsectionnumber'] = str(self.number)
    self.slides   = None
    self.remainder = None
    return

  def get_remainder(self):
    """Method for getting the remainder of the source in case there are no data slides."""
    self.remainder = self.raw_body
    if __config__.verbose:
      message = ['\nAttention: found a bad usage of presentation sectioning!']
      message.append('\nThere are not data slides!')
      message.append('\nThe data:\n"""\n')
      message.append(self.remainder)
      message.append('"""\nis placed without "### slide" section into the current section/subsection!')
      print(''.join(message))
    return

  def get_slides(self,theme):
    """Method for getting the slides contained into the subsection.

    Parameters
    ----------
    theme : Theme object
    section_number : int
      current section number
    """
    slides = []
    self.slides = []
    purged_source = __source_editor__.purge_codes(self.raw_body)
    for match in re.finditer(__regex_slide__,purged_source):
      slides.append([match.group('expr'),match.start(),match.end()])
    if __config__.toc_at_subsec_beginning:
      slides = [['Table of Contents',__config__.toc_at_subsec_beginning]] + slides
    for sdn,slide in enumerate(slides):
      if len(slide)==2:
        raw_body = '$toc('+str(slide[1])+')'
      else:
        if sdn < len(slides)-1:
          raw_body = self.raw_body[slide[2]+1:slides[sdn+1][1]]
        else:
          raw_body = self.raw_body[slide[2]+1:]
      first_of_sec = None
      first_of_subsec = None
      if sdn == 0:
        first_of_subsec = self.number
        if self.local_number == 1:
          first_of_sec = int(self.data['sectionnumber'])
      data = OrderedDict()
      data['first_of_sec'] = first_of_sec
      data['first_of_subsec'] = first_of_subsec
      data.update(self.data)
      self.slides.append(Slide(raw_body = raw_body, title = slide[0], data = data, theme = theme, local_number = sdn + 1))
    return
