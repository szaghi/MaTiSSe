#!/usr/bin/env python
"""
matisse_metadata.py, module definition of Metadata class.
"""
# modules loading
# standard library modules: these should be present in any recent python distribution
from collections import OrderedDict
import copy
# MaTiSSe.py modules
from .rawdata import Rawdata
# class definition
class Metadata(object):
  """
  Object for handling presentation metadata.
  """
  def __init__(self,
               rawdata = None,  # raw data
               data    = None): # data: is a dictionaris a dictionaryy
    if rawdata:
      self.raw_data = rawdata
    else:
      self.raw_data = Rawdata(regex_start='[-]{3}metadata',regex_end='[-]{3}endmetadata')
    if data:
      self.data = data
    else:
      self.data = OrderedDict()
      self.data['title'              ] = ''
      self.data['subtitle'           ] = ''
      self.data['authors'            ] = []
      self.data['authors_short'      ] = []
      self.data['emails'             ] = []
      self.data['affiliations'       ] = []
      self.data['affiliations_short' ] = []
      self.data['logo'               ] = ''
      self.data['location'           ] = ''
      self.data['location_short'     ] = ''
      self.data['date'               ] = ''
      self.data['conference'         ] = ''
      self.data['conference_short'   ] = ''
      self.data['session'            ] = ''
      self.data['session_short'      ] = ''
      self.data['max_time'           ] = 25
      self.data['total_slides_number'] = ''
      self.data['dirs_to_copy'       ] = []
      self.data['toc'                ] = ''
    return
  def __str__(self):
    string = []
    if self.data:
      string = [ '  '+k+' = '+str(v)+'\n' for k,v in self.data.items()]
    return 'Metadata\n'+''.join(string)
  def __deepcopy__(self):
    return Metadata(rawdata = copy.deepcopy(self.raw_data),
                    data    = copy.deepcopy(self.data))
  def get_raw_data(self,source):
    """
    Method for getting raw data from source.
    """
    self.raw_data.get(source)
    return
  def get_values(self):
    """
    Method for getting values from raw data parsed from source.
    """
    for data in self.raw_data.data:
      key = data[0].strip()
      val = data[1].strip()
      if key in self.data:
        if isinstance(self.data[key], str):
          self.data[key] = val
        elif isinstance(self.data[key], list) or isinstance(self.data[key], bool):
          self.data[key] = eval(val)
        else:
          self.data[key] = val
    return
  def set_value(self,key,value):
    """
    Method for setting metadata value.
    """
    if key in self.data:
      self.data[key] = value
    return
  def strip(self,source):
    """
    Method for striping raw metadata from source.
    """
    return self.raw_data.strip(source)
