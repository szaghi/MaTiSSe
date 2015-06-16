#!/usr/bin/env python
"""
toc.py, module definition of TOC class.
This defines the theme of the Table of Contents.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
# MaTiSSe.py modules
from .theme_element import ThemeElement
# classes definition
class SectionEmph(ThemeElement):
  """
  Object for handling the section emphasized theme into TOC, its attributes and methods.
  """
  def __init__(self,source=None,skip=None):
    """
    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    super(SectionEmph,self).__init__(data_tag=r'theme_section_emph_toc')
    self.data.data['margin'       ] = ['1% 0',             False]
    self.data.data['clear'        ] = ['both',             False]
    self.data.data['float'        ] = ['left',             False]
    self.data.data['border'       ] = ['1px solid #4788B3',False]
    self.data.data['border-radius'] = ['5px',              False]
    if source:
      self.get(source)
    return

  def get_options(self):
    """Method for getting the available data options."""
    string = ['\n\nTOC Section Emphasized']
    string.append(self.data.get_options())
    return ''.join(string)

  def get_css(self,only_custom=False,as_list=False):
    """Method for getting css from data.
    """
    css = "\n.toc-section.emph {"
    css += self.data.get_css(only_custom=only_custom)
    css += "\n}\n"
    if as_list:
      return [css]
    else:
      return css

class SubsectionEmph(ThemeElement):
  """
  Object for handling the subsection emphasized theme into TOC, its attributes and methods.
  """
  def __init__(self,source=None):
    """
    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    super(SubsectionEmph,self).__init__(data_tag=r'theme_subsection_emph_toc')
    self.data.data['clear'        ] = ['both',             False]
    self.data.data['float'        ] = ['left',             False]
    self.data.data['margin'       ] = ['1% 0',             False]
    self.data.data['border'       ] = ['1px solid #4788B3',False]
    self.data.data['border-radius'] = ['5px',              False]
    if source:
      self.get(source)
    return

  def get_options(self):
    """Method for getting the available data options."""
    string = ['\n\nTOC Subsection Emphasized']
    string.append(self.data.get_options())
    return ''.join(string)

  def get_css(self,only_custom=False,as_list=False):
    """Method for getting css from data.
    """
    css = "\n.toc-subsection.emph {"
    css += self.data.get_css(only_custom=only_custom)
    css += "\n}\n"
    if as_list:
      return [css]
    else:
      return css

class SlideEmph(ThemeElement):
  """
  Object for handling the slide emphasized theme into TOC, its attributes and methods.
  """
  def __init__(self,source=None):
    """
    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    super(SlideEmph,self).__init__(data_tag=r'theme_slide_emph_toc')
    self.data.data['margin'       ] = ['1% 0',             False]
    self.data.data['clear'        ] = ['both',             False]
    self.data.data['float'        ] = ['left',             False]
    self.data.data['border'       ] = ['1px solid #4788B3',False]
    self.data.data['border-radius'] = ['5px',              False]
    if source:
      self.get(source)
    return

  def get_options(self):
    """Method for getting the available data options."""
    string = ['\n\nTOC Slide Emphasized']
    string.append(self.data.get_options())
    return ''.join(string)

  def get_css(self,only_custom=False,as_list=False):
    """Method for getting css from data.
    """
    css = "\n.toc-slide.emph {"
    css += self.data.get_css(only_custom=only_custom)
    css += "\n}\n"
    if as_list:
      return [css]
    else:
      return css

class TOC(ThemeElement):
  """
  Object for handling the TOC theme, its attributes and methods.
  """
  def __init__(self,source=None):
    """
    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    super(TOC,self).__init__(data_tag=r'theme_toc')
    self.data.data['display'] = ['block',False]
    self.section_emph = SectionEmph()
    self.subsection_emph = SubsectionEmph()
    self.slide_emph = SlideEmph()
    if source:
      self.get(source)
    return

  def get(self,source):
    """Method for getting data values from source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    super(TOC, self).get(source)
    self.check_specials()
    self.section_emph.get(source)
    self.subsection_emph.get(source)
    self.slide_emph.get(source)
    return

  def set_from(self,other):
    """Method for setting theme slide using data of other (theme slide element).

    Parameters
    ----------
    other : TOC object
    """
    #super(TOC, self).set_from(other=other)
    self.section_emph.set_from(other=other.section_emph)
    self.subsection_emph.set_from(other=other.subsection_emph)
    self.slide_emph.set_from(other=other.slide_emph)
    return

  def update(self,source):
    """Method for updating data from source without creating new data.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    """
    self.get(source)
    return

  def check_specials(self):
    """Method for checking specials data entries."""
    super(TOC, self).check_specials()
    self.section_emph.check_specials()
    self.subsection_emph.check_specials()
    self.slide_emph.check_specials()
    return

  def get_custom(self,chk_specials=False):
    """Method returning only the data that have been set by users (customized) overriding default values.

    Parameters
    ----------
    chk_specials : bool, optional
      if activated handle special entries differently from standard ones

    Returns
    -------
    dict
      dictionary of customized data
    """
    custom = {}
    custom['toc'] = self.data.get_custom(chk_specials=chk_specials)
    custom['toc-section_emph'] = self.section_emph.data.get_custom(chk_specials=chk_specials)
    custom['toc-subsection_emph'] = self.subsection_emph.data.get_custom(chk_specials=chk_specials)
    custom['toc-slide_emph'] = self.slide_emph.data.get_custom(chk_specials=chk_specials)
    return custom

  def get_options(self):
    """Method for getting the available data options."""
    string = ['\n\nTOC']
    string.append(self.data.get_options())
    string.append(self.section_emph.get_options())
    string.append(self.subsection_emph.get_options())
    string.append(self.slide_emph.get_options())
    return ''.join(string)

  def get_css(self,only_custom=False,as_list=False):
    """Method for getting css from data.
    """
    css = ["\n.toc {" + self.data.get_css(only_custom=only_custom) + "\n}\n"]
    css.append(".toc-section{\n  display: block;\n  clear: both;\n  float: left;\n  white-space: pre-wrap;\n}\n")
    css.append(".toc-subsection{\n  display: block;\n  clear: both;\n  float: left;\n  white-space: pre-wrap;\n}\n")
    css.append(".toc-slide{\n  display: block;\n  clear: both;\n  float: left;\n  white-space: pre-wrap;\n}\n")
    css.append(self.section_emph.get_css(only_custom=only_custom))
    css.append(self.subsection_emph.get_css(only_custom=only_custom))
    css.append(self.slide_emph.get_css(only_custom=only_custom))
    if as_list:
      return css
    else:
      return ''.join(css)

  def strip(self,source):
    """Method for striping toc theme raw data from source.

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
    strip_source = self.section_emph.strip(strip_source)
    strip_source = self.subsection_emph.strip(strip_source)
    strip_source = self.slide_emph.strip(strip_source)
    return strip_source
