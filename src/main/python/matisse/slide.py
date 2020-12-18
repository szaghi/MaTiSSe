#!/usr/bin/env python
"""
slide.py, module definition of Slide class.
"""
from __future__ import absolute_import
from __future__ import print_function
from .box import Box
from .columns import Columns
from .figure import Figure
from .markdown_utils import markdown2html
from .note import Note
from .table import Table
from .theme import Theme
from .video import Video


class Slide(object):
  """
  Slide object.
  """

  @classmethod
  def reset(cls):
    """Reset to default state."""
    return

  def __init__(self, number, position=None, title=None, contents=None):
    """"
    Paramters
    ---------
    number: int
      slide global numeration
    position: dict
      position dictionary containing {'x': posx, 'y': posy, 'z': posz, 'rotx': rotx, 'roty': roty, 'rotz': rotz, 'scale': scaling}
    title: str
    contents: str
    """
    self.number = number
    self.position = None
    self.set_position(position)
    self.title = title
    self.contents = contents
    self.overtheme = Theme()
    return

  def __str__(self):
    strings = [str(self.title)]
    strings.append(str(self.contents))
    return ''.join(strings)

  def get_overtheme(self, parser):
    """Get eventaul overtheme definition.

    Parameters
    ----------
    parser: Parser
    """
    codeblocks = parser.tokenizer(source=self.contents, re_search=parser.regexs['codeblock'])
    yamlblocks = parser.tokenizer(source=self.contents, re_search=parser.regexs['yamlblock'], exclude=codeblocks)
    if len(yamlblocks) > 0:
      self.overtheme.get(source=''.join([block['match'].group().strip('---') for block in yamlblocks]),
                         name='overtheme',
                         div_id='slide-' + str(self.number))
      purged_contents = self.contents[:yamlblocks[0]['start']]
      for b, yamlblock in enumerate(yamlblocks[:-1]):
        purged_contents += self.contents[yamlblock['end']:yamlblocks[b + 1]['start']]
      purged_contents += self.contents[yamlblocks[-1]['end']:]
      self.contents = purged_contents

  def set_position(self, position):
    """Set slide position.

    Parameters
    ----------
    position: dict
      position dictionary containing {'x': posx, 'y': posy, 'z': posz, 'rotx': rotx, 'roty': roty, 'rotz': rotz, 'scale': scaling}
    """
    if position is not None:
      self.position = {}
      for key in position:
        self.position[key] = position[key]

  def put_html_attributes(self, doc):
    """Put html attibutes of the slide.

    Parameters
    ----------
    doc: Doc
    """
    doc.attr(('id', 'slide-' + str(self.number)))
    # doc.attr(('title', str(self.title)))
    doc.attr(('class', 'step slide'))
    doc.attr(('data-x', str(self.position['x'])))
    doc.attr(('data-y', str(self.position['y'])))
    doc.attr(('data-z', str(self.position['z'])))
    doc.attr(('data-scale', str(self.position['scale'])))
    doc.attr(('data-rotate-x', str(self.position['rotx'])))
    doc.attr(('data-rotate-y', str(self.position['roty'])))
    doc.attr(('data-rotate-z', str(self.position['rotz'])))
    return

  def to_html(self, doc, parser, metadata, theme, current):
    """Generate html from self.

    Parameters
    ----------
    doc: Doc
    parser: Parser
    metatadata: dict
      presentation metadata
    theme: Theme()
      presentation theme
    current: list
    """
    def _parse_env(Env, re_search, source):
      codeblocks = parser.tokenizer(source=source, re_search=parser.regexs['codeblock'])
      codes = parser.tokenizer(source=source, re_search=parser.regexs['code'], exclude=codeblocks)
      yamlblocks = parser.tokenizer(source=source, re_search=parser.regexs['yamlblock'], exclude=codeblocks + codes)
      envs = parser.tokenizer(source=source, re_search=re_search, exclude=codeblocks + yamlblocks + codes)
      if len(envs) > 0:
        parsed_source = source[:envs[0]['start']]
        for e, env in enumerate(envs[:-1]):
          current = Env(source=env['match'].group())
          parsed_source += current.to_html() + source[env['end']:envs[e + 1]['start']]
        if Env is Video:
          if self.overtheme.custom:
            current = Env(source=envs[-1]['match'].group(), theme=self.overtheme)
          else:
            current = Env(source=envs[-1]['match'].group(), theme=theme)
        else:
          current = Env(source=envs[-1]['match'].group())
        parsed_source += current.to_html() + source[envs[-1]['end']:]
        return parsed_source
      return source

    html = self.contents
    for meta in metadata:
      html = metadata[meta].parse(parser=parser, source=html, toc_depth=metadata['toc_depth'].value, max_time=metadata['max_time'].value, current=current)
    html = _parse_env(Env=Box, re_search=Box.regexs['box'], source=html)
    html = _parse_env(Env=Note, re_search=Note.regexs['note'], source=html)
    html = _parse_env(Env=Figure, re_search=Figure.regexs['figure'], source=html)
    html = _parse_env(Env=Table, re_search=Table.regexs['table'], source=html)
    html = _parse_env(Env=Video, re_search=Video.regexs['video'], source=html)
    html = _parse_env(Env=Columns, re_search=Columns.regexs['columns'], source=html)
    with doc.tag('div', klass='slide-content'):
      doc.asis(markdown2html(source=html))
    return
