#!/usr/bin/env python
"""
theme_element.py, module definition of ThemeElement class.
This is a base class for building the presentation Theme.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import copy
import re
# MaTiSSe.py modules
from ..utils.rawdata import Rawdata
# class definition
class ThemeElement(object):
  """
  Object for handling a theme element.
  """
  def __init__(self,
               data_tag): # tag enclosing the data settings
    self.raw_data = Rawdata(regex_start=r'[-]{3}'+data_tag,regex_end=r'[-]{3}end'+data_tag)
    self.data     = None
    self.css      = ''
    self.padding  = None
    self.position = None
    self.active   = True
    return
  def __str__(self):
    string = []
    if self.active:
      if self.data:
        string = [ '  '+k+' = '+str(v)+'\n' for k,v in self.data.items()]
    return ''.join(string)
  def __deepcopy__(self):
    return copy.deepcopy(self)
  def get_raw_data(self,source):
    """
    Method for getting raw data from source.
    """
    self.raw_data.get(source)
    return
  def get_data(self,source):
    """
    Method for getting data values from raw data parsed from source.
    The self.data dictionary must be previously created with defaults value:
    only items previously defined obtain a value from raw data.
    """
    self.get_raw_data(source)
    if self.raw_data.data:
      if self.data:
        for data in self.raw_data.data:
          key = data[0].strip()
          val = data[1].strip()
          if key in self.data:
            if key == 'padding':
              self.padding = val
            elif key == 'position':
              self.position = val
              self.data[key] = val
            elif isinstance(self.data[key], str):
              self.data[key] = val
            elif isinstance(self.data[key], list) or isinstance(self.data[key], bool):
              self.data[key] = eval(val)
      else:
        pass
    return
  def get_css(self):
    """
    Method for setting css theme element values accordingly to the element data.
    """
    css = self.css
    if self.active:
      for key,val in self.data.items():
        if key != 'elements' and key != 'position' and key !='padding' and key != 'slide-transition': # special keys
          css += '\n  '+key+': '+val+';'
      css += '\n}\n'
    return css
  def activate(self):
    """
    Method for activating the element.
    """
    self.active = True
    return
  def deactivate(self):
    """
    Method for deactivating the element.
    """
    self.active = False
    return
  def strip(self,source):
    """
    Method for striping theme element raw data from source.
    """
    strip_source = self.raw_data.strip(source)
    return strip_source
  def put_elements(self,tag,doc,elements):
    """
    Method for putting defined elements into the current theme element.
    """
    if 'elements' in self.data:
      for element in self.data['elements']:
        if isinstance(element,list):
          elem = element[0]
          style = element[1]
        else:
          elem = element
          style = None
        custom = re.search(r'\|custom\|',elem)
        if elem in elements or custom or elem == 'timer':
          if elem == 'logo':
            if style:
              doc.stag('img',src=elements[elem],alt=elements[elem],style=style)
            else:
              doc.stag('img',src=elements[elem],alt=elements[elem])
          elif elem == 'timer':
            with tag('span',klass='timercontainer'):
              if style:
                doc.attr(style=style)
              else:
                doc.attr(style='')
              with tag('div',klass='countDown'):
                with tag('div'):
                  doc.attr(klass='timer')
                if style:
                  if 'controls' in style:
                    with tag('div',klass='timercontrols'):
                      with tag('input',type='button'):
                        doc.attr(klass='btn reset',onclick='resetCountdown('+elements['max_time']+');',value=' &#10227; ',title='reset')
                      with tag('input',type='button'):
                        doc.attr(klass='btn stop',onclick='stopCountdown();',value=' &#9724; ',title='pause')
                      with tag('input',type='button'):
                        doc.attr(klass='btn start',onclick='startCountdown();',value=' &#9654; ',title='start')
          else:
            with tag('span'):
              if style:
                doc.attr(('style',style))
              if custom:
                doc.asis(re.sub(r'\|custom\|','',elem))
              else:
                if isinstance(elements[elem],list):
                  value = ' , '.join(elements[elem])
                else:
                  value = str(elements[elem])
                doc.asis(value)
    return
  def to_html(self,tag,doc,class_name,padding=None,style=None,content=None,elements=None):
    """
    Method for inserting element contents into html.
    """
    if self.active:
      with tag('div',('class',class_name)):
        if style:
          doc.attr(style=style)
        if padding:
          with tag('div',klass='padding',style='padding:'+padding+';'):
            if content:
              doc.asis(content)
            if elements:
              self.put_elements(tag,doc,elements)
        else:
          if content:
            doc.asis(content)
          if elements:
            self.put_elements(tag,doc,elements)
    return
