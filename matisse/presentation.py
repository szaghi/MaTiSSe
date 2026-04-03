#!/usr/bin/env python3
"""
presentation.py, module definition of Presentation class.
"""
from __future__ import annotations

import os
from collections import OrderedDict
from shutil import copytree

from yaml import FullLoader, YAMLError, load_all
from yattag import Doc, indent

from .chapter import Chapter
from .metadata import Metadata
from .parser import Parser
from .position import Position
from .section import Section
from .slide import Slide
from .subsection import Subsection
from .theme import Theme


class Presentation(object):
  """
  Presentation object.

  Attributes
  ----------
  chapters_number: int
  """
  chapters_number = 0

  @classmethod
  def reset(cls):
    """Reset to default state."""
    cls.chapters_number = 0
    Theme.reset()
    Chapter.reset()

  def __init__(self):
    """
    Attributes
    ----------
    metadata: dict
      presentation metadata; each element of the dictionary if a dict with ['value', 'user'] items: value contains
      the metadata value and user indicates if the value comes from user (if True) or from defaults (if False).
    """
    self.reset()
    self.metadata = {'title': Metadata(name='title', value=''),
                     'subtitle': Metadata(name='subtitle', value=''),
                     'authors': Metadata(name='authors', value=[]),
                     'authors_short': Metadata(name='authors_short', value=[]),
                     'emails': Metadata(name='emails', value=[]),
                     'affiliations': Metadata(name='affiliations', value=[]),
                     'affiliations_short': Metadata(name='affiliations_short', value=[]),
                     'logo': Metadata(name='logo', value=''),
                     'timer': Metadata(name='timer', value=''),
                     'location': Metadata(name='location', value=''),
                     'location_short': Metadata(name='location_short', value=''),
                     'date': Metadata(name='date', value=''),
                     'conference': Metadata(name='conference', value=''),
                     'conference_short': Metadata(name='conference_short', value=''),
                     'session': Metadata(name='session', value=''),
                     'session_short': Metadata(name='session_short', value=''),
                     'max_time': Metadata(name='max_time', value='25'),
                     'total_slides_number': Metadata(name='total_slides_number', value=''),
                     'dirs_to_copy': Metadata(name='dirs_to_copy', value=[]),
                     'toc': Metadata(name='toc', value=OrderedDict()),
                     'toc_depth': Metadata(name='toc_depth', value='2'),
                     'chaptertitle': Metadata(name='chaptertitle', value=''),
                     'chapternumber': Metadata(name='chapternumber', value=''),
                     'sectiontitle': Metadata(name='sectiontitle', value=''),
                     'sectionnumber': Metadata(name='sectionnumber', value=''),
                     'subsectiontitle': Metadata(name='subsectiontitle', value=''),
                     'subsectionnumber': Metadata(name='subsectionnumber', value=''),
                     'slidetitle': Metadata(name='slidetitle', value=''),
                     'slidenumber': Metadata(name='slidenumber', value=''),
                     'css_overtheme': Metadata(name='css_overtheme', value=[]),
                     'custom': Metadata(name='custom-[0-9]*', value='')}
    self.theme = Theme()
    self.parser = Parser()
    self.chapters = []
    self.position = Position()

  def __str__(self):
    strings = [f'Chapters number {Presentation.chapters_number}']
    strings.append(f'Sections number {Chapter.sections_number}')
    strings.append(f'Subsections number {Section.subsections_number}')
    strings.append(f'Slides number {Subsection.slides_number}')
    for chapter in self.chapters:
      strings.append(str(chapter))
    return '\n'.join(strings)

  def __update_toc(self):
    """Update TOC after a new chapter (the last one) has been added."""
    self.metadata['toc'].value[self.chapters[-1].title] = self.chapters[-1].toc

  def __get_metadata(self, source):
    """
    Get metadata from source stream.

    Parameters
    ----------
    source: str
    """
    codeblocks = self.parser.tokenizer(source=source, re_search=self.parser.regexs['codeblock'])
    yamlblocks = self.parser.tokenizer(source=source, re_search=self.parser.regexs['yamlblock'], exclude=codeblocks)
    try:
      for block in yamlblocks:
        for data in load_all(block['match'].group().strip('---'), Loader=FullLoader):
          if 'metadata' in data:
            for element in data['metadata']:
              for key in element:
                if key in self.metadata:
                  self.metadata[key].update_value(value=element[key])
    except YAMLError:
      print('No valid definition of metadata has been found')

  def __get_theme(self, source):
    """
    Get theme from source stream.

    Parameters
    ----------
    source: str
    """
    codeblocks = self.parser.tokenizer(source=source, re_search=self.parser.regexs['codeblock'])
    yamlblocks = self.parser.tokenizer(source=source, re_search=self.parser.regexs['yamlblock'], exclude=codeblocks)
    self.theme.get(''.join([block['match'].group().strip('---') for block in yamlblocks]))

  def __add_chapter(self, chapter):
    """
    Add a chapter to the presentation.

    Parameters
    ----------
    chapter: Chapter
    """
    Presentation.chapters_number += 1
    self.chapters.append(chapter)
    self.__update_toc()

  def __check_bad_sectioning(self, tokens):
    """Check if the presentation has a bad sectioning.

    Parameters
    ----------
    tokens: Parser.tokens
    source: str
    """
    if '$titlepage' not in tokens['slides'][0]['match'].group().lower():
      if tokens['slides'][0]['start'] < tokens['subsections'][0]['start'] or tokens['slides'][0]['start'] < tokens['sections'][0]['start'] or tokens['slides'][0]['start'] < tokens['chapters'][0]['start']:
        print('Warning: found bad presentation sectioning!')
        print('The slide definition:')
        print(tokens['slides'][0]['match'].group() + "\n")
        print('is placed before the first defined chapter/section/subsection.')
        print('All contents before the first defined chapter/section/subsection is omitted!')
        print()

  def __put_html_tag_head(self, doc, tag, text, config):
    """Put head tag into html doc.

    Parameters
    ----------
    doc: Doc()
    tag: Tag()
    config : MatisseConfig
      MaTiSSe configuration
    """
    with tag('head'):
      doc.stag('meta', charset='utf-8')
      doc.stag('meta', author=' and '.join(self.metadata['authors'].value))
      with tag('title'):
        text(self.metadata['title'].value)
      doc.stag('meta', subtitle=self.metadata['subtitle'].value)
      doc.stag('link', rel='stylesheet', href='css/normalize.css')
      doc.stag('link', rel='stylesheet', href='css/matisse_defaults.css')
      doc.stag('link', rel='stylesheet', href='css/matisse_defaults_printing.css')
      if config.highlight:
        if config.offline:
          doc.stag('link', rel='stylesheet', href=f'js/highlight/styles/{config.highlight_style}')
        else:
          doc.stag('link', rel='stylesheet',
                   href=f'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/{config.highlight_style}')
      doc.stag('link', rel='stylesheet', href='css/theme.css')
      for css in self.metadata['css_overtheme'].value:
        doc.stag('link', rel='stylesheet', href=css)
      for chapter in self.chapters:
        for section in chapter.sections:
          for subsection in section.subsections:
            for slide in subsection.slides:
              if slide.overtheme.custom:
                doc.stag('link', rel='stylesheet', href=f'css/slide-{slide.number}-overtheme.css')

  def __put_html_tags_scripts(self, doc, tag, config):
    """Put final tags for scripts into html doc.

    Parameters
    ----------
    doc: Doc()
    tag: Tag()
    config : MatisseConfig
      MaTiSSe configuration
    """
    with tag('script'):
      doc.attr(src='js/countDown.js')
    if config.offline:
      # --- offline mode: use local bundles ---
      with tag('script'):
        doc.attr(src='js/impress.js')
      if not config.pdf:
        with tag('script'):
          doc.asis('impress().init();')
      with tag('script'):
        doc.attr(('type', 'text/x-mathjax-config'))
        doc.text("""
          MathJax.Hub.Config({
            extensions: ["tex2jax.js"],
            jax: ["input/TeX", "output/HTML-CSS"],
            tex2jax: {
              inlineMath: [ ['$','$'] ],
              displayMath: [ ['$$','$$'] ],
              processEscapes: true
            },
            "HTML-CSS": { availableFonts: ["Neo-Euler"] }
          });
        """)
      with tag('script'):
        doc.attr(('type', 'text/javascript'))
        doc.attr(src='js/MathJax/MathJax.js')
      if config.highlight:
        with tag('script'):
          doc.attr(src='js/highlight/highlight.pack.js')
        with tag('script'):
          doc.text('hljs.initHighlightingOnLoad();')
    else:
      # --- online mode (default): CDN — impress.js 2, MathJax 3, highlight.js 11 ---
      with tag('script'):
        doc.attr(src='https://cdn.jsdelivr.net/npm/impress.js@2/dist/impress.min.js')
      if not config.pdf:
        with tag('script'):
          doc.asis('impress().init();')
      with tag('script'):
        doc.text("""
          MathJax = {
            tex: {
              inlineMath: [['$', '$']],
              displayMath: [['$$', '$$']],
              processEscapes: true
            }
          };
        """)
      with tag('script'):
        doc.attr(src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js')
      if config.highlight:
        with tag('script'):
          doc.attr(src='https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js')
        with tag('script'):
          doc.text('hljs.highlightAll();')

  def __put_html_slide_decorators(self, tag, doc, decorator, position=None, overtheme=None, current=None):
    """Put html data of headers, footers and sidebars.

    Parameters
    ----------
    doc: Doc
    tag: tag
    decorator: {header, footer, sidebar}
    position: {'L','R'}
      sidebars position, L => left, R => right
    current: list
    """
    if overtheme is not None and overtheme.custom:
      theme = overtheme
    else:
      theme = self.theme
    decorators = getattr(theme, 'slide_' + decorator)
    for decor in sorted(decorators):
      insert = True
      # position check for sidebars
      if decorator == 'sidebar' and position is not None:
        for css in decorators[decor]:
          for key in css:
            if 'position' in key.lower():
              pos = css[key]
              break
        insert = pos.lower() == position.lower()
      # active check
      for css in decorators[decor]:
        for key in css:
          if 'active' in key.lower():
            insert = insert and css[key].lower() == 'yes'
      if insert:
        placeholders = theme.get_slide_decorators_metadata(decorator=decorator, name=decor)
        for metadata in self.metadata:
          placeholders = self.metadata[metadata].parse(parser=self.parser, source=placeholders, toc_depth=self.metadata['toc_depth'].value, max_time=self.metadata['max_time'].value, current=current)
        if decorator != 'sidebar':
          with doc.tag('div'):
            doc.attr(style='clear: both;')
        with tag('div', klass='slide-' + decor):
          doc.asis(placeholders)

  def __make_toc_slide(self, slides_number, depth):
    """Create a Table of Contents slide at the current position.

    Parameters
    ----------
    slides_number : int
      slide number to assign
    depth : int or str
      TOC depth

    Returns
    -------
    Slide
    """
    self.position.update_position(presentation_theme=self.theme)
    return Slide(number=slides_number,
                 position=self.position.position,
                 title='Table of Contents',
                 contents=f'$toc[depth:{depth}]')

  def __build_slides(self, tokens, subsec, subsection, slides_number, slide_local_numbers,
                     titlepage_inserted, complete_source, config):
    """Build slides for one subsection token, inserting TOC slides as configured.

    Parameters
    ----------
    tokens : dict
    subsec : dict
      subsection token
    subsection : Subsection
    slides_number : int
    slide_local_numbers : list
    titlepage_inserted : bool
    complete_source : str
    config : MatisseConfig

    Returns
    -------
    slides_number : int
    titlepage_inserted : bool
    """
    for sld in tokens['slides']:
      if '$titlepage' in sld['match'].group().lower() and not titlepage_inserted:
        slide = Slide(number=0, title='titlepage',
                      contents=complete_source[sld['end']:sld['end_next']])
        slide.get_overtheme(parser=self.parser)
        if slide.overtheme.copy_from_theme is not None and slide.overtheme.copy_from_theme:
          slide.overtheme.copy_from(other=self.theme)
        self.position.update_position(presentation_theme=self.theme, overtheme=slide.overtheme)
        slide.set_position(position=self.position.position)
        subsection.add_slide(slide=slide)
        titlepage_inserted = True
      elif sld['start'] >= subsec['start'] and sld['start'] <= subsec['end_next']:
        slide_local_numbers[0] += 1
        slide_local_numbers[1] += 1
        slide_local_numbers[2] += 1
        if slide_local_numbers[0] == 1 and config.toc_at_chap_beginning is not None:
          slides_number += 1
          subsection.add_slide(slide=self.__make_toc_slide(slides_number, config.toc_at_chap_beginning))
        if slide_local_numbers[1] == 1 and config.toc_at_sec_beginning is not None:
          slides_number += 1
          subsection.add_slide(slide=self.__make_toc_slide(slides_number, config.toc_at_sec_beginning))
        if slide_local_numbers[2] == 1 and config.toc_at_subsec_beginning is not None:
          slides_number += 1
          subsection.add_slide(slide=self.__make_toc_slide(slides_number, config.toc_at_subsec_beginning))
        slides_number += 1
        slide = Slide(number=slides_number,
                      title=sld['match'].group('expr'),
                      contents=complete_source[sld['end']:sld['end_next']])
        slide.get_overtheme(parser=self.parser)
        if slide.overtheme.copy_from_theme is not None and slide.overtheme.copy_from_theme:
          slide.overtheme.copy_from(other=self.theme)
        self.position.update_position(presentation_theme=self.theme, overtheme=slide.overtheme)
        slide.set_position(position=self.position.position)
        subsection.add_slide(slide=slide)
    return slides_number, titlepage_inserted

  def __parse_chapters(self, tokens, complete_source, config):
    """Iterate over chapter/section/subsection/slide tokens to build the document tree.

    Parameters
    ----------
    tokens : dict
    complete_source : str
    config : MatisseConfig
    """
    chapters_number = 0
    sections_number = 0
    subsections_number = 0
    slides_number = 0
    titlepage_inserted = False
    for chap in tokens['chapters']:
      chapters_number += 1
      slide_local_numbers = [0, 0, 0]
      title = chap['match'].group('expr') or ''
      chapter = Chapter(number=chapters_number, title=title)
      for sec in tokens['sections']:
        if sec['start'] >= chap['start'] and sec['start'] <= chap['end_next']:
          sections_number += 1
          slide_local_numbers[1] = 0
          slide_local_numbers[2] = 0
          section = Section(number=sections_number, title=sec['match'].group('expr'))
          for subsec in tokens['subsections']:
            if subsec['start'] >= sec['start'] and subsec['start'] <= sec['end_next']:
              subsections_number += 1
              slide_local_numbers[2] = 0
              subsection = Subsection(number=subsections_number, title=subsec['match'].group('expr'))
              slides_number, titlepage_inserted = self.__build_slides(
                tokens=tokens, subsec=subsec, subsection=subsection,
                slides_number=slides_number, slide_local_numbers=slide_local_numbers,
                titlepage_inserted=titlepage_inserted, complete_source=complete_source, config=config)
              section.add_subsection(subsection=subsection)
          chapter.add_section(section=section)
      self.__add_chapter(chapter=chapter)
      self.metadata['total_slides_number'].update_value(value=str(Subsection.slides_number))

  def parse(self, config, source: str) -> None:
    """Parse presentation from source stream.

    Parameters
    ----------
    config : MatisseConfig
      MaTiSSe configuration
    source: str
    """
    complete_source = self.parser.includes(source=source)
    if config.print_parsed_source:
      print(complete_source)
    self.__get_metadata(source=complete_source)
    self.__get_theme(source=complete_source)
    new_theme = Theme()
    new_theme.set_from(other=self.theme)
    tokens = self.parser.tokenize(source=complete_source)
    self.__check_bad_sectioning(tokens=tokens)
    self.__parse_chapters(tokens=tokens, complete_source=complete_source, config=config)

  def to_html(self, config) -> str:
    """Generate a html stream of the whole presentation.

    Parameters
    ----------
    config : MatisseConfig
      MaTiSSe configuration
    """
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
      # doc.attr(title=self.metadata['title'].value)
      self.__put_html_tag_head(doc=doc, tag=tag, text=text, config=config)
      with tag('body', onload=f"resetCountdown({self.metadata['max_time'].value});"):
        doc.attr(klass='impress-not-supported')
        with tag('div', id='impress'):
          # numbering: [local_chap, local_sec, local_subsec, local_slide]
          current = [0, 0, 0, 0]
          for chapter in self.chapters:
            current[0] += 1
            current[1] = 0
            current[2] = 0
            current[3] = 0
            self.metadata['chaptertitle'].update_value(value=chapter.title)
            self.metadata['chapternumber'].update_value(value=chapter.number)
            for section in chapter.sections:
              current[1] += 1
              current[2] = 0
              current[3] = 0
              self.metadata['sectiontitle'].update_value(value=section.title)
              self.metadata['sectionnumber'].update_value(value=section.number)
              for subsection in section.subsections:
                current[2] += 1
                current[3] = 0
                self.metadata['subsectiontitle'].update_value(value=subsection.title)
                self.metadata['subsectionnumber'].update_value(value=subsection.number)
                for slide in subsection.slides:
                  current[3] += 1
                  self.metadata['slidetitle'].update_value(value=slide.title)
                  self.metadata['slidenumber'].update_value(value=slide.number)
                  with doc.tag('div'):
                    chapter.put_html_attributes(doc=doc)
                    section.put_html_attributes(doc=doc)
                    subsection.put_html_attributes(doc=doc)
                    slide.put_html_attributes(doc=doc)
                    self.__put_html_slide_decorators(tag=tag, doc=doc, decorator='header', current=current, overtheme=slide.overtheme)
                    # with doc.tag('div'):
                      # doc.attr(style='clear: both;')
                    self.__put_html_slide_decorators(tag=tag, doc=doc, decorator='sidebar', position='L', current=current, overtheme=slide.overtheme)
                    slide.to_html(doc=doc, parser=self.parser, metadata=self.metadata, theme=self.theme, current=current)
                    self.__put_html_slide_decorators(tag=tag, doc=doc, decorator='sidebar', position='R', current=current, overtheme=slide.overtheme)
                    # with doc.tag('div'):
                      # doc.attr(style='clear: both;')
                    self.__put_html_slide_decorators(tag=tag, doc=doc, decorator='footer', current=current, overtheme=slide.overtheme)
        self.__put_html_tags_scripts(doc=doc, tag=tag, config=config)
    # source = re.sub(r"<li>(?P<item>.*)</li>", r"<li><span>\g<item></span></li>", source)
    html = indent(doc.getvalue())
    return html

  def save(self, config, output):
    """Save the html form of presentation into external file.

    Parameters
    ----------
    config : MatisseConfig
      MaTiSSe configuration
    output : str
      output path
    """

    if not os.path.exists(output):
      os.makedirs(output)
    with open(os.path.join(output, 'index.html'), 'w') as html:
      html.write(self.to_html(config=config))
    # copy user defined directories if set
    if len(self.metadata['dirs_to_copy'].value) > 0:
      for data in self.metadata['dirs_to_copy'].value:
        copytree(data, os.path.join(output, data), dirs_exist_ok=True)
    # css files
    with open(os.path.join(output, 'css/theme.css'), 'w') as css_theme:
      css_theme.writelines(self.theme.css)
    for chapter in self.chapters:
      for section in chapter.sections:
        for subsection in section.subsections:
          for slide in subsection.slides:
            if slide.overtheme.custom:
              with open(os.path.join(output, f'css/slide-{slide.number}-overtheme.css'), 'w') as css_theme:
                css_theme.writelines(slide.overtheme.css)
