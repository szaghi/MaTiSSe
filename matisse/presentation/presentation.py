#!/usr/bin/env python
"""
presentation.py, module definition of Presentation class.
This defines the Presentation object.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import ast
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
from ..config import __config__
from ..data.data import Data
from ..theme.theme import Theme
from ..theme.slide.slide import SlidePosition
from ..utils.utils import __expr__,purge_codeblocks
from .section import Section
from .toc import TOC
# regular expressions
__regex_section__ = re.compile(r"[^#]#\s+"+__expr__)
# class definition
class Presentation(object):
  """
  Object for handling the presentation.
  """
  def __init__(self,source=None):
    """
    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Attributes
    ----------
    metadata: Data object
      presentation metadata
    theme: Theme object
    sections: list
      list of sections composing the presentation
    toc: TOC object
      presentation Table of Contents
    pos: SlidePosition object
      position of the current slide
    """

    self.metadata = Data(regex_start='[-]{3}metadata',regex_end='[-]{3}endmetadata',special_keys=['__all__'])
    self.metadata.data['title'              ] = ['',  False]
    self.metadata.data['subtitle'           ] = ['',  False]
    self.metadata.data['authors'            ] = [[],  False]
    self.metadata.data['authors_short'      ] = [[],  False]
    self.metadata.data['emails'             ] = [[],  False]
    self.metadata.data['affiliations'       ] = [[],  False]
    self.metadata.data['affiliations_short' ] = [[],  False]
    self.metadata.data['logo'               ] = ['',  False]
    self.metadata.data['location'           ] = ['',  False]
    self.metadata.data['location_short'     ] = ['',  False]
    self.metadata.data['date'               ] = ['',  False]
    self.metadata.data['conference'         ] = ['',  False]
    self.metadata.data['conference_short'   ] = ['',  False]
    self.metadata.data['session'            ] = ['',  False]
    self.metadata.data['session_short'      ] = ['',  False]
    self.metadata.data['max_time'           ] = ['25',False]
    self.metadata.data['total_slides_number'] = ['',  False]
    self.metadata.data['dirs_to_copy'       ] = [[],  False]
    self.metadata.data['toc'                ] = ['',  False]
    self.theme = Theme()
    self.sections = None
    self.toc = TOC()
    self.pos = SlidePosition()
    if source:
      self.__get(source)
    return
  def __str__(self):
    string = 'Presentation preamble\n'
    string += str(self.metadata)
    string += str(self.theme)
    return string
  def __get_metadata(self,source):
    """
    Method for getting the presentation metadata.
    Return the source without the metadata.
    """
    self.metadata.get(source)
    for key,val in self.metadata.data.items():
      if val[1]:
        if (key == 'authors' or
            key == 'authors_short' or
            key == 'emails' or
            key == 'affiliations' or
            key == 'affiliations_short' or
            key == 'dirs_to_copy'):
          self.metadata.data[key] = [ast.literal_eval(str(val[0])),True]
    return self.metadata.strip(source)
  def __get_theme(self,source):
    """
    Method for getting the presentation theme.
    Return the source without the theme.
    """
    self.theme.get(source)
    return self.theme.strip(source)
  def __get_sections(self,source):
    """
    Method for getting the sections contained into the source.
    """
    sections = []
    self.sections = []
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
        slides_number = subsection.get_slides(slides_number=slides_number,theme=self.theme)
    self.metadata.data['total_slides_number'] = slides_number
    for section in self.sections:
      for subsection in section.subsections:
        for slide in subsection.slides:
          slide.data['total_slides_number'] = slides_number
    self.toc.get(sections=self.sections)
    if __config__.is_verbose():
      print('\nTable of Contents')
      print(self.toc)
    return
  def get_css(self):
    """
    Method for creating the css theme.
    The returned string contains the css theme.
    """
    css = self.theme.get_css(only_custom=False)
    if self.sections:
      for section in self.sections:
        if section.subsections:
          for subsection in section.subsections:
            if subsection.slides:
              for slide in subsection.slides:
                css += slide.get_css(only_custom=True)
    return css
  def to_html(self):
    """
    Method for producing and html string document form presentation object.
    """
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
      doc.attr(title = self.metadata.data['title'][0])
      with tag('head'):
        doc.stag('meta',charset='utf-8')
        doc.stag('meta',author=' and '.join(self.metadata.data['authors'][0]))
        with tag('title'):
          text(self.metadata.data['title'][0])
        doc.stag('meta',subtitle=self.metadata.data['subtitle'][0])
        doc.stag('link',rel='stylesheet', href='css/normalize.css')
        doc.stag('link',rel='stylesheet', href='css/theme.css')
      with tag('body',onload="resetCountdown("+self.metadata.data['max_time'][0]+");"):
        with tag('div',id='impress'):
          for section in self.sections:
            for subsection in section.subsections:
              for sld,slide in enumerate(subsection.slides):
                slide.to_html(position = self.pos,
                              doc      = doc,
                              theme    = self.theme.slide,
                              toc      = self.toc.pstr(html=True,current=[section.number,subsection.number,sld+1]))
        with tag('script'):
          doc.attr(src='js/countDown.js')
        with tag('script'):
          doc.attr(src='js/impress.js')
        with tag('script'):
          doc.asis('impress().init();')
    if __config__.is_indented():
      return indent(doc.getvalue())
    else:
      return doc.getvalue()
  def save(self,output):
    """
    Method for saving the html form of presentation into external file.
    """
    with open(output+'index.html','w') as html:
      html.write(self.to_html())
    # copy user defined directories if set
    if len(self.metadata.data['dirs_to_copy'][0])>0:
      for data in self.metadata.data['dirs_to_copy'][0]:
        if os.path.exists(output+data):
          rmtree(output+data)
        copytree(data,output+data)
    # writing css theme
    with open(output+'css/theme.css','w') as css_theme:
      css_theme.writelines(self.get_css())
    return
