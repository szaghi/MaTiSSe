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
from ..utils.source_editor import SourceEditor
# global variables
__source_editor__ = SourceEditor()
# class definition
class Data(object):
  """Object for handling data of presentation.

  The "data" dictionary is an ordered dictionary where the entries are divided into 2
  types:

  1. standard entries which can be safely converted to css format;
  2. special entries whose key must inserted into the "special_keys" list and that are
     not converted to css format.
  """
  def __init__(self, regex_start = '', regex_end = '', skip = None, special_keys = None):
    """
    Parameters
    ----------
    regex_start : str, optional
      regural expression starting the matching block of data
    regex_end : str, optional
      regural expression ending the matching block of data
    skip : re.compile, optional
      compiled regular expression of block to be skipped
    special_keys : list, optional
      list of strings containing the special keys of data entries

    Attributes
    regex_start : str
      regural expression starting the matching block of data
    regex_end : str
      regural expression ending the matching block of data
    skip : re.compile
      compiled regular expression of block to be skipped
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
    self.regex        = re.compile(r"(?P<rdata>"+regex_start+r".*?"+regex_end+")",re.DOTALL)
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

  def get(self,source):
    """
    Method for getting data from source.
    """
    if self.skip:
      source = __source_editor__.purge(regex=self.skip,source=source)
    matching = self.regex.search(source)
    if matching:
      raw = matching.group('rdata')
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
    """Method for getting the available data options."""
    string = []
    for key,val in self.data.items():
      string.append('\n'+key+' = '+str(val[0]))
    return ''.join(string)

  def get_css(self,only_custom=False):
    """
    Method for getting css from data.
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
    """
    Method returning only the data that have been set by users (customized) overriding default values.
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
    """
    Method merging otherdata with self. Only data that are not customized is updated with the otherdata data
    if they have been customized.
    """
    for key,val in self.data.items():
      if not val[1]:
        if key in otherdata.data and otherdata.data[key][1]:
          self.data[key] = otherdata.data[key]
    return

  def strip(self,source):
    """
    Method for striping raw data from source.
    """
    strip_source = source
    if self.skip:
      regex = re.compile(r"(?!"+str(self.skip.pattern)+")",re.DOTALL)
      for match in re.finditer(regex,strip_source):
        sub = ' '*len(match.group())
        strip_source = re.sub(regex,sub,strip_source,1)
    else:
      strip_source = re.sub(self.regex,'',source)
    return strip_source
