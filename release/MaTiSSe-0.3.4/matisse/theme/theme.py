#!/usr/bin/env python
"""
theme.py, module definition of Theme class.
This defines the theme of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import re
# MaTiSSe.py modules
from .box import Box
from .canvas import Canvas
from .figure import Figure
from .heading import Heading
from .note import Note
from .selector import Selector
from .slide.slide import Slide
from .table import Table
from .toc import TOC
from ..utils.source_editor import __source_editor__
# global variables
# default theme settings
__p_css__ = {'p': '\n  padding: 1% 0;'}
__a_css__ = {'a': '\n  color: inherit;\n  text-decoration: none;\n  transition: 0.5s;',
             'a:hover, a:focus': '\n  background: rgba(255,255,255,1);\n  text-shadow: -1px -1px 2px rgba(100,100,100,0.5);'}
__ul_css__ = {'ul': '\n  padding-left: 2em;'}
__ol_css__ = {'ol': '\n  padding-left: 2em;'}
__pre_css__ = {'pre': '\n  display:flex;\n  padding: 1% 0;'}
__columns_css__ = {'.columns:after': '\n  visibility: hidden;\n  content:" ";\n  clear: both;\n display: block;'}
__input_btn_css__ = {'input[type=button]': '\n  padding:0;\n  margin:0;\n  border:0 none;\n  background: rgba(0,0,0,0.01);'}
__countDown_css__ = {'.countDown': '\n  display: block;\n  padding: 0;\n  margin: 0;'}
__timer_css__ = {'.timer': '\n  display:table-row;',
                 '.timercontrols': '\n  display:table-row;'}
__impress_css__ = {'.step': '\n  position: relative;',
                   '.impress-enabled .step': '\n  margin: 0; \n  opacity: 0.3; \n  -webkit-transition: opacity 1s; \n  -moz-transition: opacity 1s; \n  -ms-transition: opacity 1s; \n  -o-transition: opacity 1s; \n  transition: opacity 1s;',
                   '.impress-enabled .step.active': '\n  opacity: 1;'}
__table_css__ = {'table tr': 'border-top: 1px solid #cccccc; background-color: white; margin: 0; padding: 0;',
                 'table tr:nth-child(2n)': 'background-color: #f8f8f8;',
                 'table tr th': 'font-weight: bold; border: 1px solid #cccccc; text-align: left; margin: 0; padding: 6px 13px;',
                 'table tr td': ' border: 1px solid #cccccc; text-align: left; margin: 0; padding: 6px 13px;',
                 'table tr th :first-child, table tr td :first-child': 'margin-top: 0;',
                 'table tr th :last-child, table tr td :last-child': 'margin-bottom: 0;'}
__default_css__ = ['*, *:after, *:before {\n  -webkit-box-sizing: border-box;\n  -moz-box-sizing: border-box;\n  box-sizing: border-box;\n  margin: 0;\n  padding: 0;\n}']
__default_css__.append(''.join(['\n' + sel + ' {' + __p_css__[sel] + '\n}' for sel in __p_css__]))
__default_css__.append(''.join(['\n' + sel + ' {' + __a_css__[sel] + '\n}' for sel in __a_css__]))
__default_css__.append(''.join(['\n' + sel + ' {' + __ul_css__[sel] + '\n}' for sel in __ul_css__]))
__default_css__.append(''.join(['\n' + sel + ' {' + __ol_css__[sel] + '\n}' for sel in __ol_css__]))
__default_css__.append(''.join(['\n' + sel + ' {' + __pre_css__[sel] + '\n}' for sel in __pre_css__]))
__default_css__.append(''.join(['\n' + sel + ' {' + __columns_css__[sel] + '\n}' for sel in __columns_css__]))
__default_css__.append(''.join(['\n' + sel + ' {' + __input_btn_css__[sel] + '\n}' for sel in __input_btn_css__]))
__default_css__.append(''.join(['\n' + sel + ' {' + __countDown_css__[sel] + '\n}' for sel in __countDown_css__]))
__default_css__.append(''.join(['\n' + sel + ' {' + __timer_css__[sel] + '\n}' for sel in __timer_css__]))
__default_css__.append(''.join(['\n' + sel + ' {' + __impress_css__[sel] + '\n}' for sel in __impress_css__]))
__default_css__.append(''.join(['\n' + sel + ' {' + __table_css__[sel] + '\n}' for sel in __table_css__]))
__default_css__ = ''.join(__default_css__)


# class definition
class Theme(object):
  """Theme is an object that handles the presentation theme, its attributes and methods."""
  def __init__(self, source=None, defaults=False, set_all_custom=False, reset=False):
    """
    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    defaults : bool, optional
      flag for activatin the creation of a presentation istance
      having one of each element available with the default
      settings
    set_all_custom : bool, optional
      set all option as customized from users (useful for plain slides theme)
    reset : bool, optional
      reset theme components

    Attributes
    ----------
    canvas : Canvas object
      convas over which all elements are rendered
    headings : list
      list of Heading objects for handling style of html headings (h1,h2,...h6)
    titlepage: none
    slide : Slide object
      base theme of slides
    selectors : list
      list of Selector objects for handling user defined custom selectors (e.g. <code> tags)
    toc : TOC object
      Table of Contents theme

    >>> source =  '---theme_slide_header_1 height = 10% ---endtheme_slide_header_1'
    >>> source += '---theme_slide_footer_1 height = 10% ---endtheme_slide_footer_1'
    >>> source += '---theme_slide_sidebar_1 width = 10% ---endtheme_slide_sidebar_1'
    >>> theme = Theme(source=source)
    >>> theme.slide.headers['slide-header_1'].data.data['height'][0]
    '10%'
    >>> theme = Theme(defaults=True)
    >>> theme.slide.has_header()
    (True, 1)
    >>> theme = Theme(defaults=True,set_all_custom=True)
    >>> theme.slide.headers['slide-header_1'].data.data['height'][1]
    True
    """
    if reset:
      self.__reset()
    self.canvas = Canvas()
    self.headings = []
    for hds in range(6):
      self.headings.append(Heading(number=hds + 1))
    self.slide = Slide(defaults=defaults)
    self.selectors = []
    self.toc = TOC()
    if source:
      self.get(source=__source_editor__.purge_overtheme(source))
    elif defaults:
      self.selectors.append(Selector(name='def-sel'))
    if set_all_custom:
      self.canvas.set_all_custom()
      for hds in self.headings:
        hds.set_all_custom()
      self.slide.set_all_custom()
      for sel in self.selectors:
        sel.set_all_custom()
    return

  def __str__(self):
    string = 'Theme settings\n'
    string += '  Canvas\n'
    string += str(self.canvas)
    for hds, heading in enumerate(self.headings):
      string += '\n  h' + str(hds + 1) + '\n'
      string += str(heading)
    string += str(self.slide)
    for selector in self.selectors:
      string += '\n  selector ' + selector.name + '\n'
      string += str(selector)
    string += '\n  TOC\n'
    string += str(self.toc)
    return string

  def __get_selectors(self, source):
    """Method for getting the definition of user-defined custom selectors.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    number = Selector.count(source)
    if number > 0:
      sel_regex = re.compile(r'[-]{3}theme_selector_(?P<name>[a-zA-Z][a-zA-Z0-9_\-]*)')
      names = []
      for match in re.finditer(sel_regex, source):
        names.append(match.group('name'))
      for name in names:
        self.selectors.append(Selector(name=name, source=source))
    return

  @staticmethod
  def __reset():
    """Method resetting theme to initial values."""
    Box.reset()
    Figure.reset()
    Table.reset()
    Note.reset()
    return

  def check_specials(self):
    """Method for checking specials data entries.
    The main theme has not special entries, not being a subclass of ThemeElement.
    However the check_specials method of other contained theme elements is called.
    """
    self.canvas.check_specials()
    for hds in self.headings:
      hds.check_specials()
    self.slide.check_specials()
    if len(self.selectors) > 0:
      for selector in self.selectors:
        selector.check_specials()
    return

  def get(self, source):
    """Method for getting data values from source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    self.canvas.get(source=source)
    for hds in self.headings:
      hds.get(source=source)
    self.slide.get(source=source)
    self.__get_selectors(source=source)
    self.toc.get(source=source)
    self.check_specials()
    Figure.get_theme(source=source)
    Note.get_theme(source=source)
    Table.get_theme(source=source)
    return

  def set_from(self, other):
    """Method for setting theme using data of other theme.

    Parameters
    ----------
    other : Theme object

    >>> source =  '---theme_slide_header_1 height = 10% ---endtheme_slide_header_1'
    >>> source += '---theme_slide_footer_1 height = 10% ---endtheme_slide_footer_1'
    >>> source += '---theme_slide_sidebar_1 width = 10% ---endtheme_slide_sidebar_1'
    >>> thm1 = Theme(source=source)
    >>> thm1.slide.headers['slide-header_1'].data.data['background'] = ['white',False]
    >>> source =  '---theme_slide_header_1 background = red ---endtheme_slide_header_1'
    >>> source += '---theme_slide_header_2 background = red ---endtheme_slide_header_2'
    >>> source += '---theme_slide_footer_1 background = green ---endtheme_slide_footer_1'
    >>> source += '---theme_slide_footer_2 background = green ---endtheme_slide_footer_2'
    >>> source += '---theme_slide_sidebar_1 background = blue ---endtheme_slide_sidebar_1'
    >>> source += '---theme_slide_sidebar_2 background = blue ---endtheme_slide_sidebar_2'
    >>> thm2 = Theme(source=source)
    >>> thm1.set_from(thm2)
    >>> thm1.slide.headers['slide-header_1'].data.data['background'][0]
    'red'
    """
    self.canvas.set_from(other=other.canvas)
    for hds, head in enumerate(self.headings):
      head.set_from(other=other.headings[hds])
    self.slide.set_from(other=other.slide)
    self.toc.set_from(other=other.toc)
    self.check_specials()
    return

  # def update(self,source):
  #  """Method for updating data from source without creating new data.

  #  Parameters
  #  ----------
  #  source : str
  #    string (as single stream) containing the source
  #  """
  #  self.canvas.get(source=source)
  #  for hds in self.headings:
  #    hds.get(source=source)
  #  self.slide.update(source=source)
  #  if len(self.selectors)>0:
  #    for slr in self.selectors:
  #      slr.get(source=source)
  #  self.toc.get(source=source)
  #  self.check_specials()
  #  return

  def get_custom(self, chk_specials=False):
    """Method returning only the data that have been set by users (customized) overriding default values.

    Parameters
    ----------
    chk_specials : bool, optional
      if activated handle special entries differently from standard ones

    Returns
    -------
    dict
      dictionary of customized data

    >>> thm1 = Theme(defaults=True)
    >>> thm1.slide.headers['slide-header_1'].data.data['background'] = ['white',True]
    >>> thm1.get_custom()['slide-header_1'].data['background'][0]
    'white'
    """
    custom = self.slide.get_custom(chk_specials=chk_specials)
    custom['canvas'] = self.canvas.data.get_custom(chk_specials=chk_specials)
    for hds in self.headings:
      custom['h' + str(hds.number)] = hds.data.get_custom(chk_specials=chk_specials)
    if len(self.selectors) > 0:
      for selector in self.selectors:
        custom['slide-selector_' + selector.name] = selector.data.get_custom(chk_specials=chk_specials)
    custom['toc'] = self.toc.data.get_custom(chk_specials=chk_specials)
    return custom

  def get_options(self):
    """Method for getting the available data options.

    Returns
    -------
    str
      string with option_names = values pairs (without True/False custom tag)

    >>> thm1 = Theme(defaults=True)
    >>> thm1.get_options().split('\\n')[4]
    'active = True'
    """
    string = []
    string.append(self.canvas.get_options())
    for hds in self.headings:
      string.append(hds.get_options())
    string.append(self.slide.get_options())
    for sls in self.selectors:
      string.append(sls.get_options())
    string.append(self.toc.get_options())
    return ''.join(string)

  def get_css(self, only_custom=False, as_list=False):
    """Method for creating the css theme. The returned string contains the css theme.

    Parameters
    ----------
    only_custom : bool, optional
      consider only (user) customized data
    as_list : bool, optional
      return a list instead of a string

    Returns
    -------
    str
      a string containing the css code of the theme if as_list = False
    list
      a list of one string containing the css code of the theme if as_list = True

    >>> thm1 = Theme(defaults=True)
    >>> thm1.get_css(as_list=True)[0].split('\\n')[4]
    '  margin: 0;'
    """
    css = [__default_css__]
    css.append(self.canvas.get_css(only_custom=only_custom))
    for hds in self.headings:
      css.append(hds.get_css(only_custom=only_custom))
    css.append(self.slide.get_css(only_custom=only_custom))
    for sls in self.selectors:
      css.append(sls.get_css(only_custom=only_custom))
    css.append(self.toc.get_css(only_custom=only_custom))
    if as_list:
      return css
    else:
      return ''.join(css)

  def strip(self, source):
    """Method for striping theme raw data from source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      source without the theme data
    """
    strip_source = self.canvas.strip(source)
    if len(self.headings) > 0:
      for hds in self.headings:
        strip_source = hds.strip(strip_source)
    strip_source = self.slide.strip(strip_source)
    if len(self.selectors) > 0:
      for sls in self.selectors:
        strip_source = sls.strip(strip_source)
    strip_source = self.toc.strip(strip_source)
    # strip_source = box_strip_themes(strip_source)
    strip_source = Figure.strip_theme(strip_source)
    strip_source = Note.strip_theme(strip_source)
    strip_source = Table.strip_theme(strip_source)
    return strip_source.strip()
