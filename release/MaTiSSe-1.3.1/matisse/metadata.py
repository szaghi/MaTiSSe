#!/usr/bin/env python
"""
metadata.py, module definition of Metadata class.
"""
from __future__ import print_function
import re
import sys
from yattag import Doc


class Metadata(object):
  """
  Object for handling metadata.
  """

  @classmethod
  def reset(cls):
    """Reset to default state."""
    return

  def __init__(self, name, value=None):
    """
    Parameters
    ----------
    name : str
    value : str|[str]
    """
    self.name = name
    self.value = value
    self.regex = re.compile(r"\$" + self.name + r"(\[(?P<style>.*?)\])*", re.DOTALL)
    return

  def update_value(self, value):
    """Update metadata value.

    value: str|[str]
    """
    if isinstance(self.value, list):
      if not isinstance(value, list):
        sys.stderr.write('Error: the value of metadata "' + self.name + '" must be a list!')
        sys.exit(1)
      for val in value:
        self.value.append(str(val))
    else:
      self.value = str(value)

  def parse(self, parser, source, toc_depth=None, max_time=None, current=None):
    """Parse source for metadata placeholder substituting occurences with its value and its eventula css style.

    Parameters
    ----------
    parser: Parser
    source: str
    max_time: str
      max time for presentation
    """
    codeblocks = parser.tokenizer(source=source, re_search=parser.regexs['codeblock'])
    metadatablocks = parser.tokenizer(source=source, re_search=self.regex, exclude=codeblocks)
    if len(metadatablocks) > 0:
      parsed_source = source[:metadatablocks[0]['start']]
      for m, metadatablock in enumerate(metadatablocks[:-1]):
        parsed_source += self.to_html(match=metadatablock['match'], toc_depth=toc_depth, max_time=max_time, current=current) + source[metadatablock['end']:metadatablocks[m + 1]['start']]
      parsed_source += self.to_html(match=metadatablocks[-1]['match'], toc_depth=toc_depth, max_time=max_time, current=current) + source[metadatablocks[-1]['end']:]
      return parsed_source
    return source

  def logo_to_html(self, match):
    """Convert logo metadata to html stream.

    Parameters
    ----------
    match: re.match object

    Returns
    -------
    str:
      html stream
    """
    doc = Doc()
    style = None
    if match.group('style'):
      style = str(match.group('style'))
    if style is not None:
      doc.stag('img', src=self.value, alt=self.value, style=style)
    else:
      doc.stag('img', src=self.value, alt=self.value)
    return doc.getvalue()

  def timer_to_html(self, match, max_time):
    """Convert custom metadata to html stream.

    Parameters
    ----------
    match: re.match object
    max_time: str

    Returns
    -------
    str:
      html stream
    """
    doc = Doc()
    with doc.tag('span', klass='timercontainer'):
      style = None
      if match.group('style'):
        style = str(match.group('style'))
      if style:
        doc.attr(style=style)
      with doc.tag('div', klass='countDown'):
        with doc.tag('div'):
          doc.attr(klass='timer')
        if style:
          if 'controls' in style:
            with doc.tag('div', klass='timercontrols'):
              with doc.tag('input', type='button'):
                doc.attr(klass='btn reset', onclick='resetCountdown(' + str(max_time) + ');', value=' &#10227; ', title='reset')
              with doc.tag('input', type='button'):
                doc.attr(klass='btn stop', onclick='stopCountdown();', value=' &#9724; ', title='pause')
              with doc.tag('input', type='button'):
                doc.attr(klass='btn start', onclick='startCountdown();', value=' &#9654; ', title='start')
    return doc.getvalue().replace('amp;', '')

  @staticmethod
  def toc_put_text(doc, klass, current, text):
    """Put text of current TOC element.

    Parameters
    ----------
    doc: Doc()
    klass: str
    current: list
    text: str
    """
    if text != '':
      with doc.tag('span', klass=klass):
        doc.text('  ' * (len(current) - 1) + '.'.join(str(c) for c in current) + ' ' + text)

  @staticmethod
  def toc_put_slides(doc, subsection, depth, actual_current, current, numbering_start):
    """Put slides list into TOC.

    Parameters
    ----------
    doc: Doc()
    subsection: dict
      dictionary of slides contained into the subsection
    depth: int
    actual_current: list
    current: list
    numbering_start: int
    """
    for slide in subsection:
      actual_current[3] += 1
      if depth >= 4:
        with doc.tag('a', href='#slide-' + str(actual_current[4])):
          if current is not None and current[0:4] == actual_current[0:4]:
            Metadata.toc_put_text(doc=doc, klass='toc-slide-emph', current=actual_current[numbering_start:4], text=slide)
          else:
            Metadata.toc_put_text(doc=doc, klass='toc-slide', current=actual_current[numbering_start:4], text=slide)
      actual_current[4] += 1

  @staticmethod
  def toc_put_subsections(doc, section, depth, actual_current, current, numbering_start):
    """Put subsections list into TOC.

    Parameters
    ----------
    doc: Doc()
    section: dict
      dictionary of subsections contained into the section
    depth: int
    actual_current: list
    current: list
    numbering_start: int
    """
    for subsection in section:
      actual_current[2] += 1
      actual_current[3] = 0
      if depth >= 3:
        with doc.tag('a', href='#slide-' + str(actual_current[4])):
          if current is not None and current[0:3] == actual_current[0:3]:
            Metadata.toc_put_text(doc=doc, klass='toc-subsection-emph', current=actual_current[numbering_start:3], text=subsection)
          else:
            Metadata.toc_put_text(doc=doc, klass='toc-subsection', current=actual_current[numbering_start:3], text=subsection)
      if subsection == '' and len(section) == 1:
        next_numbering_start = numbering_start + 1
      else:
        next_numbering_start = numbering_start
      Metadata.toc_put_slides(doc=doc,
                              subsection=section[subsection],
                              depth=depth,
                              actual_current=actual_current,
                              current=current,
                              numbering_start=next_numbering_start)

  @staticmethod
  def toc_put_sections(doc, chapter, depth, actual_current, current, numbering_start):
    """Put sections list into TOC.

    Parameters
    ----------
    doc: Doc()
    chapter: dict
      dictionary of sections contained into the chapter
    depth: int
    actual_current: list
    current: list
    numbering_start: int
    """
    for section in chapter:
      actual_current[1] += 1
      actual_current[2] = 0
      actual_current[3] = 0
      if depth >= 2:
        with doc.tag('a', href='#slide-' + str(actual_current[4])):
          if current is not None and current[0:2] == actual_current[0:2]:
            Metadata.toc_put_text(doc=doc, klass='toc-section-emph', current=actual_current[numbering_start:2], text=section)
          else:
            Metadata.toc_put_text(doc=doc, klass='toc-section', current=actual_current[numbering_start:2], text=section)
      if section == '' and len(chapter) == 1:
        next_numbering_start = numbering_start + 1
      else:
        next_numbering_start = numbering_start
      Metadata.toc_put_subsections(doc=doc,
                                   section=chapter[section],
                                   depth=depth,
                                   actual_current=actual_current,
                                   current=current,
                                   numbering_start=next_numbering_start)

  def toc_put_chapters(self, doc, depth, actual_current, current):
    """Put chapters list into TOC.

    Parameters
    ----------
    doc: Doc()
    depth: int
    actual_current: list
    current: list
    """
    for chapter in self.value:
      actual_current[0] += 1
      actual_current[1] = 0
      actual_current[2] = 0
      actual_current[3] = 0
      with doc.tag('a', href='#slide-' + str(actual_current[4])):
        if current is not None and current[0] == actual_current[0]:
          self.toc_put_text(doc=doc, klass='toc-chapter-emph', current=actual_current[0:1], text=chapter)
        else:
          self.toc_put_text(doc=doc, klass='toc-chapter', current=actual_current[0:1], text=chapter)
      if chapter == '' and len(self.value) == 1:
        numbering_start = 1
      else:
        numbering_start = 0
      self.toc_put_sections(doc=doc,
                            chapter=self.value[chapter],
                            depth=depth,
                            actual_current=actual_current,
                            current=current,
                            numbering_start=numbering_start)

  def toc_to_html(self, match, current=None, depth=1):
    """Convert TOC to a plain string.

    Parameters
    ----------
    match: re.match()
    current: [current_chapter, current_section, current_subsection, current_slide]
      eventual current chpater-section-subsection-slide number
    depth: int
      depth of TOC: 4 => up-to slides, 3 => up-to subsections, 2 => up-to sections, 1 => only chapters

    Returns
    -------
    str:
      plain string of TOC
    """
    def get_style(match):
      """Get TOC style if one.

      Parameters
      ----------
      match: re.match()

      Returns
      -------
      str:
        style
      """
      style = None
      if match.group('style'):
        style = str(match.group('style'))
      return style

    def get_actual_depth(style, depth):
      """Get the actual depth of TOC using the eventual provided depth or the one defined into the style.

      Parameters
      ----------
      style: str
      depth: int
        depth of TOC: 4 => up-to slides, 3 => up-to subsections, 2 => up-to sections, 1 => only chapters

      Returns
      -------
      int:
        actual depth
      """
      actual_depth = int(depth)
      if style is not None:
        if 'depth' in style.lower():
          match_depth = re.search(r'depth\:(?P<depth>[1-4])\;*', style)
          if match_depth.group('depth'):
            actual_depth = int(match_depth.group('depth'))
      return actual_depth

    style = get_style(match=match)
    actual_depth = get_actual_depth(style=style, depth=depth)
    doc = Doc()
    # numbering: [local_chap, local_sec, local_subsec, local_slide, global_slide]
    actual_current = [0, 0, 0, 0, 1]
    with doc.tag('div', klass='toc'):
      if style is not None:
        doc.attr(style=style)
      self.toc_put_chapters(doc=doc,
                            depth=actual_depth,
                            actual_current=actual_current,
                            current=current)
    return '\n' + doc.getvalue()

  def custom_to_html(self, match):
    """Convert custom metadata to html stream.

    Parameters
    ----------
    match: re.match object

    Returns
    -------
    str:
      html stream
    """
    doc = Doc()
    with doc.tag('span', klass='metadata'):
      style = None
      if match.group('style'):
        style = str(match.group('style'))
      if style:
        doc.attr(style=style)
        doc.asis(re.search(r'value\:(?P<value>.*?)\;', style).group('value'))
    return doc.getvalue()

  def to_html(self, match, toc_depth=None, max_time=None, current=None):
    """Convert logo metadata to html stream.

    Parameters
    ----------
    match: re.match object
    max_time: str
      max time for presentation

    Returns
    -------
    str:
      html stream
    """
    if 'toc' in self.name:
      return self.toc_to_html(match=match, current=current, depth=int(toc_depth))
    if 'logo' in self.name:
      return self.logo_to_html(match)
    elif 'timer' in self.name:
      return self.timer_to_html(match=match, max_time=max_time)
    elif 'custom' in self.name:
      return self.custom_to_html(match)
    else:
      doc = Doc()
      with doc.tag('span', klass='metadata'):
        style = None
        if match.group('style'):
          style = str(match.group('style'))
        if style:
          doc.attr(style=style)
        if isinstance(self.value, list):
          doc.asis(', '.join(self.value))
        else:
          doc.asis(str(self.value))
    return doc.getvalue()
