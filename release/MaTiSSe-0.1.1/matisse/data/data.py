#!/usr/bin/env python
"""
data.py, module definition of Data class.
This is the generic database holding presentation settings, options, etc...
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import copy
import re
# MaTiSSe.py modules
from ..utils.source_editor import __source_editor__
# class definition
class Data(object):
  """Object for handling data of presentation.

  The "data" dictionary is an ordered dictionary where the entries are divided into 2
  types:

  1. standard entries which can be safely converted to css format;
  2. special entries whose key must be inserted into the "special_keys" list and that
     handeld differently from standard data.

  Into the source the data must be defined with the following syntax:
  regex_start
  option_name1 = option_value1
  option_name1 = option_value1
  ...
  regex_end
  """
  def __init__(self, regex_start = '', regex_end = '', skip = None, special_keys = None):
    """
    Parameters
    ----------
    regex_start : str, optional
      regural expression starting the matching block of data
    regex_end : str, optional
      regural expression ending the matching block of data
    skip : list, optional
      list of re.compile (compiled regular expression) of block to be skipped
    special_keys : list, optional
      list of strings containing the special keys of data entries

    Attributes
    regex_start : str
      regural expression starting the matching block of data
    regex_end : str
      regural expression ending the matching block of data
    skip : list
      list of compiled regular expression of block to be skipped
    special_keys : list
      list of strings containing the special keys of data entries
    regex : re.compile
      compiler regular expression of the matching block
    data : OrderedDict object
      dictionary of data entries; constitute the main database of presentation elements
      options
    ----------
    """
    self.regex_start  = regex_start
    self.regex_end    = regex_end
    self.skip         = skip
    self.special_keys = special_keys
    self.regex        = re.compile(r"(?P<rdata>"+regex_start+r"(?P<opts>.*?)"+regex_end+")",re.DOTALL)
    self.data         = OrderedDict()

  def __str__(self):
    string = []
    if self.data:
      string = ['  '+str(k)+' : '+str(v)+'\n' for k,v in self.data.items()]
    return ''.join(string)

  def __copy__(self):
    newone = type(self)()
    newone.__dict__.update(self.__dict__)
    return newone

  def __deepcopy__(self,memo):
    newone = type(self).__new__(type(self))
    newone.__dict__.update(self.__dict__)
    newone.special_keys = copy.deepcopy(self.special_keys, memo)
    newone.data = copy.deepcopy(self.data, memo)
    return newone

  def count(self,source):
    """Method for computing the number of data definitions present into the source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    int
      number of data definitions

    >>> mydata = Data('---mydata','---endmydata')
    >>> source = '---mydata option1 = val1---endmydata---mydata option2 = val2---endmydata'
    >>> mydata.count(source)
    2
    """
    if self.skip:
      for skip in self.skip:
        source = __source_editor__.purge(regex=skip,source=source)
    number = len(re.findall(self.regex,source))
    return number

  def set_all_custom(self):
    """Method for setting all data as customized by user (useful for plain slides theme)."""
    for data in self.data:
      self.data[data][1] = True
    return

  def get(self,source):
    """Method for getting data from source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    >>> mydata = Data('---mydata','---endmydata')
    >>> source = '---mydata option1 = val1 ---endmydata'
    >>> mydata.get(source)
    >>> mydata.data['option1'][0]
    'val1'
    """
    if self.skip:
      for skip in self.skip:
        source = __source_editor__.purge(regex=skip,source=source)
    matching = self.regex.search(source)
    if matching:
      #raw = matching.group('rdata')
      raw = matching.group('opts')
      raw = re.sub(r'\&\& *\n','',raw)
      raw = raw.split('\n')
      for i,rdata in enumerate(raw):
        if re.search(self.regex_start,rdata) or re.search(self.regex_end,rdata) or rdata == '':
          raw.pop(i)
        elif not re.search('=',rdata):
          raw.pop(i)
      for i,rdata in enumerate(raw):
        key = rdata.split('=')[0].strip()
        val = rdata.split('=')[1].strip()
        self.data[key] = [val,True]
    return

  def get_options(self):
    """Method for getting the available data options.

    Returns
    -------
    str
      string with option_names = values pairs (without True/False custom tag)

    >>> mydata = Data('---mydata','---endmydata')
    >>> source = '---mydata option1 = val1 ---endmydata'
    >>> mydata.get(source)
    >>> mydata.get_options()
    '\\noption1 = val1'
    """
    string = []
    for key,val in self.data.items():
      string.append('\n'+key+' = '+str(val[0]))
    return ''.join(string)

  def get_css(self,only_custom=False):
    """Method for getting css from data.

    Parameters
    ----------
    only_custom : bool, optional
      consider only (user) customized data

    Returns
    -------
    str
      sting containing the css style options based on the data options

    >>> mydata = Data('---mydata','---endmydata')
    >>> source = '---mydata option1 = val1 ---endmydata'
    >>> mydata.get(source)
    >>> mydata.get_css()
    '\\n  option1: val1;'
    """
    css = ''
    for key,val in self.data.items():
      special = False
      if self.special_keys and key in self.special_keys:
        special = True
      if not special:
        if only_custom:
          if val[1]:
            css += '\n  '+key+': '+val[0]+';'
        else:
          css += '\n  '+key+': '+val[0]+';'
    return css

  def get_custom(self,chk_specials=False):
    """Method returning only the data that have been set by users (customized) overriding default values.

    Parameters
    ----------
    chk_specials : bool, optional
      if activated handle special entries differently from standard ones

    Returns
    -------
    list
      list of only customized options

    >>> mydata = Data('---mydata','---endmydata')
    >>> source = '---mydata option1 = val1 ---endmydata'
    >>> mydata.get(source)
    >>> str(mydata.get_custom())
    "  option1 : ['val1', True]\\n"
    """
    custom = copy.deepcopy(self)
    for key,val in custom.data.items():
      special = False
      if self.special_keys and key in self.special_keys:
        special = True
      if chk_specials and special:
        continue
      else:
        if not val[1]:
          custom.data.pop(key,None)
    return custom

  def merge(self,otherdata):
    """Method merging otherdata with self. Only data that are not customized is updated with the otherdata data
    if they have been customized.

    Parameters
    ----------
    otherdata : Data object
      other data to be merged with self

    >>> mydata = Data('---mydata','---endmydata')
    >>> source = '---mydata option1 = val1 ---endmydata'
    >>> mydata.get(source)
    >>> mydata.data['option2'] = ['unset',False]
    >>> otherdata = Data('---mydata','---endmydata')
    >>> source = '---mydata option2 = val2 ---endmydata'
    >>> otherdata.get(source)
    >>> mydata.merge(otherdata)
    >>> mydata.data['option2'][0]
    'val2'
    """
    for key,val in self.data.items():
      if not val[1]:
        if key in otherdata.data and otherdata.data[key][1]:
          self.data[key] = otherdata.data[key]
    return

  def strip(self,source):
    """Method for striping raw data from source.

    Parameters
    ----------
    source : str
      string (as single stream) containing the source

    Returns
    -------
    str
      source without the raw data

    >>> mydata = Data('---mydata','---endmydata')
    >>> source = 'other contents before---mydata option1 = val1 ---endmydata,other contents after'
    >>> mydata.strip(source)
    'other contents before,other contents after'
    """
    if self.skip:
      strip_source = source
      pattern = '|'.join([ skip.pattern for skip in self.skip ])
      regex = re.compile(pattern+r"|(?P<strip>"+self.regex.pattern+r")",re.DOTALL)
      matches = []
      for match in re.finditer(regex,strip_source):
        if match.group('strip'):
          matches.append([match.start(),match.end()])
      if len(matches)>0:
        strip = ''
        for mtc,match in enumerate(matches):
          if mtc == 0:
            start = 0
          else:
            start = matches[mtc-1][1]+1
          if match[0]!=start:
            strip += strip_source[start:match[0]]
        if matches[-1][1]<len(strip_source)+1:
          strip += strip_source[matches[-1][1]:]
        strip_source = strip
    else:
      strip_source = re.sub(self.regex,'',source)
    return strip_source.strip()
