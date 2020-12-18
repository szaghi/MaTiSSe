#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
theme.py, module definition of Theme class.
"""
from __future__ import absolute_import
from __future__ import print_function
from copy import deepcopy
from collections import OrderedDict
from yaml import load_all, YAMLError, FullLoader
from .box import Box
from .note import Note
from .figure import Figure
from .table import Table
from .video import Video


class Theme(object):
  """
  Presentation theme object.
  """

  @classmethod
  def reset(cls):
    """Reset to default state."""
    Box.reset()
    Note.reset()
    Figure.reset()
    Table.reset()
    Video.reset()

  def __init__(self, source=None, name='theme', div_id=''):
    """
    Parameters
    ----------
    source: str
    name: str
    div_id: str
    default: bool
      add defaults css

    Attributes
    ----------
    canvas = dict
      dictionary of canvas theme
    toc = dict
      dictionary of table of contents theme
    slide = dict
      dictionary of slide theme
    css = str
      css theme as single stream
    """
    self.copy_from_theme = None
    self.canvas = []
    self.ordered_list = []
    self.unordered_list = []
    self.ordered_list_items = []
    self.unordered_list_items = []
    self.toc = []
    self.toc_chapter_emph = []
    self.toc_section_emph = []
    self.toc_subsection_emph = []
    self.toc_slide_emph = []
    self.slide = []
    self.slide_content = []
    self.slide_header = {}
    self.slide_footer = {}
    self.slide_sidebar = {}
    self.box = []
    self.box_caption = []
    self.box_content = []
    self.note = []
    self.note_caption = []
    self.note_content = []
    self.table = []
    self.table_caption = []
    self.table_content = []
    self.figure = []
    self.figure_caption = []
    self.figure_content = []
    self.video = []
    self.video_caption = []
    self.video_content = []
    self.slide_header_metadata = {}
    self.slide_footer_metadata = {}
    self.slide_sidebar_metadata = {}
    self.css = None
    self.custom = False
    self.div_id = div_id
    if source is not None:
      self.get(source=source, name=name, div_id=div_id)
    return

  def __str__(self):
    if self.css is None:
      return ''
    return self.css

  def set_from(self, other):
    """Set self attributes deepcopying theme from other theme.

    Parameters
    ----------
    other: Theme()
    """
    self.canvas = deepcopy(other.canvas)
    self.toc = deepcopy(other.toc)
    self.toc_chapter_emph = deepcopy(other.toc_chapter_emph)
    self.toc_section_emph = deepcopy(other.toc_section_emph)
    self.toc_subsection_emph = deepcopy(other.toc_subsection_emph)
    self.toc_slide_emph = deepcopy(other.toc_slide_emph)
    self.slide = deepcopy(other.slide)
    self.slide_content = deepcopy(other.slide_content)
    self.slide_header = deepcopy(other.slide_header)
    self.slide_footer = deepcopy(other.slide_footer)
    self.slide_sidebar = deepcopy(other.slide_sidebar)
    self.box = deepcopy(other.box)
    self.box_caption = deepcopy(other.box_caption)
    self.box_content = deepcopy(other.box_content)
    self.note = deepcopy(other.note)
    self.note_caption = deepcopy(other.note_caption)
    self.note_content = deepcopy(other.note_content)
    self.table = deepcopy(other.table)
    self.table_caption = deepcopy(other.table_caption)
    self.table_content = deepcopy(other.table_content)
    self.figure = deepcopy(other.figure)
    self.figure_caption = deepcopy(other.figure_caption)
    self.figure_content = deepcopy(other.figure_content)
    self.video = deepcopy(other.video)
    self.video_caption = deepcopy(other.video_caption)
    self.video_content = deepcopy(other.video_content)
    self.slide_header_metadata = deepcopy(other.slide_header_metadata)
    self.slide_footer_metadata = deepcopy(other.slide_footer_metadata)
    self.slide_sidebar_metadata = deepcopy(other.slide_sidebar_metadata)
    self.css = deepcopy(other.css)
    self.custom = deepcopy(other.custom)

  def copy_from(self, other):
    """Copy attributes from other theme if self has not already set those attributes.

    Parameters
    ----------
    other: Theme()
    """
    def append_css(my_element, other_element):
      if len(other_element) > 0:
        for css in other_element:
          found = False
          for mycss in my_element:
            if isinstance(css, dict):
              if css.keys()[0] in mycss:
                found = True
            elif css in mycss:
              found = True
          if not found:
            if isinstance(my_element, list):
              my_element.append(css)
            else:
              my_element[css] = other_element[css]

    append_css(my_element=self.canvas, other_element=other.canvas)
    append_css(my_element=self.toc, other_element=other.toc)
    append_css(my_element=self.toc_chapter_emph, other_element=other.toc_chapter_emph)
    append_css(my_element=self.toc_section_emph, other_element=other.toc_section_emph)
    append_css(my_element=self.toc_subsection_emph, other_element=other.toc_subsection_emph)
    append_css(my_element=self.toc_slide_emph, other_element=other.toc_slide_emph)
    append_css(my_element=self.slide, other_element=other.slide)
    append_css(my_element=self.slide_content, other_element=other.slide_content)
    for header in other.slide_header:
      if header not in self.slide_header:
        self.slide_header[header] = other.slide_header[header]
      else:
        append_css(my_element=self.slide_header[header], other_element=other.slide_header[header])
    for footer in other.slide_footer:
      if footer not in self.slide_footer:
        self.slide_footer[footer] = other.slide_footer[footer]
      else:
        append_css(my_element=self.slide_footer[footer], other_element=other.slide_footer[footer])
    for sidebar in other.slide_sidebar:
      if sidebar not in self.slide_sidebar:
        self.slide_sidebar[sidebar] = other.slide_sidebar[sidebar]
      else:
        append_css(my_element=self.slide_sidebar[sidebar], other_element=other.slide_sidebar[sidebar])
    append_css(my_element=self.box, other_element=other.box)
    append_css(my_element=self.box_caption, other_element=other.box_caption)
    append_css(my_element=self.box_content, other_element=other.box_content)
    append_css(my_element=self.note, other_element=other.note)
    append_css(my_element=self.note_caption, other_element=other.note_caption)
    append_css(my_element=self.note_content, other_element=other.note_content)
    append_css(my_element=self.table, other_element=other.table)
    append_css(my_element=self.table_caption, other_element=other.table_caption)
    append_css(my_element=self.table_content, other_element=other.table_content)
    append_css(my_element=self.figure, other_element=other.figure)
    append_css(my_element=self.figure_caption, other_element=other.figure_caption)
    append_css(my_element=self.figure_content, other_element=other.figure_content)
    append_css(my_element=self.video, other_element=other.video)
    append_css(my_element=self.video_caption, other_element=other.video_caption)
    append_css(my_element=self.video_content, other_element=other.video_content)
    for header in other.slide_header_metadata:
      if header not in self.slide_header_metadata:
        self.slide_header_metadata[header] = other.slide_header_metadata[header]
      else:
        append_css(my_element=self.slide_header_metadata[header], other_element=other.slide_header_metadata[header])
    for footer in other.slide_footer_metadata:
      if footer not in self.slide_footer_metadata:
        self.slide_footer_metadata[footer] = other.slide_footer_metadata[footer]
      else:
        append_css(my_element=self.slide_footer_metadata[footer], other_element=other.slide_footer_metadata[footer])
    for sidebar in other.slide_sidebar_metadata:
      if sidebar not in self.slide_sidebar_metadata:
        self.slide_sidebar_metadata[sidebar] = other.slide_sidebar_metadata[sidebar]
      else:
        append_css(my_element=self.slide_sidebar_metadata[sidebar], other_element=other.slide_sidebar_metadata[sidebar])
    self.__check_slide()
    self.__get_css()

  @staticmethod
  def theme2css(div, div_id, klass, theme_list):
    """
    Convert theme list data to css.

    Parameters
    ----------
    div: str
      div tag type
    div_id: str
    klass: str
      css class name
    theme_list: list
      theme list data

    Returns
    -------
    css: str
    """
    if len(theme_list) > 0:
      head = ''
      if div_id != '':
        head += '#' + div_id
      if div != '':
        head += ' ' + div + ' '
      if klass != '':
        if klass == 'slide':
          head += '.' + klass + ' '
        else:
          head += ' .' + klass + ' '
      css = ['\n' + head + '{']
      for element in theme_list:
        for key in element:
          if 'metadata' not in key.lower():
            css.append('\n  ' + key + ': ' + element[key] + ';')
      css.append('\n}')
      return ''.join(css)
    return ''

  @staticmethod
  def check_css_attribute(name, value, css_list, retain=False):
    """Ensure css attribute presence into CSS theme.

    Parameters
    ----------
    name: str
      attribute name
    value: str
      attribute value
    css_list: list
    retain: bool
      retain the already present value
    """
    found = False
    for css in css_list:
      if found:
        break
      for key in css:
        if name.lower() in key.lower():
          if not retain:
            css[key] = value
          found = True
          break
    if not found:
      css_list.append({name: value})

  def __get_slide_decorators_metadata(self):
    """Get metadata of slide decorators (headers, footers, sidebars)."""
    def __get_decorators(decorator):
      decorators = getattr(self, 'slide_' + decorator)
      for decor in decorators:
        getattr(self, 'slide_' + decorator + '_metadata')[decor] = OrderedDict()
        for data in decorators[decor]:
          for key in data:
            if 'metadata' in key.lower():
              for meta in data[key]:
                for meta_key in meta:
                  css = ''
                  for elem in meta[meta_key]:
                    for elem_key in elem:
                      css += elem_key + ':' + elem[elem_key] + ';'
                  getattr(self, 'slide_' + decorator + '_metadata')[decor][meta_key] = css

    __get_decorators(decorator='header')
    __get_decorators(decorator='footer')
    __get_decorators(decorator='sidebar')

  def __get_copy_from(self, data):
    """
    Get copy-from value.

    Parameters
    ----------
    data: dict
    """
    if 'copy-from-theme' in data:
      self.copy_from_theme = data['copy-from-theme']

  def __get_canvas(self, data):
    """
    Get canvas theme.

    Parameters
    ----------
    data: dict
    """
    if 'canvas' in data:
      self.canvas = data['canvas']

  def __get_ordered_list(self, data):
    """
    Get ordered-list theme.

    Parameters
    ----------
    data: dict
    """
    if 'ordered-list' in data:
      self.ordered_list = data['ordered-list']

  def __get_unordered_list(self, data):
    """
    Get unordered-list theme.

    Parameters
    ----------
    data: dict
    """
    if 'unordered-list' in data:
      self.unordered_list = data['unordered-list']

  def __get_ordered_list_items(self, data):
    """
    Get ordered-list-items theme.

    Parameters
    ----------
    data: dict
    """
    if 'ordered-list-items' in data:
      self.ordered_list_items = data['ordered-list-items']

  def __get_unordered_list_items(self, data):
    """
    Get unordered-list-items theme.

    Parameters
    ----------
    data: dict
    """
    if 'unordered-list-items' in data:
      self.unordered_list_items = data['unordered-list-items']

  def __get_toc(self, data):
    """
    Get toc theme.

    Parameters
    ----------
    data: dict
    """
    if 'toc' in data:
      toc = data['toc']
      for toc_element in toc:
        for key in toc_element:
          if 'emph' not in key:
            self.toc.append(toc_element)
          if 'chapter-emph' in key:
            self.toc_chapter_emph = toc_element[key]
          if 'section-emph' in key and 'subsection' not in key:
            self.toc_section_emph = toc_element[key]
          if 'subsection-emph' in key:
            self.toc_subsection_emph = toc_element[key]
          if 'slide-emph' in key:
            self.toc_slide_emph = toc_element[key]

  def __check_slide_dimensions(self):
    """Ensure dimensions assignment for slide theme."""
    found_w = False
    found_h = False
    for css in self.slide:
      if found_w and found_h:
        break
      for key in css:
        if 'width' in key.lower():
          found_w = True
        if 'height' in key.lower():
          found_h = True
    if not found_w:
      self.slide.append({'width': '900px'})
    if not found_h:
      self.slide.append({'height': '700px'})

  def __check_slide_headers_dimensions(self):
    """Ensure dimensions assignment for slide headers theme."""
    for header in self.slide_header:
      # search for eventual margins
      #         top, bottom, right, left
      margin = [0, 0, 0, 0]
      for css in self.slide_header[header]:
        for key in css:
          if 'margin-top' in key.lower():
            margin[0] = int(css[key].strip('%'))
          if 'margin-bottom' in key.lower():
            margin[1] = int(css[key].strip('%'))
          if 'margin-right' in key.lower():
            margin[2] = int(css[key].strip('%'))
          if 'margin-left' in key.lower():
            margin[3] = int(css[key].strip('%'))
      # checking dimensions
      found_w = False
      found_h = False
      for css in self.slide_header[header]:
        for key in css:
          if 'width' in key.lower():
            found_w = True
            w = int(css[key].strip('%'))
            css[key] = str(w - margin[2] - margin[3]) + '%'
          if 'height' in key.lower():
            found_h = True
            h = int(css[key].strip('%'))
            css[key] = str(h - margin[0] - margin[1]) + '%'
      if not found_w:
        self.slide_header[header].append({'width': str(100 - margin[2] - margin[3]) + '%'})
      if not found_h:
        self.slide_header[header].append({'height': str(10 - margin[0] - margin[1]) + '%'})

  def __check_slide_footers_dimensions(self):
    """Ensure dimensions assignment for slide footers theme."""
    for footer in self.slide_footer:
      # search for eventual margins
      #         top, bottom, right, left
      margin = [0, 0, 0, 0]
      for css in self.slide_footer[footer]:
        for key in css:
          if 'margin-top' in key.lower():
            margin[0] = int(css[key].strip('%'))
          if 'margin-bottom' in key.lower():
            margin[1] = int(css[key].strip('%'))
          if 'margin-right' in key.lower():
            margin[2] = int(css[key].strip('%'))
          if 'margin-left' in key.lower():
            margin[3] = int(css[key].strip('%'))
      # checking dimensions
      found_w = False
      found_h = False
      for css in self.slide_footer[footer]:
        for key in css:
          if 'width' in key.lower():
            found_w = True
            w = int(css[key].strip('%'))
            css[key] = str(w - margin[2] - margin[3]) + '%'
          if 'height' in key.lower():
            found_h = True
            h = int(css[key].strip('%'))
            css[key] = str(h - margin[0] - margin[1]) + '%'
      if not found_w:
        self.slide_footer[footer].append({'width': str(100 - margin[2] - margin[3]) + '%'})
      if not found_h:
        self.slide_footer[footer].append({'width': str(10 - margin[0] - margin[1]) + '%'})

  @staticmethod
  def __check_active(decorator):
    """Check if a decorator is active.

    Parameters
    ----------
    decorator: list
      list of css attributes

    Returns
    -------
    bool:
      active status
    """
    active = False
    for css in decorator:
      for key in css:
        if 'active' in key.lower():
          active = css[key].lower() == 'yes'
    return active

  @staticmethod
  def __get_attribute(attribute, css_list):
    """Get css attribute from css_list.

    Parameters
    ----------
    attribute: str
      attribute name
    css_list: list
      list of css attributes

    Returns
    -------
    str:
      attribute value
    """
    for css in css_list:
      for key in css:
        if attribute in key.lower():
          return css[key]
    return ''

  def __get_slide_content_height(self):
    """Get the height of the slide content from the headers and footers remainder height.

    Returns
    -------
    height: str
    """
    height = 0
    for header in self.slide_header:
      active = self.__check_active(decorator=self.slide_header[header])
      if active:
        height += int(self.__get_attribute(attribute='height', css_list=self.slide_header[header]).strip('%'))
        margin = self.__get_attribute(attribute='margin-top', css_list=self.slide_header[header]).strip('%')
        if margin != '':
          height += int(margin)
        margin = self.__get_attribute(attribute='margin-bottom', css_list=self.slide_header[header]).strip('%')
        if margin != '':
          height += int(margin)
    for footer in self.slide_footer:
      active = self.__check_active(decorator=self.slide_footer[footer])
      if active:
        height += int(self.__get_attribute(attribute='height', css_list=self.slide_footer[footer]).strip('%'))
        margin = self.__get_attribute(attribute='margin-top', css_list=self.slide_footer[footer]).strip('%')
        if margin != '':
          height += int(margin)
        margin = self.__get_attribute(attribute='margin-bottom', css_list=self.slide_footer[footer]).strip('%')
        if margin != '':
          height += int(margin)
    return 100 - height

  def __get_slide_content_width(self):
    """Get the width of the slide content from the sidebars remainder width.

    Returns
    -------
    width: str
    """
    width = 0
    for sidebar in self.slide_sidebar:
      active = self.__check_active(decorator=self.slide_sidebar[sidebar])
      if active:
        width += int(self.__get_attribute(attribute='width', css_list=self.slide_sidebar[sidebar]).strip('%'))
        margin = self.__get_attribute(attribute='margin-left', css_list=self.slide_sidebar[sidebar]).strip('%')
        if margin != '':
         width += int(margin)
        margin = self.__get_attribute(attribute='margin-right', css_list=self.slide_sidebar[sidebar]).strip('%')
        if margin != '':
         width += int(margin)
    return 100 - width

  def __check_slide_sidebars_dimensions(self):
    """Ensure dimensions assignment for slide sidebars theme."""
    height = self.__get_slide_content_height()
    for sidebar in self.slide_sidebar:
      # search for eventual margins
      #         top, bottom, right, left
      margin = [0, 0, 0, 0]
      for css in self.slide_sidebar[sidebar]:
        for key in css:
          if 'margin-top' in key.lower():
            margin[0] = int(css[key].strip('%'))
          if 'margin-bottom' in key.lower():
            margin[1] = int(css[key].strip('%'))
          if 'margin-right' in key.lower():
            margin[2] = int(css[key].strip('%'))
          if 'margin-left' in key.lower():
            margin[3] = int(css[key].strip('%'))
      # checking dimensions
      found_w = False
      found_h = False
      for css in self.slide_sidebar[sidebar]:
        for key in css:
          if 'width' in key.lower():
            found_w = True
            w = int(css[key].strip('%'))
            css[key] = str(w - margin[2] - margin[3]) + '%'
          if 'height' in key.lower():
            found_h = True
            h = int(css[key].strip('%'))
            css[key] = str(h - margin[0] - margin[1]) + '%'
      if not found_w:
        self.slide_sidebar[sidebar].append({'width': '10%'})
        self.slide_sidebar[sidebar].append({'width': str(10 - margin[2] - margin[3]) + '%'})
      if not found_h:
        self.slide_sidebar[sidebar].append({'height': str(height - margin[0] - margin[1]) + '%'})

  def __check_slide_content_dimensions(self):
    """Ensure dimensions assignment for slide content theme."""
    height = self.__get_slide_content_height()
    width = self.__get_slide_content_width()
    # search for eventual margins
    #         top, bottom, right, left
    margin = [0, 0, 0, 0]
    for css in self.slide_content:
      for key in css:
        if 'margin-top' in key.lower():
          margin[0] = int(css[key].strip('%'))
        if 'margin-bottom' in key.lower():
          margin[1] = int(css[key].strip('%'))
        if 'margin-right' in key.lower():
          margin[2] = int(css[key].strip('%'))
        if 'margin-left' in key.lower():
          margin[3] = int(css[key].strip('%'))
    # checking dimensions
    found_w = False
    found_h = False
    for css in self.slide_content:
      for key in css:
        if 'width' in key.lower():
          css[key] = str(width - margin[2] - margin[3]) + '%'
          found_w = True
        if 'height' in key.lower():
          css[key] = str(height - margin[0] - margin[1]) + '%'
          found_h = True
    if not found_w:
      self.slide_content.append({'width': str(width - margin[2] - margin[3]) + '%'})
    if not found_h:
      self.slide_content.append({'height': str(height - margin[0] - margin[1]) + '%'})

  def __check_slide(self):
    """Chack slide consistency."""
    # css attributes
    # main slide
    self.check_css_attribute(name='display', value='block', css_list=self.slide)
    # content
    self.check_css_attribute(name='display', value='block', css_list=self.slide_content)
    self.check_css_attribute(name='float', value='left', css_list=self.slide_content)
    # headers
    for header in self.slide_header:
      self.check_css_attribute(name='display', value='block', css_list=self.slide_header[header])
      self.check_css_attribute(name='active', value='yes', css_list=self.slide_header[header], retain=True)
    # footers
    for footer in self.slide_footer:
      self.check_css_attribute(name='display', value='block', css_list=self.slide_footer[footer])
      self.check_css_attribute(name='active', value='yes', css_list=self.slide_footer[footer], retain=True)
    # sidebars
    for sidebar in self.slide_sidebar:
      self.check_css_attribute(name='display', value='block', css_list=self.slide_sidebar[sidebar])
      self.check_css_attribute(name='float', value='left', css_list=self.slide_sidebar[sidebar])
      self.check_css_attribute(name='position', value='R', css_list=self.slide_sidebar[sidebar], retain=True)
      self.check_css_attribute(name='active', value='yes', css_list=self.slide_sidebar[sidebar], retain=True)
    # dimensions
    self.__check_slide_dimensions()
    self.__check_slide_headers_dimensions()
    self.__check_slide_footers_dimensions()
    self.__check_slide_sidebars_dimensions()
    self.__check_slide_content_dimensions()

  def __get_slide(self, data):
    """
    Get slide theme.

    Parameters
    ----------
    data: dict
    """
    if 'slide' in data:
      slide = data['slide']
      if slide is not None:
        for slide_element in slide:
          for key in slide_element:
            if key is not None:
              if 'content' not in key and 'header' not in key and 'footer' not in key and 'sidebar' not in key:
                self.slide.append(slide_element)
              if 'content' in key:
                self.slide_content = slide_element[key]
              if 'header' in key:
                self.slide_header[key] = slide_element[key]
              if 'footer' in key:
                self.slide_footer[key] = slide_element[key]
              if 'sidebar' in key:
                self.slide_sidebar[key] = slide_element[key]
      self.__check_slide()
      self.__get_slide_decorators_metadata()

  def __get_box_like(self, env, data):
    """
    Get box-like theme (box, note, table, figure, video).

    Parameters
    ----------
    data: dict
    """
    if env in data:
      env_data = data[env]
      for env_element in env_data:
        for key in env_element:
          if 'caption' not in key.lower() and 'content' not in key.lower():
            getattr(self, env).append(env_element)
          if 'caption' in key.lower():
            setattr(self, env + '_caption', env_element[key])
          if 'content' in key.lower():
            setattr(self, env + '_content', env_element[key])

  def __get_css(self):
    """Construct CSS theme."""
    css = []
    css.append(self.theme2css(div='body', div_id=self.div_id, klass='', theme_list=self.canvas))
    css.append(self.theme2css(div='ol li', div_id=self.div_id, klass='', theme_list=self.ordered_list))
    css.append(self.theme2css(div='ul li', div_id=self.div_id, klass='', theme_list=self.unordered_list))
    css.append(self.theme2css(div='ol li:before', div_id=self.div_id, klass='', theme_list=self.ordered_list_items))
    css.append(self.theme2css(div='ul li:before', div_id=self.div_id, klass='', theme_list=self.unordered_list_items))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='toc', theme_list=self.toc))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='toc-chapter-emph', theme_list=self.toc_chapter_emph))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='toc-section-emph', theme_list=self.toc_section_emph))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='toc-subsection-emph', theme_list=self.toc_subsection_emph))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='toc-slide-emph', theme_list=self.toc_slide_emph))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='slide', theme_list=self.slide))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='slide-content', theme_list=self.slide_content))
    for header in self.slide_header:
      css.append(self.theme2css(div='', div_id=self.div_id, klass='slide-' + header, theme_list=self.slide_header[header]))
    for footer in self.slide_footer:
      css.append(self.theme2css(div='', div_id=self.div_id, klass='slide-' + footer, theme_list=self.slide_footer[footer]))
    for sidebar in self.slide_sidebar:
      css.append(self.theme2css(div='', div_id=self.div_id, klass='slide-' + sidebar, theme_list=self.slide_sidebar[sidebar]))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='box', theme_list=self.box))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='box-caption', theme_list=self.box_caption))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='box-content', theme_list=self.box_content))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='note', theme_list=self.note))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='note-caption', theme_list=self.note_caption))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='note-content', theme_list=self.note_content))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='table', theme_list=self.table))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='table-caption', theme_list=self.table_caption))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='table-content', theme_list=self.table_content))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='figure', theme_list=self.figure))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='figure-caption', theme_list=self.figure_caption))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='figure-content', theme_list=self.figure_content))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='video', theme_list=self.video))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='video-caption', theme_list=self.video_caption))
    css.append(self.theme2css(div='', div_id=self.div_id, klass='video-content', theme_list=self.video_content))
    self.css = ''.join(css)

  def get(self, source, name='theme', div_id=''):
    """
    Get theme from source stream.

    Parameters
    ----------
    source: str
    name: str
    div_id: str
    """
    self.div_id = div_id
    if len(source) > 0:
      try:
        for data in load_all(source, Loader=FullLoader):
          if name in data:
            for element in data[name]:
              self.__get_copy_from(data=element)
              self.__get_canvas(data=element)
              self.__get_ordered_list(data=element)
              self.__get_unordered_list(data=element)
              self.__get_ordered_list_items(data=element)
              self.__get_unordered_list_items(data=element)
              self.__get_toc(data=element)
              self.__get_slide(data=element)
              self.__get_box_like(env='box', data=element)
              self.__get_box_like(env='note', data=element)
              self.__get_box_like(env='table', data=element)
              self.__get_box_like(env='figure', data=element)
              self.__get_box_like(env='video', data=element)
        self.custom = True
      except YAMLError:
        print('No valid definition of theme has been found')
    self.__get_css()

  def get_slide_decorators_metadata(self, decorator, name):
    """Get the slide decorators (headers, footers, sidebars) metadata placeholders.

    Parameters
    ----------
    decorator: str
      header|footer|sidebar
    name: str
      header-1, header-2, ... footer-1,...

    Returns
    -------
    str:
      metadata placeholder
    """
    metadata = getattr(self, 'slide_' + decorator + '_metadata')[name]
    placeholders = []
    for data in metadata:
      placeholders.append(r'$' + data + r'[' + metadata[data] + ']')
    return ''.join(placeholders)

  def get_slide_transition(self):
    """Get slide transition (positioning) informations.

    Returns
    -------
    dict:
      dictionary of the slides-transition informations
    """
    infos = {}
    transition = self.__get_attribute(attribute='transition', css_list=self.slide)
    if transition == '':
      transition = 'horizontal'
    infos['transition'] = transition

    width = self.__get_attribute(attribute='width', css_list=self.slide)
    if width == '':
      width = '900px'
    infos['width'] = int(width.strip('px'))

    height = self.__get_attribute(attribute='height', css_list=self.slide)
    if height == '':
      height = '700px'
    infos['height'] = int(height.strip('px'))

    offset = self.__get_attribute(attribute='data-offset', css_list=self.slide)
    if offset == '':
      offset = '10'
    infos['offset'] = int(offset)

    scale = self.__get_attribute(attribute='scale', css_list=self.slide)
    if scale == '':
      scale = '1'
    infos['scale'] = int(scale)

    infos['data-x'] = self.__get_attribute(attribute='data-x', css_list=self.slide)
    infos['data-y'] = self.__get_attribute(attribute='data-y', css_list=self.slide)
    infos['data-z'] = self.__get_attribute(attribute='data-z', css_list=self.slide)
    infos['data-rotate-x'] = self.__get_attribute(attribute='data-rotate-x', css_list=self.slide)
    infos['data-rotate-y'] = self.__get_attribute(attribute='data-rotate-y', css_list=self.slide)
    infos['data-rotate-z'] = self.__get_attribute(attribute='data-rotate-z', css_list=self.slide)
    return infos
