#!/usr/bin/env python
"""
sidebar.py, module definition of Sidebar class.
This defines the theme of the slide sidebar element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
# MaTiSSe.py modules
from ..theme_element import ThemeElement
# class definition
class Sidebar(ThemeElement):
  """
  Object for handling the presentation theme slide sidebars, their attributes and methods.
  """
  def __init__(self,number,source=None):
    """
    Parameters
    ----------
    number : int
      number of header in the global numeration
    source : str, optional
      string (as single stream) containing the source

    Attributes
    ----------
    number : int
      number of header in the global numeration
    position : {'R','L'}
      sidebar position: rigth of left respect with the slide content element
    """
    self.number = number
    self.position = None
    super(Sidebar,self).__init__(data_tag=r'theme_slide_sidebar_'+str(self.number),special_keys=['position'],class_name='slide-sidebar_'+str(self.number))
    self.data.data['display'    ] = ['block',                       False]
    self.data.data['width'      ] = ['0%',                          False]
    self.data.data['height'     ] = ['100%',                        False]
    self.data.data['font-size'  ] = ['100%',                        False]
    self.data.data['font-family'] = ['Open Sans, Arial, sans-serif',False]
    self.data.data['position'   ] = [self.position,                 False]
    self.data.data['overflow'   ] = ['hidden',                      False]
    if source:
      self.get(source)
      self.check_specials()
    return

  def check_specials(self):
    """Method for checking specials data entries.

    This theme element has the following special entries:
    1. position

    >>> source = '---theme_slide_sidebar_1 width = 15% ---endtheme_slide_sidebar_1'
    >>> sidb1 = Sidebar(number=1,source=source)
    >>> sidb1.check_specials()
    >>> sidb1.data.data['position'][0]
    'R'
    """
    super(Sidebar,self).check_specials()
    for key,val in self.data.data.items():
      if val[1]:
        if key == 'position':
          self.position = val[0]
          self.data.data[key] = [self.position,True]
    if not self.position:
      # user does not set the position, default is right
      self.position = 'R'
      self.data.data['position'] = [self.position,False]
    return

  def set_from(self,other):
    """Method for setting theme using data of other (theme element).

    Parameters
    ----------
    other : Sidebar object

    >>> source = '---theme_slide_sidebar_1 background = red ---endtheme_slide_sidebar_1'
    >>> sidb1 = Sidebar(number=1,source=source)
    >>> source = '---theme_slide_sidebar_2 width = 15% \\n position = L ---endtheme_slide_sidebar_2'
    >>> sidb2 = Sidebar(number=2,source=source)
    >>> sidb1.set_from(sidb2)
    >>> sidb1.data.data['width'][0]
    '15%'
    >>> sidb1.data.data['position'][0]
    'L'
    """
    overposition = None
    if self.data.data['position'][1]:
      overposition = self.data.data['position']
    super(Sidebar,self).set_from(other=other)
    if overposition:
      self.data.data['position'] = overposition
    self.check_specials()
    return

  def adjust_dims(self,headers,footers):
    """Method for adjusting sidebar dimensions accordingly to the settings of other elements of the slide theme.

    Parameters
    ----------
    headers : dict
      dictionary with values of Header objects, being the list of headers defined into the slide
    footers : dict
      dictionary with values of Footer objects, being the list of footers defined into the slide

    >>> from .header import Header
    >>> source = '---theme_slide_header_1 height = 10% ---endtheme_slide_header_1'
    >>> myheader = Header(number=1,source=source)
    >>> source = '---theme_slide_sidebar_1 width = 10% ---endtheme_slide_sidebar_1'
    >>> mysidebar = Sidebar(number=1,source=source)
    >>> mysidebar.adjust_dims(headers={'1':myheader},footers={})
    >>> mysidebar.data.data['height'][0]
    '90%'
    """
    s_h = 100 # slide sidebar height (in percent %); should be always 100% initially
    if len(headers)>0:
      for header in headers.values():
        if header.active:
          s_h -= int(header.data.data['height'][0].strip('%'))
    if len(footers)>0:
      for footer in footers.values():
        if footer.active:
          s_h -= int(footer.data.data['height'][0].strip('%'))
    self.data.data['height'] = [str(s_h)+'%',True]
    return

  def get_options(self):
    """Method for getting the available data options.

    >>> source = '---theme_slide_sidebar_1 width = 10% ---endtheme_slide_sidebar_1'
    >>> mysidebar = Sidebar(number=1,source=source)
    >>> mysidebar.get_options()
    '\\n\\nSlide Sidebar\\nmetadata = []\\nactive = True\\ndisplay = block\\nwidth = 10%\\nheight = 100%\\nfont-size = 100%\\nfont-family = Open Sans, Arial, sans-serif\\nposition = R\\noverflow = hidden'
    """
    string = ['\n\nSlide Sidebar']
    string.append(self.data.get_options())
    return ''.join(string)

  def get_css(self,only_custom=False,as_list=False):
    """Method for getting css from data.

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

    >>> source = '---theme_slide_sidebar_1 width = 10% ---endtheme_slide_sidebar_1'
    >>> mysidebar = Sidebar(number=1,source=source)
    >>> mysidebar.get_css(only_custom=True)
    '\\n .slide-sidebar_1 {\\n  float: left;\\n  width: 10%;\\n}\\n'
    """
    css = "\n .slide-sidebar_"+str(self.number)+" {\n  float: left;"
    css += self.data.get_css(only_custom=only_custom)
    css += "\n}\n"
    if as_list:
      return [css]
    else:
      return css
