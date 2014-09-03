#!/usr/bin/env python
"""
slide.py, module definition of Slide class.
This defines a slide of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import sys
# modules not in the standard library
try:
  import markdown
  #__md__ = markdown.Markdown(output_format='html5',extensions=['fenced_code','footnotes','tables','smart_strong','codehilite(noclasses=True,pygments_style=vim)','toc'])
  #__md__ = markdown.Markdown(output_format='html5',extensions=['fenced_code','footnotes','tables','smart_strong','codehilite','toc'])
  __md__ = markdown.Markdown(output_format='html5',extensions=['fenced_code','footnotes','tables','smart_strong'])
except ImportError :
  sys.stderr.write("Error: can't import module 'markdown'")
  sys.exit(1)
# MaTiSSe.py modules
#from .rawdata import Rawdata
# class definition
class Slide(object):
  """
  Slide is an object that handles a single slide, its attributes and methods.
  """
  def __init__(self,raw_body='',number=0,title='',data=None):
    self.raw_body = raw_body
    self.number   = number
    self.title    = title
    self.data     = OrderedDict()
    if data:
      for key,val in data.items():
        self.data[key] = val
    self.data['slidetitle' ] = self.title
    self.data['slidenumber'] = str(self.number)

    #self.override_data=Rawdata(regex_start=r'[-]{3}slide',regex_end=r'[-]{3}endslide')
    #self.override_data.get(raw_body)
    #if self.override_data.data:
    #  for odata in self.override_data.data:
    #    key = odata[0].strip()
    #    val = odata[1].strip()
    #    if key == 'slide-transition':
    #      self.theme.slide.data[key] = val
    #    else:
    #      self.theme.slide.content.data[key] = val
    return
  def to_html(self,tag,doc,theme):
    """
    Method for converting slide content into html format.
    """
    # append to the css theme the overriding styles
    #if self.override_data.data:
    #  sss = '#slide-'+str(self.number)+' .slide-content {\n' # special slide styles
    #  for key,val in self.theme.slide.content.data.items():
    #    if key != 'padding':
    #      sss += '  '+key+': '+val+';\n'
    #  sss += '}\n'
    #  engine.put_sss(sss)
    with tag('div'):
      doc.attr(('id','slide-'+str(self.number)))
      doc.attr(('class','step slide'))
      doc.attr(('title',self.title))
      doc.attr(('sectiontitle',self.data['sectiontitle']))
      doc.attr(('sectionnumber',self.data['sectionnumber']))
      if theme.data['slide-transition'] == 'horizontal':
        offset = int(theme.data['width'].strip('px'))
        doc.attr(('data-x',str(self.number+self.number*offset*1.01)))
      elif theme.data['slide-transition'] == 'vertical':
        offset = int(theme.data['height'].strip('px'))
        doc.attr(('data-y',str(self.number+self.number*offset*1.01)))
      # headers
      for header in theme.headers:
        header.to_html(tag=tag,doc=doc,elements=self.data)
      # left sidebars
      for sidebar in theme.sidebars:
        if sidebar.position == 'L':
          sidebar.to_html(tag=tag,doc=doc,elements=self.data)
      # slide content
      theme.content.to_html(tag=tag,doc=doc,content='\n'+__md__.convert(self.raw_body),elements=self.data)
      # right sidebars
      for sidebar in theme.sidebars:
        if sidebar.position == 'R':
          sidebar.to_html(tag=tag,doc=doc,elements=self.data)
      # footers
      for footer in theme.footers:
        footer.to_html(tag=tag,doc=doc,elements=self.data)
    return
