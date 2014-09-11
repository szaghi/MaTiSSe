#!/usr/bin/env python
"""
slide.py, module definition of Slide class.
This defines the theme of the slide element.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
# MaTiSSe.py modules
from ..theme_element import ThemeElement
from ...utils.utils import  purge_source,__regex_over_slide_theme__
from .header import Header
from .footer import Footer
from .sidebar import Sidebar
from .content import Content
# class definition
class SlidePosition(object):
  """
  Object for handling slide position into the canvas.
  """
  def __init__(self):
    self.position = [0,0,0] # x,y,z
    self.rotation = [0,0,0] # around x,y,z
    self.scale = 1
    return
  def __str__(self):
    string = ['\nPosition (x,y,z) = '+','.join([str(p) for p in self.position])]
    string.append('\nRotation (x,y,z) = '+','.join([str(r) for r in self.rotation]))
    string.append('\nScale factor = '+str(self.scale))
    return ''.join(string)
  def set_position(self,theme,overtheme=None):
    """
    Method for getting positioning data inquiring the (base) theme and the eventually
    present overriding one.
    """
    actual_theme = theme
    if overtheme:
      actual_theme = overtheme

    scale = self.get_scale(theme=actual_theme)

    self.rotation = self.get_rotation(theme=actual_theme)

    self.position = self.get_position(theme=actual_theme,scale=scale)

    self.scale = scale
    return
  @staticmethod
  def get_scale(theme):
    """
    Method for computing the current slide scale factor.
    """
    return int(theme.data.data['data-scale'][0])
  @staticmethod
  def get_rotation(theme):
    """
    Method for computing the current slide scale factor.
    """
    rot = int(theme.data.data['data-rotate'][0])
    rot_x = int(theme.data.data['data-rotate-x'][0])
    rot_y = int(theme.data.data['data-rotate-y'][0])
    rot_z = int(theme.data.data['data-rotate-z'][0])
    if rot_z != 0:
      rot = max(rot,rot_z)
    return [rot_x,rot_y,rot]
  def get_position(self,theme,scale):
    """
    Method for computing the current slide position.
    """
    pos_x = int(theme.data.data['data-x'][0])
    pos_y = int(theme.data.data['data-y'][0])
    pos_z = int(theme.data.data['data-z'][0])
    slide_width = int(theme.data.data['width'][0].strip('px'))
    slide_height = int(theme.data.data['height'][0].strip('px'))
    slide_transition = theme.data.data['slide-transition'][0]
    if slide_transition == 'horizontal':
      pos_x = self.position[0] + slide_width*(max(self.scale,scale)+0.01)
      pos_y = self.position[1]
    elif slide_transition == 'vertical':
      pos_x = self.position[0]
      pos_y = self.position[1] + slide_height*(max(self.scale,scale)+0.01)
    return [pos_x,pos_y,pos_z]
class Slide(ThemeElement):
  """
  Object for handling the presentation theme slide, its attributes and methods.
  """
  def __init__(self,source=None):
    """
    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Attributes
    ----------
    content : Content object
      the main content element of the slide
    headers : list
      list of Header objects for handling the slide headers
    footers : list
      list of Footer objects for handling the slide footers
    sidebars : list
      list of Sidebar objects for handling the slide sidebars
    """
    self.content  = Content()
    self.headers  = {}
    self.footers  = {}
    self.sidebars = {}
    super(Slide,self).__init__(data_tag=r'theme_slide_global',
                               special_keys=['slide-transition',
                                             'data-scale',
                                             'data-rotate','data-rotate-x','data-rotate-y','data-rotate-z',
                                             'data-x','data-y','data-z'])
    self.data.data['width'           ] = ['900px',     False]
    self.data.data['height'          ] = ['700px',     False]
    self.data.data['slide-transition'] = ['horizontal',False]
    self.data.data['data-scale']       = ['1',         False]
    self.data.data['data-rotate']      = ['0',         False]
    self.data.data['data-rotate-x']    = ['0',         False]
    self.data.data['data-rotate-y']    = ['0',         False]
    self.data.data['data-rotate-z']    = ['0',         False]
    self.data.data['data-x']           = ['0',         False]
    self.data.data['data-y']           = ['0',         False]
    self.data.data['data-z']           = ['0',         False]
    if source:
      self.get(source)
    return

  def __str__(self):
    string = '\n  Global slide\n'
    string += super(Slide, self).__str__()
    if self.has_header():
      for header in self.headers.values():
        string += '\n  Header n.'+str(header.number)+'\n'+str(header)
    if self.has_footer():
      for footer in self.footers.values():
        string += '\n  Footer n.'+str(footer.number)+'\n'+str(footer)
    if self.has_sidebar():
      for sidebar in self.sidebars.values():
        string += '\n  Sidebar n.'+str(sidebar.number)+'\n'+str(sidebar)
    string += '\n  Content\n'+str(self.content)
    return string

  def has_header(self,source=None):
    """Method for inquiring the presence of headers.

    Parameters
    ----------
    source : str
    """
    if source:
      number = purge_source(regex=__regex_over_slide_theme__,source=source).count('theme_slide_header')/2
    else:
      number = len(self.headers)
    return number>0,number

  def has_footer(self,source=None):
    """Method for inquiring the presence of footers.

    Parameters
    ----------
    source : str
    """
    if source:
      number = purge_source(regex=__regex_over_slide_theme__,source=source).count('theme_slide_footer')/2
    else:
      number = len(self.footers)
    return number>0,number

  def has_sidebar(self,source=None):
    """Method for inquiring the presence of sidebars.

    Parameters
    ----------
    source : str
    """
    if source:
      number = purge_source(regex=__regex_over_slide_theme__,source=source).count('theme_slide_sidebar')/2
    else:
      number = len(self.footers)
    return number>0,number

  def get(self,source):
    """Method for getting data values from source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    super(Slide, self).get(source)
    self.check_specials()
    self.content.get(source)
    has,number = self.has_header(source)
    if has:
      for hdr in range(number):
        self.headers['slide-header_'+str(hdr+1)] = Header(number=hdr+1,source=source)
    has,number = self.has_footer(source)
    if has:
      for ftr in range(number):
        self.footers['slide-footer_'+str(ftr+1)] = Footer(number=ftr+1,source=source)
    has,number = self.has_sidebar(source)
    if has:
      for sbr in range(number):
        self.sidebars['slide-sidebar_'+str(sbr+1)] = Sidebar(number=sbr+1,source=source)
    self.adjust_dims()
    return

  def set_from(self,other):
    """Method for setting theme slide using data of other (theme slide element).

    Parameters
    ----------
    other : ThemeSlide object
    """
    self.content.set_from(other=other.content)

    if other.has_header():
      for header in other.headers:
        if header in self.headers:
          self.headers[header].set_from(other=other.headers[header])
        else:
          self.headers[header] = Header(number=other.headers[header].number)
          self.headers[header].set_from(other=other.headers[header])

    if other.has_footer():
      for footer in other.footers:
        if footer in self.footers:
          self.footers[footer].set_from(other=other.footers[footer])
        else:
          self.footers[footer] = Footer(number=other.footers[footer].number)
          self.footers[footer].set_from(other=other.footers[footer])

    if other.has_sidebar():
      for sidebar in other.sidebars:
        if sidebar in self.sidebars:
          self.sidebars[sidebar].set_from(other=other.sidebars[sidebar])
        else:
          self.sidebars[sidebar] = Sidebar(number=other.sidebars[sidebar].number)
          self.sidebars[sidebar].set_from(other=other.sidebars[sidebar])

    self.check_specials()
    return

  def update(self,source):
    """Method for updating data from source without creating new data.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    super(Slide,self).get(source)
    self.content.get(source)
    if self.has_header():
      for hdr in self.headers.values():
        hdr.get(source)
    if self.has_footer():
      for ftr in self.footers.values():
        ftr.get(source)
    if self.has_sidebar():
      for sbr in self.sidebars.values():
        sbr.get(source)
    self.adjust_dims()
    return

  def check_specials(self):
    """Method for checking specials data entries.

    This theme element has the following special entries:
    1. slide-transition
    2. data-scale
    3. data-rotate
    4. data-rotate-x
    5. data-rotate-y
    6. data-rotate-z
    7. data-x
    8. data-y']
    9. data-z
    The check_specials method of other contained elements is called.
    """
    for key,val in self.data.data.items():
      if val[1]:
        if (key == 'slide-transition' or
            key == 'data-scale' or
            key =='data-rotate' or key =='data-rotate-x' or key =='data-rotate-y' or key =='data-rotate-z' or
            key =='data-x' or key =='data-y' or key =='data-z'):
          self.data.data[key] = [val[0],True]
    self.content.check_specials()
    if self.has_header():
      for hdr in self.headers.values():
        hdr.check_specials()
    if self.has_footer():
      for ftr in self.footers.values():
        ftr.check_specials()
    if self.has_sidebar():
      for sbr in self.sidebars.values():
        sbr.check_specials()
    return

  def adjust_dims(self):
    """Method for adjusting dimensions of slide elements accordingly to the settings of other elements of the slide theme.
    """
    self.content.adjust_dims(headers=self.headers,footers=self.footers,sidebars=self.sidebars)
    if self.has_sidebar():
      for sidebar in self.sidebars.values():
        if sidebar.active:
          sidebar.adjust_dims(headers=self.headers,footers=self.footers)
    return

  def get_custom(self,chk_specials=False):
    """Method returning only the data that have been set by users (customized) overriding default values.

    Parameters
    ----------
    chk_specials : bool, optional
      if activated handle special entries differently from standard ones
    """
    custom = {}
    custom['slide-content'] = self.content.data.get_custom(chk_specials=chk_specials)
    if self.has_header():
      for header in self.headers.values():
        if header.active:
          custom['slide-header_'+str(header.number)] = header.data.get_custom(chk_specials=chk_specials)
    if self.has_footer():
      for footer in self.footers.values():
        if footer.active:
          custom['slide-footer_'+str(footer.number)] = footer.data.get_custom(chk_specials=chk_specials)
    if self.has_sidebar():
      for sidebar in self.sidebars.values():
        if sidebar.active:
          custom['slide-sidebar_'+str(sidebar.number)] = sidebar.data.get_custom(chk_specials=chk_specials)
    return custom

  def get_css(self,only_custom=False,as_list=False):
    """Method for setting theme values. The theme skeleton is passed as string.

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
    """
    css = ["\n.slide {\n  display: block;\n  padding: 0;\n  margin: 0;"+super(Slide,self).get_css(only_custom=only_custom)+"\n}\n"]
    if self.has_header():
      for header in self.headers.values():
        css.append(header.get_css(only_custom=only_custom))
    if self.has_footer():
      for footer in self.footers.values():
        css.append(footer.get_css(only_custom=only_custom))
    if self.has_sidebar():
      for sidebar in self.sidebars.values():
        css.append(sidebar.get_css(only_custom=only_custom))
    css.append(self.content.get_css(only_custom=only_custom))
    if as_list:
      return css
    else:
      return ''.join(css)

  def strip(self,source):
    """Method for striping theme slide raw data from source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      source without the theme data
    """
    strip_source = self.data.strip(source)
    strip_source = self.content.strip(strip_source)
    if self.has_header():
      for hdr in self.headers.values():
        strip_source = hdr.strip(strip_source)
    if self.has_footer():
      for ftr in self.footers.values():
        strip_source = ftr.strip(strip_source)
    if self.has_sidebar():
      for sdr in self.sidebars.values():
        strip_source = sdr.strip(strip_source)
    return strip_source
