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
from ..utils.source_editor import __source_editor__
# class definition
class ThemeElement(object):
  """
  Object for handling a theme element.
  """
  def __init__(self, data_tag, skip = None, special_keys = None, class_name = None):
    """
    Parameters
    ----------
    data_tag : str
      tag name enclosing the data
    skip : list, optional
      list of re.compile (compiled regular expression) of block to be skipped
    special_keys : list, optional
      list of special entries that must be handled differently from the standard ones
    class_name : str, optional
      name of the 'css class' corresponding to the theme element
    set_all_custom : bool, optional
      set all option as customized from users (useful for plain slides theme)

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
    _skip = [__source_editor__.regex_overtheme,__source_editor__.regex_codeblock,__source_editor__.regex_codeinline]
    if skip:
      for skp in skip:
        _skip.append(skp)
    _special_keys = ['metadata','active']
    if special_keys:
      for key in special_keys:
        _special_keys.append(key)
    self.data_tag     = data_tag
    self.data         = Data(regex_start=r'[-]{3}'+data_tag,regex_end=r'[-]{3}end'+data_tag,
                             skip=_skip,special_keys=_special_keys)
    self.class_name   = class_name
    self.active       = True
    self.data.data['metadata'] = [[],  False]
    self.data.data['active'  ] = [True,False]
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

    >>> elem = ThemeElement('header')
    >>> source = '---header option1 = val1 ---endheader'
    >>> elem.get(source)
    >>> elem.data.data['option1'][0]
    'val1'
    """
    self.data.get(source)
    return

  def set_from(self,other):
    """Method for setting theme using data of other (theme element).

    Parameters
    ----------
    other : ThemeElement object

    >>> elem1 = ThemeElement('header')
    >>> elem1.data.data['option1'] = ['unset',False]
    >>> elem2 = ThemeElement('header')
    >>> source = '---header option1 = val1 ---endheader'
    >>> elem2.get(source)
    >>> elem1.set_from(elem2)
    >>> elem1.data.data['option1'][0]
    'val1'
    """
    if other.active:
      for key,val in self.data.data.items():
        if not val[1]:
          if key in other.data.data:
            self.data.data[key] = other.data.data[key]
      self.check_specials()
    return

  def set_all_custom(self):
    """Method for setting all data as customized by user (useful for plain slides theme).

    >>> elem = ThemeElement('header')
    >>> elem.data.data['option1'] = ['unset',False]
    >>> elem.set_all_custom()
    >>> elem.data.data['option1'][1]
    True
    """
    self.data.set_all_custom()
    return

  def check_specials(self):
    """
    Method for checking special data entries.
    All theme elements have the following special entries:
    1. metadata
    2. active
    Other particular special entries must be handled into the subclass method.

    >>> elem = ThemeElement('header')
    >>> source = '---header metadata = ["slidetitle"] \\n active = False---endheader'
    >>> elem.get(source)
    >>> eval(elem.data.data['metadata'][0])[0]
    'slidetitle'
    """
    for key,val in self.data.data.items():
      if val[1]:
        if key == 'metadata':
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

    >>> elem = ThemeElement('header',class_name='header')
    >>> source = '---header height = 10% ---endheader'
    >>> elem.get(source)
    >>> elem.get_css(only_custom=True)
    '\\n.header {\\n  height: 10%;\\n}\\n'
    """
    if self.class_name:
      css = '\n.'+self.class_name+' {'+self.data.get_css(only_custom=only_custom)+'\n}\n'
    else:
      css = self.data.get_css(only_custom=only_custom)
    if as_list:
      return [css]
    else:
      return css

  def strip(self,source):
    """Method for striping theme element data from source.

    Parameters
    ----------
    source : str

    Returns
    -------
    str
      source without the theme element data

    >>> elem = ThemeElement('header')
    >>> source = 'other contents before---header height = 10% ---endheader,other contents after'
    >>> elem.get(source)
    >>> elem.data.data['height'][0]
    '10%'
    >>> elem.strip(source)
    'other contents before,other contents after'
    """
    return self.data.strip(source)

  @staticmethod
  def put_logo(doc,metadata,style):
    """Method for putting logo element.

    Parameters
    ----------
    doc : yattag.Doc object
      the currently open yattag.Doc object
    metadata : OrderedDict object
      dictionary of metadata
    style : str
      style applied to element
    """
    if style:
      doc.stag('img',src=metadata['logo'],alt=metadata['logo'],style=style)
    else:
      doc.stag('img',src=metadata['logo'],alt=metadata['logo'])
    return

  @staticmethod
  def put_timer(doc,metadata,style):
    """Method for putting timer element.

    Parameters
    ----------
    doc : yattag.Doc object
      the currently open yattag.Doc object
    metadata : OrderedDict object
      dictionary of metadata
    style : str
      style applied to element
    """
    with doc.tag('span',klass='timercontainer'):
      if style:
        doc.attr(style=style)
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
    return

  @staticmethod
  def put_toc(doc,style,deep):
    """Method for putting TOC element.

    Parameters
    ----------
    doc : yattag.Doc object
      the currently open yattag.Doc object
    style : str
      style applied to element
    deep : int
      depth of Table of Contents
    """
    with doc.tag('div'):
      if style:
        doc.attr(('style',style))
      doc.asis('$toc('+str(deep)+')')
    return

  def put_metadata(self,doc,metadata):
    """Method for putting metadata elements into the current theme element.

    Parameters
    ----------
    doc : yattag.Doc object
      the currently open yattag.Doc object
    metadata : OrderedDict object
      dictionary of metadata
    """
    for element in self.data.data['metadata'][0]:
      elem = element
      style = None
      deep = 1
      if isinstance(element,list):
        elem = element[0]
        style = element[1]
        if len(element)>=3:
          deep = element[2]
      if elem == 'logo' and elem in metadata:
        self.put_logo(doc=doc,metadata=metadata,style=style)
      elif elem == 'timer' and 'max_time' in metadata:
        self.put_timer(doc=doc,metadata=metadata,style=style)
      elif elem == 'toc':
        self.put_toc(doc=doc,style=style,deep=deep)
      else:
        custom = re.search(r'\|custom\|',elem)
        with doc.tag('div'):
          style_txt = 'float:left;'
          if style:
            style_txt += style
          doc.attr(('style',style_txt))
          if custom:
            doc.asis(re.sub(r'\|custom\|','',elem))
          elif elem in metadata:
            if isinstance(metadata[elem],list):
              value = ' , '.join(metadata[elem])
            else:
              value = str(metadata[elem])
            doc.asis(value)
    return

  def to_html(self,doc,style=None,content=None,metadata=None):
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
    metadata : OrderedDict object
      dictionary of metadata
    """
    if self.active:
      if content or metadata:
        with doc.tag('div'):
          if self.class_name:
            doc.attr(klass=self.class_name)
          if style:
            doc.attr(style=style)
          if content:
            doc.asis(content)
          if metadata:
            self.put_metadata(doc=doc,metadata=metadata)
    return
