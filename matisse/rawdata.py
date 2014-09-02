#!/usr/bin/env python
"""
raw_data.py, module definition of Rawdata class.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
import copy
import re
# class definition
class Rawdata(object):
  """
  Object for handling raw data of presentation preamble.
  """
  def __init__(self,
               regex_start,  # regex of tag that starts the raw data string
               regex_end,    # regex of tag that ends the raw data string
               regex = None, # the complete regex enclosing the raw data string
               data = None): # data of the raw data: a list of type [[key,value]]
    self.regex_start = regex_start
    self.regex_end   = regex_end
    if regex:
      self.regex     = regex
    else:
      self.regex     = re.compile(r"(?P<rdata>"+regex_start+r".*?"+regex_end+")",re.DOTALL)
    self.data        = data
    return
  def __str__(self):
    string = []
    if self.data:
      string = ['  '+d[0]+' = '+d[1]+'\n' for d in self.data]
    return ''.join(string)
  def __deepcopy__(self):
    return Rawdata(regex_start = copy.deepcopy(self.regex_start),
                   regex_end   = copy.deepcopy(self.regex_end),
                   regex       = copy.deepcopy(self.regex),
                   data        = copy.deepcopy(self.data))
  def get(self,source):
    """
    Method for getting raw data from source.
    """
    matching = self.regex.search(source)
    if matching:
      raw = matching.group('rdata')
      # join eventually split data
      raw = re.sub(r'\&\& *\n','',raw)
      self.data = raw.split('\n')
      for i,data in enumerate(self.data):
        if re.search(self.regex_start,data) or re.search(self.regex_end,data):
          self.data.pop(i)
        if data == '':
          self.data.pop(i)
      for i,data in enumerate(self.data):
        self.data[i] = [data.split('=')[0].strip(),data.split('=')[1].strip()]
    return
  def strip(self,source):
    """
    Method for striping raw data from source.
    """
    return re.sub(self.regex,'',source)
