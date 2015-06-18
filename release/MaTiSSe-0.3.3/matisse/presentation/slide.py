#!/usr/bin/env python
"""
slide.py, module definition of Slide class.
This defines a slide of the presentation.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import re
# modules not in the standard library
from yattag import Doc
# MaTiSSe.py modules
from ..config import __config__
from ..theme import box
from ..theme import columns
from ..theme import figure
from ..theme import note
from ..theme import table
from ..theme.theme import Theme
from ..utils.source_editor import __source_editor__ as seditor
from ..utils.source_editor import obfuscate_codeblocks as obfuscate
from ..utils.source_editor import illuminate_protected as illuminate


# class definition
class Slide(object):
  """
  Slide is an object that handles a single slide, its attributes and methods.

  Attributes
  ----------
  slides_number : int
    global number of slides (equals to the number of Slide instances)
  """
  slides_number = 0

  @classmethod
  def reset(cls):
    """Method resetting Slide to initial values."""
    cls.slides_number = 0
    return

  def __init__(self, raw_body='', title='', data=None, theme=None, local_number=1):
    """
    Parameters
    ----------
    raw_body : str, optional
      string containing the body of the slide in raw format
    title : str, optional
      slide title
    data : OrderedDict object, optional
      slide metadata
    local_number : int, optional
      subsection number in local-to-section numeration

    Attributes
    ----------
    raw_body : str
      string containing the body of the slide in raw format
    number : int
      slide number in global numeration
    local_number : int
      subsection number in local-to-subsection numeration
    title : str
      slide title
    data : OrderedDict object
      slide metadata
    overtheme : Theme object
      overriding theme of the current slide
    """
    Slide.slides_number += 1
    self.raw_body = raw_body
    self.number = Slide.slides_number
    self.local_number = local_number
    self.title = title
    self.data = OrderedDict()
    if data:
      for key, val in data.items():
        self.data[key] = val
    self.data['slidetitle'] = self.title
    self.data['slidenumber'] = str(self.number)
    self.overtheme = None
    self.__get_overtheme(theme=theme)
    # metadata autoparsing...
    for meta in ['sectiontitle', 'subsectiontitle', 'slidetitle']:
      if meta in self.data:
        self.data[meta] = self.parse_metadata(source=self.data[meta])
    return

  def __get_overtheme(self, theme=None):
    """Method for checking if the slide has a personal theme overriding the global one.

    Parameters
    ----------
    theme: Theme object, optional
      base theme used to set other overtheme data not being defined
    """
    source = seditor.get_overtheme(source=self.raw_body)
    if source:
      self.overtheme = Theme(source=source)
      if theme:
        self.overtheme.set_from(other=theme)
      self.overtheme.slide.adjust_dims()
      self.raw_body = seditor.strip_overtheme(self.raw_body)
      if __config__.verbose:
        print('Found overriding theme for slide n. ' + str(self.number))
        print(self.get_css(only_custom=True))
    return

  def get_css(self, only_custom=False):
    """Method returning slide's css.

    Parameters
    ----------
    only_custom : bool, optional
      consider only (user) customized data

    Returns
    -------
    str
      a string containing the css code of the theme
    """
    css = []
    if self.overtheme:
      css = self.overtheme.slide.get_css(only_custom=only_custom, as_list=True)
    if len(css) > 0:
      return ''.join(['\n#slide-' + str(self.number) + c[1:] for c in css])
    else:
      return ''

  def put_attributes(self, doc):
    """Method for putting html attibutes of the slide.

    Parameters
    ----------
    """
    doc.attr(('id', 'slide-' + str(self.number)))
    doc.attr(('title', self.title))
    if 'sectiontitle' in self.data:
      doc.attr(('sectiontitle', self.data['sectiontitle']))
    if 'sectionnumber' in self.data:
      doc.attr(('sectionnumber', self.data['sectionnumber']))
    if 'subsectiontitle' in self.data:
      doc.attr(('subsectiontitle', self.data['subsectiontitle']))
    if 'subsectionnumber' in self.data:
      doc.attr(('subsectionnumber', self.data['subsectionnumber']))
    return

  def metadata_to_html(self, metadata, style=None):
    """Method for converting slide level metadata to html.

    Parameters
    ----------
    metadata : str
      metadata key
    style : str, optional
      css style of metadata tag

    Returns
    -------
    str
      html string containing the metadata
    """
    doc = Doc()
    with doc.tag('span', klass='metadata'):
      if style:
        doc.attr(style=style)
      doc.asis(self.data[metadata])
    return doc.getvalue()

  def parse_metadata(self, source):
    """Method for parsing metadata of slide level that are not parsed from presentation metadata parsing.

    The slide level metadata are:
    + sectiontitle: the title of each section that is obtained parsing your source;
    + sectionnumber: the number of each section that is obtained parsing your source;
    + subsectiontitle: the title of each subsection that is obtained parsing your source;
    + subsectionnumber: the number of each subsection that is obtained parsing your source;
    + slidetitle: the title of each slide that is obtained parsing your source;
    + slidenumber: the number of each slide that is obtained parsing your source.
    """
    protected, obfuscate_source = obfuscate(source=source)
    for meta in ['sectiontitle', 'sectionnumber', 'subsectiontitle', 'subsectionnumber', 'slidetitle', 'slidenumber']:
      if meta != 'toc':
        regex = re.compile(r"\$" + meta + r"(\[(?P<style>.*?)\])*", re.DOTALL)
        for match in re.finditer(regex, obfuscate_source):
          style = None
          if match.group('style'):
            style = str(match.group('style'))
          obfuscate_source = re.sub(regex, lambda x: self.metadata_to_html(metadata=meta, style=style), obfuscate_source, 1)
    return illuminate(source=obfuscate_source, protected_contents=protected)

  def raw_body_parse(self):
    """Method for parsing raw_body.

    Returns
    -------
    str
      string containing the parsed raw_body
    """
    tokens = columns.tokenize(source=self.raw_body)
    parsed_body = ''
    for token in tokens:
      if token[0] == 'unknown':
        content = box.parse(token[1])
        content = figure.parse(content)
        content = table.parse(content)
        content = note.parse(content)
        parsed_body += '\n' + seditor.md_convert(content)
      elif token[0] == 'columns':
        parsed_body += '\n' + columns.parse(source=token[1])
    return self.parse_metadata(source=parsed_body)

  def to_html(self, position, theme):
    """Convert slide content into html format.

    Parameters
    ----------
    position : SlidePosition object
      current slide position
    doc : yattag.Doc object
      the main html doc
    theme : Theme object
      the base theme
    """
    doc = Doc()
    with doc.tag('div'):
      self.put_attributes(doc=doc)
      # get slide positioning data
      actual_theme = None
      if self.overtheme:
        actual_theme = self.overtheme.slide
      else:
        actual_theme = theme
      position.set_position(theme=actual_theme)
      if self.title != '$overview':
        doc.attr(('class', 'step slide'))
        doc.attr(('data-x', str(position.position[0])))
        doc.attr(('data-y', str(position.position[1])))
        doc.attr(('data-z', str(position.position[2])))
        doc.attr(('data-scale', str(position.scale)))
        doc.attr(('data-rotate-x', str(position.rotation[0])))
        doc.attr(('data-rotate-y', str(position.rotation[1])))
        doc.attr(('data-rotate-z', str(position.rotation[2])))
        # inserting elements
        for header in actual_theme.loop_over_headers():
          header.to_html(doc=doc, metadata=self.data)
        for sidebar in actual_theme.loop_over_sidebars():
          if sidebar.position == 'L':
            sidebar.to_html(doc=doc, metadata=self.data)
        actual_theme.content.to_html(doc=doc, content='\n' + self.raw_body_parse())
        for sidebar in actual_theme.loop_over_sidebars():
          if sidebar.position == 'R':
            sidebar.to_html(doc=doc, metadata=self.data)
        for footer in actual_theme.loop_over_footers():
          footer.to_html(doc=doc, metadata=self.data)
      else:
        doc.attr(('class', 'step overview'))
        doc.attr(('style', ''))
        doc.attr(('data-x', str(position.position[0])))
        doc.attr(('data-y', str(position.position[1])))
        doc.attr(('data-z', str(position.position[2])))
        # doc.attr(('data-scale',str(position.scale)))
        doc.attr(('data-scale', '100'))
    return doc.getvalue()
