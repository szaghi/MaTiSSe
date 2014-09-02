#!/usr/bin/env python
"""
toc.py, module definition of TOC class.
This defines the Table of Contents of the presentation.
"""
# class definition
class TOC(object):
  """
  Object handling the table of contents of presntation.
  """
  def __init__(self,sections):
    self.data = []
    for section in sections:
      pass
      #self.data.append([section.number,section.title,[ [subsection.number,subsection.title, [ [slide.number,slide.title] for slide in subsection.slides]] for subsection in section.subsections ]])
    return
  def __str__(self):
    string = '\n'
    #for section in self.data:
    #  if section[0]>0:
    #    string += section[1]+'\n'
    #  for subsection in section[2]:
    #    if subsection[0]>0:
    #      string += '  '+subsection[1]+'\n'
    #    for slide in subsection[2]:
    #      string += '  '*2+'<a href="#slide-'+str(slide[0])+'" title="'+str(slide[0])+'">'+str(slide[0])+'</a>'+' '+slide[1]+'\n'
    return string
