#!/usr/bin/env python
"""Script for creating tests reference values"""
import os
import subprocess
import sys

__md_files__ = [os.path.join(dp, f) for dp, dn, filenames in os.walk('.') for f in filenames if f.endswith('.md')]

def syswork(cmd):
  """
  Function for executing system command 'cmd': for compiling and linking files.
  """
  try:
    output = subprocess.check_output(cmd, shell=True)
  except subprocess.CalledProcessError as err:
    if err.returncode != 0:
      print(output)
      sys.exit(1)
  return

def create():
  """Function for creating tests reference values."""
  pyver = str(sys.version_info.major)+'.'+str(sys.version_info.minor)+'.'+str(sys.version_info.micro)
  print('Python'+pyver)
  for mdf in __md_files__:
    directory = os.path.dirname(mdf)
    inputfile = os.path.basename(mdf)
    print('Creating '+directory)
    cmd = 'cd '+directory+' ; ../../../main/python/MaTiSSe.py -i '+inputfile+' -o '+inputfile[:-3]+pyver+' ; cd -'
    syswork(cmd)
  return

if __name__ == "__main__":
  create()
