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
# modules not in the standard library
from yattag import Doc,indent
# MaTiSSe.py modules
from ..config import __config__
from ..theme.slide.position import Position
from ..theme.theme import Theme
from ..utils.source_editor import __source_editor__ as seditor
from ..utils.source_editor import obfuscate_codeblocks as obfuscate
from ..utils.source_editor import illuminate_protected as illuminate
from .metadata import Metadata
from .regexs import  __regex_section__
from .section import Section
from .slide import Slide
from .subsection import Subsection
from .titlepage import Titlepage
from .toc import TOC
# class definition
class Presentation(object):
  """
  Object for handling the presentation.
  """
  def __init__(self,source=None,defaults=False):
    """
    Parameters
    ----------
    source : str, optional
      string (as single stream) containing the source
    defaults : bool, optional
      flag for activatin the creation of a presentation istance
      having one of each element available with the default
      settings

    Attributes
    ----------
    metadata : Metadata object
      presentation metadata
    theme : Theme object
    sections : list
      list of sections composing the presentation
    toc : TOC object
      presentation Table of Contents
    pos : Position object
      position of the current slide
    """
    self.__reset()
    self.metadata = Metadata()
    self.theme = Theme(defaults=defaults)
    self.sections = None
    self.remainder = None
    self.titlepage = Titlepage()
    self.toc = TOC()
    self.pos = Position()
    if source:
      self.__get(source)
    return

  def __str__(self):
    string = 'Presentation preamble\n'
    string += str(self.metadata)
    string += str(self.theme)
    return string

  def __get_theme(self,source):
    """Method for getting the presentation theme.

    Return the source without the theme.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      source without theme data
    """
    self.theme.get(source)
    return self.theme.strip(source)

  def __get_sections(self,source):
    """Method for getting the sections contained into the source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    sections = []
    self.sections = []
    purged_source = seditor.purge_codes(source)
    for match in re.finditer(__regex_section__,purged_source):
      sections.append([match.group('expr'),match.start(),match.end()])
    if len(sections)==0:
      # there is no section thus crate one with no title as a generic container
      self.sections.append(Section(raw_body=source,data=self.metadata.data.data))
    else:
      for scs,section in enumerate(sections):
        if scs == 0:
          if section[1] != 0:
            self.get_remainder(source,section[1])
        if scs < len(sections)-1:
          raw_body = source[section[2]+1:sections[scs+1][1]]
        else:
          raw_body = source[section[2]+1:]
        self.sections.append(Section(raw_body = raw_body, title = section[0], data = self.metadata.data.data))
    return

  def __get(self,source):
    """Method for getting the presentation from source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    protected, obfuscate_source = obfuscate(source = source)
    strip_source = self.metadata.get(source=obfuscate_source)
    strip_source = self.__get_theme(source=strip_source)
    strip_source = self.titlepage.get(source=strip_source)
    strip_source = illuminate(source=strip_source,protected_contents=protected)
    self.__get_sections(source=strip_source)
    for section in self.sections:
      section.get_subsections()
      for subsection in section.subsections:
        subsection.get_slides(theme=self.theme)
    self.metadata.data.data['total_slides_number'] = [Slide.slides_number,True]
    for section in self.sections:
      for subsection in section.subsections:
        for slide in subsection.slides:
          slide.data['total_slides_number'] = Slide.slides_number
    self.toc.get(sections=self.sections)
    if __config__.verbose:
      print('\nTable of Contents')
      print(self.toc)
    return

  @staticmethod
  def __reset():
    """Method resetting presentation to initial values."""
    Section.reset()
    Slide.reset()
    Subsection.reset()
    return

  def get_remainder(self,source,end_remainder):
    """Method for getting the remainder of the source in case there are data subsections/slides
    before the first section defined, i.e. bad use of sections.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    end_remainder : int
      last character of remainder string into the raw_body
    """
    self.remainder = source[0:end_remainder]
    if __config__.verbose:
      message = ['\nAttention: found a bad usage of "# section" presentation sectioning!']
      message.append('\nThe data:\n"""\n')
      message.append(self.remainder)
      message.append('"""\nis placed before the first section defined')
      message.append('\nThe correct usage is the follwong:')
      message.append('\n1. place the subsection/data slides (e.g. "## subsection ### sllide") after the first defined section;')
      message.append('\n2. not use at all the section partitioning.\n')
      print(''.join(message))
    return

  def get_options(self):
    """Method for getting the available data options."""
    string = ['Presentation metadata']
    string.append(self.metadata.get_options())
    string.append(self.theme.get_options())
    return ''.join(string)

  def get_css(self):
    """Method for creating the css theme.

    The returned string contains the css theme.
    """
    css = self.theme.get_css(only_custom=False)
    if self.titlepage.found:
      css += self.titlepage.get_css(only_custom=True)
    if self.sections:
      for section in self.sections:
        if section.subsections:
          for subsection in section.subsections:
            if subsection.slides:
              for slide in subsection.slides:
                css += slide.get_css(only_custom=True)
    return css

  def to_html(self):
    """Method for producing and html string document from presentation object."""
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
      doc.attr(title = self.metadata.data.data['title'][0])
      with tag('head'):
        doc.stag('meta',charset='utf-8')
        doc.stag('meta',author=' and '.join(self.metadata.data.data['authors'][0]))
        with tag('title'):
          text(self.metadata.data.data['title'][0])
        doc.stag('meta',subtitle=self.metadata.data.data['subtitle'][0])
        doc.stag('link',rel='stylesheet', href='css/normalize.css')
        if __config__.highlight:
          doc.stag('link',rel='stylesheet', href='js/highlight/styles/'+__config__.highlight_style)
        doc.stag('link',rel='stylesheet', href='css/theme.css')
      with tag('body',onload="resetCountdown("+self.metadata.data.data['max_time'][0]+");"):
        with tag('div',id='impress'):
          if self.titlepage.found:
            html = self.titlepage.to_html(position = self.pos, theme = self.theme.slide)
            html = self.metadata.parse(html)
            html = self.toc.parse(html)
            doc.asis(html)
          for section in self.sections:
            for subsection in section.subsections:
              for slide in subsection.slides:
                html = slide.to_html(position = self.pos, theme = self.theme.slide)
                html = self.metadata.parse(html)
                html = self.toc.parse(html,current=[int(slide.data['sectionnumber']),int(slide.data['subsectionnumber']),slide.number])
                doc.asis(html)
        with tag('script'):
          doc.attr(src='js/countDown.js')
        with tag('script'):
          doc.attr(src='js/impress.js')
        with tag('script'):
          doc.asis('impress().init();')
        if __config__.online_mathjax:
          with tag('script'):
            doc.attr(('type','text/javascript'))
            doc.attr(src='http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML')
        else:
          with tag('script'):
            doc.attr(('type','text/x-mathjax-config'))
            doc.text("""
              MathJax.Hub.Config({
                extensions: ["tex2jax.js"],
                jax: ["input/TeX", "output/HTML-CSS"],
                tex2jax: {
                  inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                  displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
                  processEscapes: true
                },
                "HTML-CSS": { availableFonts: ["Neo-Euler"] }
              });
            """)
          with tag('script'):
            doc.attr(('type','text/javascript'))
            doc.attr(src='js/MathJax/MathJax.js')
        if __config__.highlight:
          with tag('script'):
            doc.attr(src='js/highlight/highlight.pack.js')
          with tag('script'):
            doc.text("""hljs.initHighlightingOnLoad();""")
    if __config__.indented:
      return indent(doc.getvalue())
    else:
      return doc.getvalue()

  def save(self,output):
    """Method for saving the html form of presentation into external file.

    Parameters
    ----------
    output : str
      output path
    """
    with open(output+'index.html','w') as html:
      html.write(self.to_html())
    # copy user defined directories if set
    if len(self.metadata.data.data['dirs_to_copy'][0])>0:
      for data in self.metadata.data.data['dirs_to_copy'][0]:
        if os.path.exists(output+data):
          rmtree(output+data)
        copytree(data,output+data)
    # writing css theme
    with open(output+'css/theme.css','w') as css_theme:
      css_theme.writelines(self.get_css())
    return
