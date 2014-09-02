#!/usr/bin/env python
"""
theme.py, module definition of Theme class.
This defines the theme of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import os
import copy
# MaTiSSe.py modules
from .theme_slide_header import ThemeSlideHeader
from .theme_slide_footer import ThemeSlideFooter
from .theme_slide_sidebar import ThemeSlideSidebar
from .theme_slide import ThemeSlide
# class definition
class Theme(object):
  """
  Theme is an object that handles the presentation theme, its attributes and methods.
  """
  def __init__(self,
               source = None,
               slide  = None):
    if slide:
      self.slide = slide
    else:
      self.slide = ThemeSlide()
    if source:
      # parsing source for eventual global slide settings
      self.slide.get_raw_data(source)
      self.slide.get_values()
      # parsing source for eventual headers definition and settings
      self.slide.count_headers(source)
      if self.slide.headers_number>0:
        for hdr in range(self.slide.headers_number):
          self.slide.headers.append(ThemeSlideHeader(number=hdr+1,active=True))
          self.slide.headers[hdr].get_raw_data(source)
          self.slide.headers[hdr].get_values()
      # parsing source for eventual footers definition and settings
      self.slide.count_footers(source)
      if self.slide.footers_number>0:
        for ftr in range(self.slide.footers_number):
          self.slide.footers.append(ThemeSlideFooter(number=ftr+1,active=True))
          self.slide.footers[ftr].get_raw_data(source)
          self.slide.footers[ftr].get_values()
      # parsing source for eventual sidebars definition and settings
      self.slide.count_sidebars(source)
      if self.slide.sidebars_number>0:
        for sbr in range(self.slide.sidebars_number):
          self.slide.sidebars.append(ThemeSlideSidebar(number=sbr+1,active=True))
          self.slide.sidebars[sbr].get_raw_data(source)
          self.slide.sidebars[sbr].get_values()
          self.slide.sidebars[sbr].update_position()
      # parsing source for eventual slide content settings
      self.slide.content.get_raw_data(source)
      self.slide.content.get_values()
    return
  def __str__(self):
    string = 'Theme settings\n'
    string += str(self.slide)
    return string
  def __deepcopy__(self):
    return Theme(source = None, slide = copy.deepcopy(self.slide))
  def has_header(self):
    """
    Method for inquiring the presence of headers into the slide theme.
    """
    return self.slide.has_header()
  def has_footer(self):
    """
    Method for inquiring the presence of footers into the slide theme.
    """
    return self.slide.has_footer()
  def has_sidebar(self):
    """
    Method for inquiring the presence of sidebars into the slide theme.
    """
    return self.slide.has_sidebar()
  def get_css(self):
    """
    Method for creating a theme css accordingly to the user options.
    It is made parsing the "MaTiSSe/css/themes/default-skeleton.css" file.
    The returned string contains the css theme.
    """
    # dimensioning slide content size accordingly to other theme's elements
    self.slide.content.adjust_dims(headers=self.slide.headers,footers=self.slide.footers,sidebars=self.slide.sidebars)
    # dimensioning slide sidebars size accordingly to other theme's elements
    if self.has_sidebar():
      for sidebar in self.slide.sidebars:
        sidebar.adjust_dims(headers=self.slide.headers,footers=self.slide.footers)
    # loading skeleton
    css = os.path.join(os.path.dirname(__file__), 'css/themes/default-skeleton.css')
    with open(css,'r') as sk_css:
      css_template = sk_css.read()
    return css_template+self.slide.get_css()
  def strip(self,source):
    """
    Method for striping theme raw data from source.
    """
    strip_source = self.slide.raw_data.strip(source)
    strip_source = self.slide.content.raw_data.strip(strip_source)
    return strip_source
