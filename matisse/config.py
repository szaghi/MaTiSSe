#!/usr/bin/env python
"""
config.py, module definition of MaTiSSe.py configuration.
"""
# class definition
class MaTiSSeConfig(object):
  """
  Object handling MaTiSSe.py configuration
  """
  def __init__(self):
    self.verbose = False
    self.indented = False  # indent html output: can corrupt TOC rendering (specailly if white-space:pre-wrap style is used)
    return
  def __str__(self):
    string = ['MaTiSSe.py configuration']
    string.append('\n  Verbose mode: '+str(self.verbose))
    string.append('\n  Indent html output: '+str(self.indented))
    return ''.join(string)
  def is_verbose(self):
    """
    Method inquiring verbose mode.
    """
    return self.verbose
  def is_indented(self):
    """
    Method inquiring indent mode.
    """
    return self.indented
# global variables
__initialized__ = False
if not __initialized__:
  __config__ = MaTiSSeConfig()
  __initialized__ = True
