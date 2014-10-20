#!/usr/bin/env python
"""
content.py, module definition of Content class.
This defines the theme of the slide content element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
# MaTiSSe.py modules
from ..theme_element import ThemeElement
# class definition
class Content(ThemeElement):
  """
  Object for handling the presentation theme slide content, its attributes and methods.
  """
  def __init__(self,source=None):
    """
    Parameters
    ----------
    source : str, optional
      string (as single stream) containing the source
    """
    super(Content,self).__init__(data_tag=r'theme_slide_content',class_name='slide-content')
    self.data.data['display'    ] = ['block',                       False]
    self.data.data['width'      ] = ['100%',                        False]
    self.data.data['height'     ] = ['100%',                        False]
    self.data.data['padding'    ] = ['0',                           False]
    self.data.data['font-size'  ] = ['100%',                        False]
    self.data.data['font-family'] = ['Open Sans, Arial, sans-serif',False]
    self.data.data['overflow'   ] = ['hidden',                      False]
    if source:
      self.get(source)
      self.check_specials()
    return

  def adjust_dims(self,headers,footers,sidebars):
    """Method for adjusting content dimensions accordingly to the settings of other elements of the slide theme.

    Parameters
    ----------
    headers : dict
      dictionary with values of Header objects, being the list of headers defined into the slide
    footers : dict
      dictionary with values of Footer objects, being the list of footers defined into the slide
    sidebars : dict
      dictionary with values of Sidebar objects, being the list of sidebars defined into the slide

    >>> from .header import Header
    >>> source = '---theme_slide_header_1 height = 10% ---endtheme_slide_header_1'
    >>> myheader = Header(number=1,source=source)
    >>> source = '---theme_slide_content background = red ---endtheme_slide_content'
    >>> mycontent = Content(source=source)
    >>> mycontent.adjust_dims(headers={'1':myheader},footers={},sidebars={})
    >>> mycontent.data.data['height'][0]
    '90%'
    """
    s_w = 100 # slide content width (in percent %); should be always 100% initially
    s_h = 100 # slide content height (in percent %); should be always 100% initially
    if len(headers)>0:
      for header in headers.values():
        if header.active:
          s_h -= int(header.data.data['height'][0].strip('%'))
    if len(footers)>0:
      for footer in footers.values():
        if footer.active:
          s_h -= int(footer.data.data['height'][0].strip('%'))
    if len(sidebars)>0:
      for sidebar in sidebars.values():
        if sidebar.active:
          s_w -= int(sidebar.data.data['width'][0].strip('%'))
    self.data.data['width']  = [str(s_w)+'%',True]
    self.data.data['height'] = [str(s_h)+'%',True]
    return

  def get_options(self):
    """Method for getting the available data options.

    >>> source = '---theme_slide_content background = red ---endtheme_slide_content'
    >>> mycontent = Content(source=source)
    >>> mycontent.get_options()
    '\\n\\nSlide Content\\nmetadata = []\\nactive = True\\ndisplay = block\\nwidth = 100%\\nheight = 100%\\npadding = 0\\nfont-size = 100%\\nfont-family = Open Sans, Arial, sans-serif\\noverflow = hidden\\nbackground = red'
    """
    string = ['\n\nSlide Content']
    string.append(self.data.get_options())
    return ''.join(string)

  def get_css(self,only_custom=False,as_list=False):
    """Method for getting css from data.

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

    >>> source = '---theme_slide_content background = red ---endtheme_slide_content'
    >>> mycontent = Content(source=source)
    >>> mycontent.get_css(only_custom=True)
    '\\n .slide-content {\\n  float: left;\\n  background: red;\\n}\\n'
    """
    css = "\n .slide-content {\n  float: left;"
    css += self.data.get_css(only_custom=only_custom)
    css += "\n}\n"
    if as_list:
      return [css]
    else:
      return css
