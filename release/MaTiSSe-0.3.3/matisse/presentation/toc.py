#!/usr/bin/env python
"""
toc.py, module definition of TOC class.
This defines the Table of Contents of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
# modules not in the standard library
from yattag import Doc
# global variables
# regular expressions
__retoc__ = re.compile(r"\$toc(\((?P<deep>[1-3])\))*",re.DOTALL)
# class definition
class TOC(object):
  """
  Object handling the table of contents of presntation.
  """
  def __init__(self,deep=3):
    """
    Parameters
    ----------
    deep : {1,2,3}, optional
      depth of printed TOC; 1 => print only sections, 2 => print sections and subsections, 3=> print sections, subsections and slides

    Attributes
    ----------
    sections : list
      list of sections with the following form
      sections = [ #section_number, 'section title', [list of subsections], #slide_number_at_which_section_starts ];
      the subsections list has the following form
      subsections = [ #subsection_number, 'subsection title', [list of slides], #local_subsection_number, #slide_number_at_which_subsection_starts ];
      the slides list has the following form
      subsections = [ #slide_number, 'slide title', #local_slide_number ];
    deep : {1,2,3}
      depth of printed TOC; 1 => print only sections, 2 => print sections and subsections, 3=> print sections, subsections and slides
    """
    self.sections = []
    self.deep = deep
    return

  def __str__(self):
    return self.pstr()

  @staticmethod
  def print_section(section,html=False,current=None):
    """Method for printing section data.

    Parameters
    ----------
    section: list
      section data
    html: bool, optional
      activate html tags
    current: list, optional
      list containing current section, subsection and slide number used
      for highlighting current slide into the TOC

    Returns
    -------
    str
      string containing the pretty printed section data
    """
    if html:
      doc, tag, text = Doc().tagtext()
      with tag('a',href='#slide-'+str(section[3])):
        if current and current[0] == section[0]:
          with tag('span',klass='toc-section emph'):
            text(str(section[0])+' '+section[1])
        else:
          with tag('span',klass='toc-section'):
            text(str(section[0])+' '+section[1])
      string = '\n'+doc.getvalue()
    else:
      string = '\n'+str(section[0])+' '+section[1]
    return string

  @staticmethod
  def print_subsection(section,subsection,html=False,current=None):
    """Method for printing subsection data.

    Parameters
    ----------
    section: list
      section data
    subsection: list
      subsection data
    html: bool, optional
      activate html tags
    current: list, optional
      list containing current section, subsection and slide number used
      for highlighting current slide into the TOC

    Returns
    -------
    str
      string containing the pretty printed subsection data
    """
    if html:
      doc, tag, text = Doc().tagtext()
      with tag('a',href='#slide-'+str(subsection[4])):
        if current and current[0] == section[0] and current[1] == subsection[0]:
          with tag('span',klass='toc-subsection emph'):
            text('  '+str(section[0])+'.'+str(subsection[3])+' '+subsection[1])
        else:
          with tag('span',klass='toc-subsection'):
            text('  '+str(section[0])+'.'+str(subsection[3])+' '+subsection[1])
      string = '\n'+doc.getvalue()
    else:
      string = '\n'+'  '+str(section[0])+'.'+str(subsection[3])+' '+subsection[1]
    return string

  @staticmethod
  def print_slide(section,subsection,slide,html=False,current=None):
    """Method for printing slideta.

    Parameters
    ----------
    section: list
      section data
    subsection: list
      subsection data
    slide: list
      slide data
    html: bool, optional
      activate html tags
    current: list, optional
      list containing current section, subsection and slide number used
      for highlighting current slide into the TOC

    Returns
    -------
    str
      string containing the pretty printed slide data
    """
    if html:
      doc, tag, text = Doc().tagtext()
      with tag('a',href='#slide-'+str(slide[0])):
        if current and current[0] == section[0] and current[1] == subsection[0] and current[2] == slide[0]:
          with tag('span',klass='toc-slide emph'):
            text('    '+str(section[0])+'.'+str(subsection[3])+'.'+str(slide[2])+' '+slide[1])
        else:
          with tag('span',klass='toc-slide'):
            text('    '+str(section[0])+'.'+str(subsection[3])+'.'+str(slide[2])+' '+slide[1])
      string = '\n'+doc.getvalue()
    else:
      string = '\n'+'    '+str(section[0])+'.'+str(subsection[3])+'.'+str(slide[2])+' '+slide[1]
    return string

  def pstr(self,html=False,current=None,deep=None):
    """Method powering __str__ obtaining a customizable pretty printer.

    Parameters
    ----------
    html: bool, optional
      activate html tags
    current: list, optional
      list containing current section, subsection and slide number used
      for highlighting current slide into the TOC
    deep : {1,2,3}, optional
      depth of printed TOC; 1 => print only sections, 2 => print sections and subsections, 3=> print sections, subsections and slides
    """
    deep = deep
    if not deep:
      deep = self.deep
    string = ''
    for section in self.sections:
      string += self.print_section(section=section,html=html,current=current)
      if deep > 1:
        for subsection in section[2]:
          string += self.print_subsection(section=section,subsection=subsection,html=html,current=current)
          if deep > 2:
            for slide in subsection[2]:
              string += self.print_slide(section=section,subsection=subsection,slide=slide,html=html,current=current)
    return string

  def get(self,sections):
    """
    Method for building TOC from presentation sections.
    """
    for sec,section in enumerate(sections):
      self.sections.append([ int(section.number),section.title,[],0 ])
      for sub,subsection in enumerate(section.subsections):
        self.sections[sec][2].append([ int(subsection.number),subsection.title,[],int(subsection.local_number),0 ])
        for slide in subsection.slides:
          self.sections[sec][2][sub][2].append([ int(slide.number),slide.title,int(slide.local_number) ])
          if slide.data['first_of_sec']:
            self.sections[sec][3] = slide.number
          if slide.data['first_of_subsec']:
            self.sections[sec][2][sub][4] = slide.number
    return

  def parse(self, source, current=None):
    """Method for substituting $toc with its pretty printed version.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    current: list, optional
      list containing current section, and subsection number used
      for highlighting current slide into the TOC
    """
    parsed_source = source
    for match in re.finditer(__retoc__, parsed_source):
      deep = match.group('deep')
      if deep:
        deep = int(deep)
      doc = Doc()
      with doc.tag('div', klass='toc'):
        doc.asis(self.pstr(html=True, current=current, deep=deep))
      parsed_source = re.sub(__retoc__, lambda x: doc.getvalue(), parsed_source, 1)
      doc = None
    return parsed_source
