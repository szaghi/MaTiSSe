#!/usr/bin/env python
"""
presentation.py, module definition of Presentation class.
This defines the Presentation object.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import os
import re
from shutil import copytree,rmtree
import sys
# modules not in the standard library
try:
  from yattag import Doc,indent
except ImportError :
  sys.stderr.write("Error: can't import module 'yattag'")
  sys.exit(1)
# MaTiSSe.py modules
from ..utils.metadata import Metadata
from .section import Section
from ..theme.theme import Theme
from .toc import TOC
from ..utils.utils import __expr__,purge_codeblocks
# regular expressions
__regex_section__ = re.compile(r"[^#]#\s+"+__expr__)
# class definition
class Presentation(object):
  """
  Object for handling the presentation.
  """
  def __init__(self,source):
    self.metadata = None
    self.theme    = None
    self.sections = None
    self.toc      = None
    self.__get(source)
    return
  def __get_metadata(self,source):
    """
    Method for getting the presentation metadata.
    Return the source without the metadata.
    """
    self.metadata = Metadata()
    self.metadata.get_raw_data(source)
    self.metadata.get_values()
    return self.metadata.strip(source)
  def __get_theme(self,source):
    """
    Method for getting the presentation theme.
    Return the source without the theme.
    """
    self.theme = Theme(source=source)
    return self.theme.strip(source)
  def __get_sections(self,source):
    """
    Method for getting the sections contained into the source.
    """
    sections = []
    self.sections = []
    # remove code blocks from string parsed in searching sections
    purged_source = purge_codeblocks(source)
    for match in re.finditer(__regex_section__,purged_source):
      sections.append([match.group('expr'),match.start(),match.end()])
    if len(sections)==0:
      # there is no section thus crate one with no title as a generic container
      self.sections.append(Section(raw_body=source,number=0,data=self.metadata.data))
    else:
      for scs,section in enumerate(sections):
        if scs < len(sections)-1:
          self.sections.append(Section(raw_body=source[section[2]+1:sections[scs+1][1]-1],number=scs+1,title=section[0],data=self.metadata.data))
        else:
          self.sections.append(Section(raw_body=source[section[2]+1:],number=scs+1,title=section[0],data=self.metadata.data))
    self.toc = TOC(self.sections)
    self.metadata.set_value('toc',str(self.toc))
    return
  def __get(self,source):
    """
    Method for getting the presentation from source.
    """
    strip_source = self.__get_metadata(source=source)
    strip_source = self.__get_theme(source=strip_source)
    self.__get_sections(source=strip_source)
    slides_number = 0
    for section in self.sections:
      section.get_subsections()
      for subsection in section.subsections:
        slides_number = subsection.get_slides(slides_number=slides_number)
    self.metadata.set_value('total_slides_number',slides_number)
    return
  def to_html(self):
    """
    Method for producing and html string document form presentation object.
    """
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
      doc.attr(title = self.metadata.data['title'])
      with tag('head'):
        doc.stag('meta',charset='utf-8')
        doc.stag('meta',author=' and '.join(self.metadata.data['authors']))
        with tag('title'):
          text(self.metadata.data['title'])
        doc.stag('meta',subtitle=self.metadata.data['subtitle'])
        doc.stag('link',rel='stylesheet', href='css/normalize.css')
        doc.stag('link',rel='stylesheet', href='css/theme.css')
      with tag('body',onload="resetCountdown("+self.metadata.data['max_time']+");"):
        with tag('div',id='impress'):
          for section in self.sections:
            section.to_html(tag=tag,doc=doc,theme=self.theme.slide)
        with tag('script'):
          doc.attr(src='js/countDown.js')
        with tag('script'):
          doc.attr(src='js/impress.js')
        with tag('script'):
          doc.asis('impress().init();')
    return indent(doc.getvalue())
  def save(self,output):
    """
    Method for saving the html form of presentation into external file.
    """
    with open(output+'index.html','w') as html:
      html.write(self.to_html())
    # copy user defined directories if set
    if len(self.metadata.data['dirs_to_copy'])>0:
      for data in self.metadata.data['dirs_to_copy']:
        if os.path.exists(output+data):
          rmtree(output+data)
        copytree(data,output+data)
    # writing css theme
    with open(output+'css/theme.css','w') as css_theme:
      css_theme.writelines(self.theme.get_css())
    return
