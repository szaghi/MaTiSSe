#!/usr/bin/env python
"""
toc.py, module definition of TOC class.
This defines the Table of Contents of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import sys
# modules not in the standard library
try:
  from yattag import Doc
except ImportError :
  sys.stderr.write("Error: can't import module 'yattag'")
  sys.exit(1)
# class definition
class TOC(object):
  """
  Object handling the table of contents of presntation.
  """
  def __init__(self,deep=3):
    self.sections = []
    self.deep = deep
    return
  def __str__(self):
    return self.pstr()
  def pstr(self,html=False,current=None,deep=None):
    """Method powering __str__ obtaining a customizable pretty printer.
    Parameters
    ----------
    html: bool, optional
      activate html tags
    current: list, optional
      list containing current section, subsection and slide number used
      for highlighting current slide into the TOC
    deep: {3,2,1}
      control the depth of printed TOC: 1 consider only sections, 2 consider
      sections and subsections and 3 consider sections, subsections and slides
    """
    def get_section(section,html=None,current=None):
      """Helper function for pretty print section.
      Parameters
      ----------
      section: list
        section data
      html: bool, optional
        activate html tags
      current: list, optional
        list containing current section, subsection and slide number used
        for highlighting current slide into the TOC
      """
      if html:
        doc, tag, text = Doc().tagtext()
        with tag('span',klass='toc-section'):
          if current and current[0] == section[0]:
            with tag('span',klass='toc-section emph'):
              text(str(section[0])+' '+section[1])
          else:
            text(str(section[0])+' '+section[1])
        string = '\n'+doc.getvalue()
      else:
        string = '\n'+str(section[0])+' '+section[1]
      return string
    def get_subsection(section,subsection,html=None,current=None):
      """Helper function for pretty print subsection.
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
      """
      if html:
        doc, tag, text = Doc().tagtext()
        with tag('span',klass='toc-subsection'):
          if current and current[0] == section[0] and current[1] == subsection[0]:
            with tag('span',klass='toc-subsection emph'):
              text('  '+str(section[0])+'.'+str(subsection[0])+' '+subsection[1])
          else:
            text('  '+str(section[0])+'.'+str(subsection[0])+' '+subsection[1])
        string = '\n'+doc.getvalue()
      else:
        string = '\n'+'  '+str(section[0])+'.'+str(subsection[0])+' '+subsection[1]
      return string
    def get_slide(section,subsection,slide,html=None,current=None):
      """Helper function for pretty print subsection.
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
      """
      if html:
        doc, tag, text = Doc().tagtext()
        with tag('span',klass='toc-slide'):
          if current and current[0] == section[0] and current[1] == subsection[0] and current[2] == slide[2]:
            with tag('span',klass='toc-slide emph'):
              text('    '+str(section[0])+'.'+str(subsection[0])+'.'+str(slide[2])+' '+slide[1])
          else:
            text('    '+str(section[0])+'.'+str(subsection[0])+'.'+str(slide[2])+' '+slide[1])
        string = '\n'+doc.getvalue()
      else:
        string = '\n'+'    '+str(section[0])+'.'+str(subsection[0])+'.'+str(slide[2])+' '+slide[1]
      return string
    # starting printing TOC
    deep = deep
    if not deep:
      deep = self.deep
    string = ''
    for section in self.sections:
      string += get_section(section=section,html=html,current=current)
      if deep > 1:
        for subsection in section[2]:
          string += get_subsection(section=section,subsection=subsection,html=html,current=current)
          if deep > 2:
            for slide in subsection[2]:
              string += get_slide(section=section,subsection=subsection,slide=slide,html=html,current=current)
    return string
  def get(self,sections):
    """
    Method for building TOC from presentation sections.
    """
    for sec,section in enumerate(sections):
      self.sections.append([ section.number,section.title,[] ])
      for sub,subsection in enumerate(section.subsections):
        self.sections[sec][2].append([ subsection.number,subsection.title,[] ])
        for sld,slide in enumerate(subsection.slides):
          self.sections[sec][2][sub][2].append([ slide.number,slide.title,sld+1 ])
    return
