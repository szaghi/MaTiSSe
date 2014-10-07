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
from ..md_mathjax.mdx_mathjax import MathJaxExtension
#global variables
__regex_codeblock__ = re.compile(r"(?P<cblock>[`]{3}.*?[`]{3})",re.DOTALL)
__regex_codeinline__ = re.compile(r"(?P<cline>[`]{1}.*?[`]{1})",re.DOTALL)
__regex_overtheme__ = re.compile(r"(?P<ostheme>[-]{3}slide(?P<block>.*?)[-]{3}endslide)",re.DOTALL)
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
    self.regex_codeblock  =  __regex_codeblock__
    self.regex_codeinline =  __regex_codeinline__
    self.regex_overtheme  =  __regex_overtheme__
    self.mkd = markdown.Markdown(output_format='html5',extensions=['smarty',
                                                                   'extra',
                                                                   MathJaxExtension()])
    return

  def md_convert(self,source):
    """Method for converting markdown source to html.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      converted source
    """
    p_start = '<p>'
    p_end   = '</p>'
    markup = self.mkd.reset().convert(source)
    #if markup.startswith(p_start) and markup.endswith(p_end):
      #markup = markup[len(p_start):-len(p_end)]
    return markup

  @staticmethod
  def get(regex,source,group_name=None):
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
    """
    match = re.match(regex,source)
    if match:
      if group_name:
        return match.group(group_name)
      else:
        return match.group()
    return None

  def get_codeblocks(self,source):
    """Method for getting code blocks from a source string.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      (first) matching code blocks of source; if nothing matches None is returned
    """
    return self.get(regex=__regex_codeblock__,group_name='cblock',source=source)

  def get_codeinlines(self,source):
    """Method for getting code inlines from a source string.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      (first) matching code blocks of source; if nothing matches None is returned
    """
    return self.get(regex=__regex_codeinline__,group_name='cline',source=source)

  def get_overtheme(self,source):
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
    return self.get(regex=__regex_overtheme__,group_name='block',source=source)

  @staticmethod
  def purge(regex,source,group_name=None,strip=False):
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
    """
    purged_source = source
    for match in re.finditer(regex,purged_source):
      if strip:
        sub = ''
      else:
        if group_name:
          sub = ' '*len(match.group(group_name))
        else:
          sub = ' '*len(match.group())
      purged_source = re.sub(regex,sub,purged_source,1)
    return purged_source

  def purge_codeblocks(self,source):
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
    """
    return self.purge(regex=__regex_codeblock__,group_name='cblock',source=source)

  def purge_codeinlines(self,source):
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
    """
    return self.purge(regex=__regex_codeinline__,group_name='cline',source=source)

  def purge_codes(self,source):
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
    """
    source = self.purge_codeinlines(source=source)
    return self.purge_codeblocks(source=source)

  def purge_overtheme(self,source):
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
    """
    return self.purge(regex=__regex_overtheme__,group_name='ostheme',source=source)

  def strip(self,regex,source,group_name=None):
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
    """
    return self.purge(regex=regex,source=source,group_name=group_name,strip=True)

  def strip_overtheme(self,source):
    """Method for striping out overriding slide theme blocks from a source string.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      stripped string
    """
    return self.strip(regex=__regex_overtheme__,source=source)

  @staticmethod
  def includes(source):
    """Method for including other sources into source.

    It parse souce for matching "include" regular expressions and for each include found
    the external sources is included "in place" into source. It is not recursive!

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      source with included other sources
    """
    inc_source = source
    for match in re.finditer(__regex_include__,inc_source):
      include_file = match.group('include')
      if not os.path.exists(include_file):
        sys.stderr.write('Error: cannot include "'+include_file+'"')
        sys.exit(1)
      else:
        with open(include_file,'r') as inc:
          other_source = inc.read()
        inc_source = re.sub(__regex_include__,other_source,inc_source,1)
    return inc_source

def obfuscate_protected(source,re_protected):
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
  """
  obfuscate_source = source
  protected_contents = []
  for match in re.finditer(re_protected,source):
    protected_contents.append([match.start(),match.end(),match.group()])
    obfuscate_source = re.sub(re_protected,'$PROTECTED-'+str(len(protected_contents)),obfuscate_source,1)
  return protected_contents,obfuscate_source

def obfuscate_codeblocks(source):
  """Method for obfuscating codes contents.

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
  """
  obfuscate_source = source
  protected_contents = []
  for match in re.finditer(__regex_codeblock__,source):
    protected_contents.append([match.start(),match.end(),match.group()])
    obfuscate_source = re.sub(__regex_codeblock__,'$PROTECTED-'+str(len(protected_contents)),obfuscate_source,1)
  return protected_contents,obfuscate_source

def illuminate_protected(source,protected_contents):
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
  """
  if len(protected_contents)>0:
    illuminate_source = source
    for match in re.finditer(__regex_protected__,illuminate_source):
      illuminate_source = re.sub(__regex_protected__,protected_contents[int(match.group('num'))-1][2],illuminate_source,1)
    return illuminate_source
  else:
    return source

# global variables
__initialized__ = False
if not __initialized__:
  __source_editor__ = SourceEditor()
  __initialized__ = True
