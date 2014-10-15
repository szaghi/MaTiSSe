#!/usr/bin/env python
"""
section.py, module definition of Section class.
This defines a section of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import re
# MaTiSSe.py modules
from ..config import __config__
from ..utils.source_editor import __source_editor__ as seditor
from .regexs import  __regex_subsection__
from .subsection import Subsection
# class definition
class Section(object):
  """
  Object for handling a single section, its attributes and methods.

  Attributes
  ----------
  sections_number : int
    global number of sections (equals to the number of Section instances)
  """
  sections_number = 0

  @classmethod
  def reset(cls):
    """Method resetting Section to initial values."""
    cls.sections_number = 0
    return

  def __init__(self,raw_body='',title='',data=None):
    """
    Parameters
    ----------
    raw_body : str, optional
      string containing the body of the section in raw format
    title : str, optional
      section title
    data : OrderedDict object
      section metadata

    Attributes
    ----------
    raw_body : str, optional
      slide number in global numeration
    number : int, optional
      section number in global numeration
    title : str, optional
      section title
    data : OrderedDict object
      section metadata
    subsections : list
      list of subsections
    remainder : str
      remainder of raw_body containing bad placed data slides
    """
    Section.sections_number += 1
    self.raw_body    = raw_body
    self.number      = Section.sections_number
    self.title       = title
    self.data        = OrderedDict()
    if data:
      for key,val in data.items():
        self.data[key] = val[0]
    self.data['sectiontitle' ] = self.title
    self.data['sectionnumber'] = str(self.number)
    self.subsections = None
    self.remainder = None
    return

  def get_remainder(self,end_remainder):
    """Method for getting the remainder of the source in case there are data slides
    before the first subsection defined, i.e. bad use of subsections.

    Parameters
    ----------
    end_remainder : int
      last character of remainder string into the raw_body
    """
    self.remainder = self.raw_body[0:end_remainder]
    if __config__.verbose:
      message = ['\nAttention: found a bad usage of "## subsection" presentation sectioning!']
      message.append('\nThe data:\n"""\n')
      message.append(self.remainder)
      message.append('"""\nis placed before the first subsection defined into the current section')
      message.append('\nThe correct usage is the follwong:')
      message.append('\n1. place the data slides (e.g. "### slide") after the first defined subsection;')
      message.append('\n2. not use at all the subsection partitioning.\n')
      print(''.join(message))
    return

  def get_subsections(self):
    """Method for getting the subsections contained into the section."""
    subsections = []
    self.subsections = []
    purged_source = seditor.purge_codes(self.raw_body)
    for match in re.finditer(__regex_subsection__,purged_source):
      subsections.append([match.group('expr'),match.start(),match.end()])
    if len(subsections)==0:
      # there is no subsection thus crate one with no title as a generic container
      self.subsections.append(Subsection(raw_body=self.raw_body,data=self.data))
    else:
      for ssn,subsec in enumerate(subsections):
        if ssn == 0:
          if subsec[1] != 0:
            self.get_remainder(subsec[1])
        if ssn < len(subsections)-1:
          raw_body = self.raw_body[subsec[2]+1:subsections[ssn+1][1]]
        else:
          raw_body = self.raw_body[subsec[2]+1:]
        self.subsections.append(Subsection(raw_body     = raw_body,
                                           title        = subsec[0],
                                           data         = self.data,
                                           local_number = ssn+1))
    return
