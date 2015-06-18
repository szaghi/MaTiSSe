#!/usr/bin/env python
"""
source_editor.py, module definition of SourceEditor class.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import os
import re
import sys
# modules not in the standard library
import markdown
from .mdx_mathjax import MathJaxExtension
try:
  from markdown_checklist.extension import ChecklistExtension
  __mdx_checklist__ = True
except ImportError:
  __mdx_checklist__ = False
# global variables
__regex_codeblock__ = re.compile(r"(?P<cblock>[`]{3}.*?[`]{3})", re.DOTALL)
__regex_codeblock_html__ = re.compile(r"(?P<cblock>\<code.*?\<\/code\>)", re.DOTALL)
__regex_codeinline__ = re.compile(r"(?P<cline>[`]{1}.*?[`]{1})", re.DOTALL)
__regex_overtheme__ = re.compile(r"(?P<ostheme>[-]{3}slide(?P<block>.*?)[-]{3}endslide)", re.DOTALL)
__regex_include__ = re.compile(r"\$include\((?P<include>.*?)\)")
__regex_protected__ = re.compile(r"(\$PROTECTED-(?P<num>[0-9]*))")


# class definition
class SourceEditor(object):
  """
  Object for editing source stream:

  - get from source necessary data;
  - purge from source uncessary data;
  - strip out from source uncessary data.
  """
  def __init__(self):
    """
    Attributes
    ----------
    regex_codeblock : re.compile object
    regex_codeinline : re.compile object
    regex_overtheme : re.compile object
    mkd : markdown.Markdown object
      markdown converter
    """
    self.regex_codeblock = __regex_codeblock__
    self.regex_codeinline = __regex_codeinline__
    self.regex_overtheme = __regex_overtheme__
    if __mdx_checklist__:
      self.mkd = markdown.Markdown(output_format='html5',
                                   extensions=['smarty',
                                               'extra',
                                               ChecklistExtension(),
                                               MathJaxExtension()])
    else:
      self.mkd = markdown.Markdown(output_format='html5',
                                   extensions=['smarty',
                                               'extra',
                                               MathJaxExtension()])
    return

  def md_convert(self, source, no_p=False):
    """Convert markdown source to html.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source
    no_p : bool, optional
      if True the converted contents is not inserted into the <p></p> tags

    Returns
    -------
    str
      converted source
    """
    markup = self.mkd.reset().convert(source)
    if no_p:
      p_start = '<p>'
      p_end = '</p>'
      if markup.startswith(p_start) and markup.endswith(p_end):
        markup = markup[len(p_start):-len(p_end)]
    return markup

  @staticmethod
  def get(regex, source, group_name=None):
    """Method for getting blocks of characters matching 'regex' from a source string.

    Parameters
    ----------
    regex : re.compile object
      regular expression to match
    source : str
      string (as single stream) containing the source
    group_name : str, optional
      name of the group to get; if no name is passed the whole 'regex' is gotten

    Returns
    -------
    str
      (first) matching block of source; if nothing matches None is returned; if group
      name is not passed the whole match is returned

    >>> seditor = SourceEditor()
    >>> source = '---test contents ---endtest other contents'
    >>> regex = re.compile(r"(?P<test>[-]{3}test.*?[-]{3}endtest)",re.DOTALL)
    >>> seditor.get(regex,source,'test')
    '---test contents ---endtest'
    >>> seditor.get(regex,source,'testNone')
    '---test contents ---endtest'
    >>> regex = re.compile(r"(?P<test>[-]{3}wrongtest.*?[-]{3}endwrongtest)",re.DOTALL)
    >>> seditor.get(regex,source,'test')
    """
    match = re.match(regex, source)
    if match:
      if group_name and group_name in match.groupdict():
        return match.group(group_name)
      else:
        return match.group()
    return None

  def get_codeblocks(self, source):
    """Method for getting code blocks from a source string.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      (first) matching code blocks of source; if nothing matches None is returned

    >>> seditor = SourceEditor()
    >>> source = '``` my code block ``` other contents'
    >>> seditor.get_codeblocks(source)
    '``` my code block ```'
    """
    return self.get(regex=__regex_codeblock__, group_name='cblock', source=source)

  def get_codeinlines(self, source):
    """Method for getting code inlines from a source string.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      (first) matching code blocks of source; if nothing matches None is returned

    >>> seditor = SourceEditor()
    >>> source = '` my code inline ` other contents'
    >>> seditor.get_codeinlines(source)
    '` my code inline `'
    """
    return self.get(regex=__regex_codeinline__, group_name='cline', source=source)

  def get_overtheme(self, source):
    """Method for getting blocks of characters defining the overriding slide theme from a source string.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      (first) matching overriding theme block of source; if nothing matches None is returned
    """
    return self.get(regex=__regex_overtheme__, group_name='block', source=source)

  @staticmethod
  def purge(regex, source, group_name=None, strip=False):
    """Method for removing blocks of characters matching 'regex' from a source string
    and replacing with an equivalent number of spaces as the removed characters.

    Parameters
    ----------
    regex : re.compile object
      regular expression to match
    source : str
      string (as single stream) containing the source
    group_name : str, optional
      name of the group to purge; if no name is passed the whole 'regex' is purged
    strip : bool, optional
      if true the matching characters is simply stripped out and replacing with an equivalent
      number of spaces

    Returns
    -------
    str
      purged string

    >>> seditor = SourceEditor()
    >>> source = '---test contents ---endtest other contents'
    >>> regex = re.compile(r"(?P<test>[-]{3}test.*?[-]{3}endtest)",re.DOTALL)
    >>> seditor.purge(regex,source,'test')
    '                            other contents'
    """
    purged_source = source
    for match in re.finditer(regex, purged_source):
      if strip:
        sub = ''
      else:
        if group_name:
          sub = ' ' * len(match.group(group_name))
        else:
          sub = ' ' * len(match.group())
      purged_source = re.sub(regex, lambda x: sub, purged_source, 1)
    return purged_source

  def purge_codeblocks(self, source):
    """Method for removing code blocks from a source string and
    replacing with an equivalent number of spaces as the removed characters.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      purged string

    >>> seditor = SourceEditor()
    >>> source = '``` my code block ``` other contents'
    >>> seditor.purge_codeblocks(source)
    '                      other contents'
    """
    return self.purge(regex=__regex_codeblock__, group_name='cblock', source=source)

  def purge_codeinlines(self, source):
    """Method for removing code inlines from a source string and
    replacing with an equivalent number of spaces as the removed characters.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      purged string

    >>> seditor = SourceEditor()
    >>> source = '` my code inline ` other contents'
    >>> seditor.purge_codeinlines(source)
    '                   other contents'
    """
    return self.purge(regex=__regex_codeinline__, group_name='cline', source=source)

  def purge_codes(self, source):
    """Method for removing code (blocks and inline) from a source string and
    replacing with an equivalent number of spaces as the removed characters.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      purged string

    >>> seditor = SourceEditor()
    >>> source = '``` my code block ``` contents ` my code inline ` other contents'
    >>> seditor.purge_codes(source)
    '                      contents                    other contents'
    """
    source = self.purge_codeinlines(source=source)
    return self.purge_codeblocks(source=source)

  def purge_overtheme(self, source):
    """Method for removing overriding slide themes blocks from a source string and
    replacing with an equivalent number of spaces as the removed characters.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      purged string

    >>> seditor = SourceEditor()
    >>> source = '---slide contents ---endslide other contents'
    >>> seditor.purge_overtheme(source)
    '                              other contents'
    """
    return self.purge(regex=__regex_overtheme__, group_name='ostheme', source=source)

  def strip(self, regex, source, group_name=None):
    """Method for striping out blocks of characters matching 'regex' from a source string.

    Parameters
    ----------
    regex : re.compile object
      regular expression to match
    source : str
      string (as single stream) containing the source
    group_name : str, optional
      name of the group to strip; if no name is passed the whole 'regex' is stripped

    Returns
    -------
    str
      stripped string

    >>> seditor = SourceEditor()
    >>> source = '---test contents ---endtest other contents'
    >>> regex = re.compile(r"(?P<test>[-]{3}test.*?[-]{3}endtest)",re.DOTALL)
    >>> seditor.strip(regex,source,'test')
    ' other contents'
    """
    return self.purge(regex=regex, source=source, group_name=group_name, strip=True)

  def strip_overtheme(self, source):
    """Method for striping out overriding slide theme blocks from a source string.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      stripped string

    >>> seditor = SourceEditor()
    >>> source = '---slide contents ---endslide other contents'
    >>> seditor.strip_overtheme(source)
    ' other contents'
    """
    protected, obfuscate_source = obfuscate_codeblocks(source=source)
    obfuscate_source = self.strip(regex=__regex_overtheme__, source=obfuscate_source)
    return illuminate_protected(source=obfuscate_source, protected_contents=protected)

  @staticmethod
  def includes(source):
    """Include other sources into source.

    It parse source for matching "include" regular expressions and for each include found
    the external sources is included "in place" into source. It is recursive!

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      source with included other sources
    """
    protected, obfuscate_source = obfuscate_codeblocks(source=source)
    if __regex_include__.search(obfuscate_source):
      for match in re.finditer(__regex_include__, obfuscate_source):
        include_file = match.group('include')
        if not os.path.exists(include_file):
          sys.stderr.write('Error: cannot include "' + include_file + '"')
          sys.exit(1)
        else:
          with open(include_file, 'r') as inc:
            other_source = repr(inc.read())
          obfuscate_source = re.sub(__regex_include__, lambda x: other_source, obfuscate_source, 1)
      return SourceEditor.includes(source=illuminate_protected(source=obfuscate_source, protected_contents=protected))
    return illuminate_protected(source=obfuscate_source, protected_contents=protected)


def obfuscate_protected(source, re_protected):
  """Method for obfuscating protected contents.

  It can be often useful to temporarly obfuscate some blocks of contents for performing safely some tasks
  and then re-introducing them.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source
  re_protected : re.compile object
    regular expression of protected block

  Returns
  -------
  protected_contents : list
    list of str containing the contents of protected blocks
  str
    source with protected contents obfuscated and replaced by a safe placeholder

  >>> source = '``` my code block ``` other contents'
  >>> prot, ob_source = obfuscate_protected(source,__regex_codeblock__)
  >>> prot[0][2]
  '``` my code block ```'
  >>> ob_source
  '$PROTECTED-1 other contents'
  """
  obfuscate_source = source
  protected_contents = []
  for match in re.finditer(re_protected, source):
    protected_contents.append([match.start(), match.end(), match.group()])
    obfuscate_source = re.sub(re_protected, lambda x: '$PROTECTED-' + str(len(protected_contents)), obfuscate_source, 1)
  return protected_contents, obfuscate_source


def obfuscate_codeblocks(source):
  """Method for obfuscating codeblocks contents.

  It can be often useful to temporarly obfuscate codeblocks contents for performing safely some tasks
  and then re-introducing them.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source

  Returns
  -------
  protected_contents : list
    list of str containing the contents of codeblocks
  str
    source with codeblocks contents obfuscated and replaced by a safe placeholder

  >>> source = '``` my code block ``` other contents'
  >>> prot, ob_source = obfuscate_codeblocks(source)
  >>> prot[0][2]
  '``` my code block ```'
  >>> ob_source
  '$PROTECTED-1 other contents'
  """
  obfuscate_source = source
  protected_contents = []
  for match in re.finditer(__regex_codeblock__, obfuscate_source):
    protected_contents.append([match.start(), match.end(), match.group()])
    obfuscate_source = re.sub(__regex_codeblock__, lambda x: '$PROTECTED-' + str(len(protected_contents)), obfuscate_source, 1)
  for match in re.finditer(__regex_codeblock_html__, obfuscate_source):
    protected_contents.append([match.start(), match.end(), match.group()])
    obfuscate_source = re.sub(__regex_codeblock_html__, lambda x: '$PROTECTED-' + str(len(protected_contents)), obfuscate_source, 1)
  return protected_contents, obfuscate_source


def obfuscate_codes(source):
  """Method for obfuscating codes contents.

  It can be often useful to temporarly obfuscate codes contents for performing safely some tasks
  and then re-introducing them.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source

  Returns
  -------
  protected_contents : list
    list of str containing the contents of codes
  str
    source with codes contents obfuscated and replaced by a safe placeholder

  >>> source = '``` my code block ``` contents ` code inline ` other contents'
  >>> prot, ob_source = obfuscate_codes(source)
  >>> prot[0][2]
  '``` my code block ```'
  >>> prot[1][2]
  '` code inline `'
  >>> ob_source
  '$PROTECTED-1 contents $PROTECTED-2 other contents'
  """
  obfuscate_source = source
  protected_contents = []
  for match in re.finditer(__regex_codeblock__, obfuscate_source):
    protected_contents.append([match.start(), match.end(), match.group()])
    obfuscate_source = re.sub(__regex_codeblock__, lambda x: '$PROTECTED-' + str(len(protected_contents)), obfuscate_source, 1)
  for match in re.finditer(__regex_codeblock_html__, obfuscate_source):
    protected_contents.append([match.start(), match.end(), match.group()])
    obfuscate_source = re.sub(__regex_codeblock_html__, lambda x: '$PROTECTED-' + str(len(protected_contents)), obfuscate_source, 1)
  for match in re.finditer(__regex_codeinline__, obfuscate_source):
    protected_contents.append([match.start(), match.end(), match.group()])
    obfuscate_source = re.sub(__regex_codeinline__, lambda x: '$PROTECTED-' + str(len(protected_contents)), obfuscate_source, 1)
  return protected_contents, obfuscate_source


def illuminate_protected(source, protected_contents):
  """Method for re-insterting protected contents (illuminating previously obfuscated blocks).

  It can be often useful to temporarly obfuscate some blocks of contents for performing safely some tasks
  and then re-introducing (illuminating) them.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source
  protected_contents : list
    list of str containing the contents of protected blocks

  Returns
  -------
  str
    source with protected contents illuminated (reintroduced)

  >>> source = '``` my code block ``` contents ` code inline ` other contents'
  >>> prot, ob_source = obfuscate_codes(source)
  >>> illuminate_protected(ob_source,prot)
  '``` my code block ``` contents ` code inline ` other contents'
  """
  if len(protected_contents) > 0:
    illuminate_source = source
    for match in re.finditer(__regex_protected__, illuminate_source):
      illuminate_source = re.sub(__regex_protected__, lambda x: protected_contents[int(match.group('num')) - 1][2], illuminate_source, 1)
    return illuminate_source
  else:
    return source


def tokenize(source, re_part, name_part):
  """Method for tokenizing source tagging parts of the source.

  Parameters
  ----------
  source : str
    string (as single stream) containing the source
  re_part : re.compile object
    regex matching parts to be tokenized
  name_part : str
    name of parts matched

  Returns
  -------
  list
    list of tokens whose elements are ['name',source_part]; name is name_part for parts matching re_part and
    'unknown' for anything else

  >>> source = '---test contents ---endtest other contents'
  >>> regex = re.compile(r"(?P<test>[-]{3}test.*?[-]{3}endtest)",re.DOTALL)
  >>> tokenize(source,regex,'TEST')[0][1]
  '---test contents ---endtest'
  """
  protected, obfuscate_source = obfuscate_codeblocks(source=source)
  matches = []
  for match in re.finditer(re_part, obfuscate_source):
    matches.append([match.start(), match.end(), illuminate_protected(source=match.group(), protected_contents=protected)])
  if len(matches) > 0:
    tokens = []
    for mtc, match in enumerate(matches):
      if mtc == 0:
        start = 0
      else:
        start = matches[mtc - 1][1] + 1
      if match[0] != start:
        tokens.append(['unknown', illuminate_protected(source=obfuscate_source[start:match[0]], protected_contents=protected)])
      tokens.append([name_part, match[2]])
    if matches[-1][1] < len(obfuscate_source):
      tokens.append(['unknown', illuminate_protected(source=obfuscate_source[matches[-1][1] + 1:], protected_contents=protected)])
  else:
    tokens = [['unknown', source]]
  return tokens

# global variables
__initialized__ = False
if not __initialized__:
  __source_editor__ = SourceEditor()
  __initialized__ = True
