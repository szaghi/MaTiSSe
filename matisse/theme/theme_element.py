#!/usr/bin/env python
"""
theme_element.py, module definition of ThemeElement class.
This is a base class for building the presentation Theme.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import ast
import re
# MaTiSSe.py modules
from ..data.data import Data
from ..utils.utils import  __regex_over_slide_theme__
# class definition
class ThemeElement(object):
  """
  Object for handling a theme element.
  """
  def __init__(self, data_tag, special_keys = None, class_name = None):
    """
    Parameters
    ----------
    data_tag : str
      tag name enclosing the data
    special_keys : list, optional
      list of special entries that must be handled differently from the standard ones
    class_name : str, optional
      name of the 'css class' corresponding to the theme element

    Attributes
    ----------
    data_tag: str
      tag name enclosing the data
    data: Data object
    class_name : str
      name of the 'css class' corresponding to the theme element
    active : bool
      flag for inquiring if the current theme element is active or not
    """
    _special_keys = ['elements','active']
    if special_keys:
      for key in special_keys:
        _special_keys.append(key)
    self.data_tag     = data_tag
    self.data         = Data(regex_start=r'[-]{3}'+data_tag,regex_end=r'[-]{3}end'+data_tag,skip=__regex_over_slide_theme__,special_keys=_special_keys)
    self.class_name   = class_name
    self.active       = True
    self.data.data['width'        ] = ['',                            False]
    self.data.data['height'       ] = ['',                            False]
    self.data.data['background'   ] = ['white',                       False]
    self.data.data['border'       ] = ['0',                           False]
    self.data.data['border-radius'] = ['0 0 0 0',                     False]
    self.data.data['color'        ] = ['black',                       False]
    self.data.data['font'         ] = ['',                            False]
    self.data.data['font-size'    ] = ['100%',                        False]
    self.data.data['font-family'  ] = ['Open Sans, Arial, sans-serif',False]
    self.data.data['elements'     ] = [[],                            False]
    self.data.data['active'       ] = [True,                          False]
    return

  def __str__(self):
    string = ''
    if self.active:
      string = str(self.data)
    return string

  def get(self,source):
    """Method for getting raw data from source.
    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    self.data.get(source)
    return

  def set_from(self,other):
    """Method for setting theme using data of other (theme element).

    Parameters
    ----------
    other : ThemeElement object
    """
    if other.active:
      for key,val in self.data.data.items():
        if not val[1]:
          if key in other.data.data:
            self.data.data[key] = other.data.data[key]
      self.check_specials()
    return

  def check_specials(self):
    """
    Method for checking special data entries.
    All theme elements have the following special entries:
    1. elements
    2. active
    Other particular special entries must be handled into the subclass method.
    """
    for key,val in self.data.data.items():
      if val[1]:
        if key == 'elements':
          self.data.data[key] = [ast.literal_eval(str(val[0])),True]
        elif key == 'active':
          self.active = ast.literal_eval(str(val[0]))
          self.data.data[key] = [self.active,True]
    return

  def get_css(self,only_custom=False,as_list=False):
    """
    Method for getting css from data.

    Parameters
    ----------
    only_custom : bool, optional
      consider only the (user) customized data
    as_list : bool, optional
      return a list instead of a string

    Returns
    -------
    str
      a string containing the css code of the element if as_list = False
    list
      a list of one string containing the css code of the element if as_list = True
    """
    if as_list:
      return [self.data.get_css(only_custom=only_custom)]
    else:
      return self.data.get_css(only_custom=only_custom)

  def strip(self,source):
    """Method for striping theme element data from source.

    Parameters
    ----------
    source : str

    Returns
    -------
    str
      source without the theme element data
    """
    return self.data.strip(source)

  def put_elements(self,doc,metadata,toc=None):
    """Method for putting defined elements into the current theme element.

    Parameters
    ----------
    doc : yattag.Doc object
      the currently open yattag.Doc object
    metadata: Data object
    toc: TOC object, optional
    -------
    str
    """
    if 'elements' in self.data.data:
      for element in self.data.data['elements'][0]:
        if isinstance(element,list):
          elem = element[0]
          style = element[1]
        else:
          elem = element
          style = None
        custom = re.search(r'\|custom\|',elem)
        if elem in metadata or custom or elem == 'timer':
          if elem == 'logo':
            if style:
              doc.stag('img',src=metadata[elem],alt=metadata[elem],style=style)
            else:
              doc.stag('img',src=metadata[elem],alt=metadata[elem])
          elif elem == 'timer':
            with doc.tag('span',klass='timercontainer'):
              if style:
                doc.attr(style=style)
              else:
                doc.attr(style='')
              with doc.tag('div',klass='countDown'):
                with doc.tag('div'):
                  doc.attr(klass='timer')
                if style:
                  if 'controls' in style:
                    with doc.tag('div',klass='timercontrols'):
                      with doc.tag('input',type='button'):
                        doc.attr(klass='btn reset',onclick='resetCountdown('+metadata['max_time']+');',value=' &#10227; ',title='reset')
                      with doc.tag('input',type='button'):
                        doc.attr(klass='btn stop',onclick='stopCountdown();',value=' &#9724; ',title='pause')
                      with doc.tag('input',type='button'):
                        doc.attr(klass='btn start',onclick='startCountdown();',value=' &#9654; ',title='start')
          else:
            with doc.tag('span'):
              if style:
                doc.attr(('style',style))
              if custom:
                doc.asis(re.sub(r'\|custom\|','',elem))
              else:
                if elem == 'toc':
                  if toc:
                    value = toc
                elif isinstance(metadata[elem],list):
                  value = ' , '.join(metadata[elem])
                else:
                  value = str(metadata[elem])
                doc.asis(value)
    return

  def to_html(self,doc,style=None,padding=None,content=None,metadata=None,toc=None):
    """
    Method for inserting element contents into html.

    Parameters
    ----------
    doc : yattag.Doc object
      the currently open yattag.Doc object
    style: str, optional
      particular element style
    padding: bool, optional
      activate internal element padded container
    content: str, optional
      content of the element as raw string
    metadata: Data object
    toc: str, optional
      str(toc), toc being a TOC object
    """
    if self.active:
      if content or metadata:
        with doc.tag('div'):
          if self.class_name:
            doc.attr(klass=self.class_name)
          if style:
            doc.attr(style=style)
          if padding:
            with doc.tag('div',klass='padding',style='padding:'+padding+';'):
              if content:
                doc.asis(content)
              if metadata:
                self.put_elements(doc=doc,metadata=metadata,toc=toc)
          else:
            if content:
              doc.asis(content)
            if metadata:
              self.put_elements(doc=doc,metadata=metadata,toc=toc)
    return
