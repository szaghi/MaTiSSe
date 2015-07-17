#!/usr/bin/env python
"""
slide.py, module definition of Parser class.
This defines the MaTiSSe.py Parser.
"""
from __future__ import print_function
import os
import re
import sys


class Parser(object):
  """
  Parser of MaTiSSe.py sources.
  """
  regexs = {"all": re.compile(r"(.*(?P<expr>))", re.DOTALL)}

  def __init__(self):
    """
    Parameters
    ----------

    Attributes
    ----------
    regexs: dict
      dictionary filled with compiled objects of MaTiSSe.py regexs
    """
    self.regexs = {"chapter": re.compile(r"([^#]#|^#)\s+" + r"(?P<expr>.*)"),
                   "section": re.compile(r"([^#]##|^##)\s+" + r"(?P<expr>.*)"),
                   "subsection": re.compile(r"([^#]###|^###)\s+" + r"(?P<expr>.*)"),
                   "slide": re.compile(r"([^#]####|^####)\s+" + r"(?P<expr>.*)"),
                   "codeblock": re.compile(r"(?P<block>[`]{3}.*?[`]{3})", re.DOTALL),
                   "code": re.compile(r"(?P<block>`.*?`)"),
                   "yamlblock": re.compile(r"(?P<block>[-]{3}.*?[-]{3})", re.DOTALL),
                   "includeblock": re.compile(r"\$include\((?P<include>.*?)\)")}
    return

  @staticmethod
  def tokenizer(source, re_search, exclude=None, force_all=False):
    """Tokenize accordingly to re_search (and exlude if passed).

    Parameters
    ----------
    source: str
      input stream
    re_search: compiled regex
    exclude: list
      list of start/end index of source lines

    Returns
    -------
    tokens: list
      list of token
    """
    def __tokenizer(source, re_search, exclude=None):
      tokens = []
      for match in re.finditer(re_search, source):
        safe = True
        if exclude is not None:
          for exc in exclude:
            if match.start() >= exc['start'] and match.end() <= exc['end']:
              safe = False
        if safe:
          tokens.append({'match': match, 'start': match.start(), 'end': match.end()})
      return tokens

    tokens = __tokenizer(source=source, re_search=re_search, exclude=exclude)
    if len(tokens) == 0 and force_all:
      tokens = __tokenizer(source=source, re_search=Parser.regexs['all'], exclude=exclude)
      return tokens[:-1]
    return tokens

  @staticmethod
  def tokens_end_update(tokens, end=None):
    """Update the end of tokens accordinly to the start of the next one into the tokens list.

    Paramaters
    ----------
    tokens: list

    Returns
    -------
    tokens: list
    """
    if len(tokens) > 0:
      for k, tok in enumerate(tokens[:-1]):
        tok['end_next'] = tokens[k + 1]['start']
      if end is not None:
        tokens[-1]['end_next'] = end
    return tokens

  @staticmethod
  def slides_end_update(slides, others):
    """Update the end of slides accordinly to the start of others sectionings.

    Paramaters
    ----------
    slides: list
    others: list

    Returns
    -------
    slides: list
    """
    for slide in slides:
      for other in others:
        if slide['start'] < other['start'] and slide['end_next'] >= other['start']:
          slide['end_next'] = other['start']
    return slides

  def includes(self, source):
    """
    Recursive inclusion of other sources.

    Parameters
    ----------
    source: str
      input stream

    Returns
    -------
    str:
      included sources stream
    """
    codeblocks = self.tokenizer(source=source, re_search=self.regexs['codeblock'])
    includeblocks = self.tokenizer(source=source, re_search=self.regexs['includeblock'], exclude=codeblocks)
    if len(includeblocks) > 0:
      complete_source = source[:includeblocks[0]['start']]
      for block, includeblock in enumerate(includeblocks[:-1]):
        include_file = includeblock['match'].group('include')
        if not os.path.exists(include_file):
          sys.stderr.write('Error: cannot include "' + include_file + '"')
          sys.exit(1)
        else:
          with open(include_file, 'r') as inc:
            other_source = inc.read()
          complete_source += other_source + source[includeblock['end']:includeblocks[block + 1]['start']]
      include_file = includeblocks[-1]['match'].group('include')
      if not os.path.exists(include_file):
        sys.stderr.write('Error: cannot include "' + include_file + '"')
        sys.exit(1)
      else:
        with open(include_file, 'r') as inc:
          other_source = inc.read()
      complete_source += other_source + source[includeblocks[-1]['end']:]
      source = complete_source
      source = self.includes(source=source)
    return source

  def tokenize(self, source):
    """Tokenize input source returning tagged tokens.

    Parameters
    ----------
    source: str
      input stream

    Returns
    -------
    tokens: dict
      dictionary of tokens; each element is a list of type [token, start_char, end_char]
    """
    codeblocks = self.tokenizer(source=source, re_search=self.regexs['codeblock'])
    yamlblocks = self.tokenizer(source=source, re_search=self.regexs['yamlblock'], exclude=codeblocks)
    chapters = self.tokenizer(source=source, re_search=self.regexs['chapter'], exclude=codeblocks + yamlblocks, force_all=True)
    chapters = self.tokens_end_update(tokens=chapters, end=len(source))
    sections = self.tokenizer(source=source, re_search=self.regexs['section'], exclude=codeblocks + yamlblocks, force_all=True)
    sections = self.tokens_end_update(tokens=sections, end=len(source))
    subsections = self.tokenizer(source=source, re_search=self.regexs['subsection'], exclude=codeblocks + yamlblocks, force_all=True)
    subsections = self.tokens_end_update(tokens=subsections, end=len(source))
    slides = self.tokenizer(source=source, re_search=self.regexs['slide'], exclude=codeblocks + yamlblocks)
    slides = self.tokens_end_update(tokens=slides, end=len(source))
    slides = self.slides_end_update(slides=slides, others=chapters)
    slides = self.slides_end_update(slides=slides, others=sections)
    slides = self.slides_end_update(slides=slides, others=subsections)
    tokens = {'codeblocks': codeblocks,
              'yamlblocks': yamlblocks,
              'chapters': chapters,
              'sections': sections,
              'subsections': subsections,
              'slides': slides}
    return tokens
