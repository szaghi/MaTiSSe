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
from .subsection import Subsection
from ..utils.utils import __expr__,purge_codeblocks
# regular expressions
__regex_subsection__ = re.compile(r"[^#]##\s+"+__expr__)
# class definition
class Section(object):
  """
  Object for handling a single section, its attributes and methods.
  """
  def __init__(self,raw_body='',number=0,title='',data=None):
    self.raw_body    = raw_body
    self.number      = number
    self.title       = title
    self.subsections = None
    self.data        = OrderedDict()
    if data:
      for key,val in data.items():
        self.data[key] = val
    self.data['sectiontitle' ] = self.title
    self.data['sectionnumber'] = str(self.number)
    return
  def get_subsections(self):
    """
    Method for getting the subsections contained into the section.
    """
    subsections = []
    self.subsections = []
    # remove code blocks from string parsed in searching slides
    purged_source = purge_codeblocks(self.raw_body)
    for match in re.finditer(__regex_subsection__,purged_source):
      subsections.append([match.group('expr'),match.start(),match.end()])
    if len(subsections)==0:
      # there is no subsection thus crate one with no title as a generic container
      self.subsections.append(Subsection(raw_body=self.raw_body,data=self.data))
    else:
      for ssn,subsec in enumerate(subsections):
        if ssn < len(subsections)-1:
          raw_body = self.raw_body[subsec[2]+1:subsections[ssn+1][1]]
        else:
          raw_body = self.raw_body[subsec[2]+1:]
        self.subsections.append(Subsection(raw_body = raw_body,
                                           number   = ssn+1,
                                           title    = subsec[0],
                                           data     = self.data))
    return
  def to_html(self,tag,doc,theme):
    """
    Method for converting section slides content into html format.
    """
    if self.subsections:
      for subsection in self.subsections:
        subsection.to_html(tag,doc,theme)
    return
