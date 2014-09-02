#!/usr/bin/env python
"""
theme_element.py, module definition of ThemeElement class.
This a base class for building the presentation Theme.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import copy
import re
# class definition
class ThemeElement(object):
  """
  Object for handling a theme element.
  """
  def __init__(self,
               raw_data,       # raw data extracted from source
               data,           # dictionary containing data of element
               css,            # css skeleton
               padding = None, # element content padding
               active = True): # element is active or not
    self.raw_data = raw_data
    self.data     = data
    self.css      = css
    self.padding  = padding
    self.active   = active
    return
  def __str__(self):
    string = []
    if self.active:
      if self.data:
        string = [ '  '+k+' = '+str(v)+'\n' for k,v in self.data.items()]
    return ''.join(string)
  def __deepcopy__(self):
    return ThemeElement(raw_data = copy.deepcopy(self.raw_data),
                        data     = copy.deepcopy(self.data),
                        css      = copy.deepcopy(self.css),
                        padding  = copy.deepcopy(self.padding),
                        active   = copy.deepcopy(self.active))
  def get_raw_data(self,source):
    """
    Method for getting raw data from source.
    """
    self.raw_data.get(source)
    return
  def get_values(self):
    """
    Method for getting values from raw data parsed from source.
    """
    for data in self.raw_data.data:
      key = data[0].strip()
      val = data[1].strip()
      if key in self.data:
        if key == 'padding': #special case for padding
          self.padding = val
          self.data[key] = val
        elif isinstance(self.data[key], str):
          self.data[key] = val
        elif isinstance(self.data[key], list) or isinstance(self.data[key], bool):
          self.data[key] = eval(val)
      else:
        self.data[key] = val
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
