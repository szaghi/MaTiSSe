#!/usr/bin/env python
"""Testing columns environment"""
# import doctest
from __future__ import print_function
import os
from shutil import rmtree
import sys
import subprocess
import unittest
# import matisse.presentation as presentation
# import matisse.theme as theme
from matisse.matisse_config import MatisseConfig
from matisse.presentation import Presentation

__compare_dirs__ = [dp for dp, dn, filenames in os.walk('src/unittest/python/compare/') for f in filenames if f == 'test.md']
__pyver__ = str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '.' + str(sys.version_info.micro)


def syswork(cmd):
  """
  Executing system command 'cmd'.

  Parameters
  ----------
  cmd : str
    string containing the command
  """
  try:
    output = subprocess.check_output(cmd, shell=True)
  except subprocess.CalledProcessError as err:
    if err.returncode != 0:
      print(output)
      sys.exit(1)
  return


class SuiteTest(unittest.TestCase):
  """Testing suite for MaTiSSe.py."""

  def __init__(self, *args, **kwargs):
    super(SuiteTest, self).__init__(*args, **kwargs)
    self.config = MatisseConfig()
    dirslist = ['src/unittest/python/utils/']
    for cdir in __compare_dirs__:
      dirslist.append(cdir)
    for cdir in dirslist:
      print('Preparing ' + cdir)
      # if cdir.endswith('checklists') and not __mdx_checklist__:
      #   continue
      # if cdir.endswith('timer') and not __mdx_checklist__:
      #   continue
      old_pwd = os.getcwd()
      os.chdir(cdir)
      if os.path.exists('test' + __pyver__):
        rmtree('test' + __pyver__)
      syswork('MaTiSSe.py -i test.md -o test' + __pyver__)
      os.chdir(old_pwd)
    self.assertEqual(0, 0)
    return

  def test_compares(self):
    """Comparing tests."""
    self.maxDiff = None
    num_failures = 0
    failed = []
    passed = []
    for cdir in __compare_dirs__:
  #     if cdir.endswith('checklists') and not __mdx_checklist__:
  #       continue
  #     if cdir.endswith('timer') and not __mdx_checklist__:
  #       continue
      if os.path.exists(cdir + os.sep + 'test.md'):
        source = open(cdir + os.sep + 'test.md').read()
        talk = Presentation()
        talk.parse(config=self.config, source=source)
        if os.path.exists(cdir + os.sep + 'test' + __pyver__):
          if open(cdir + os.sep + 'test' + __pyver__ + os.sep + 'index.html').read() != talk.to_html(config=self.config):
            num_failures += 1
            failed.append([cdir, talk.to_html(config=self.config)])
          else:
            passed.append(cdir)
          rmtree(cdir + os.sep + 'test' + __pyver__)
        else:
          num_failures += 1
          failed.append([cdir, talk.to_html(config=self.config)])
    if len(passed) > 0:
      print('Tests Passed')
      for done in passed:
        print('  ' + done)
    if len(failed) > 0:
      print('Tests Failed')
      for fail in failed:
        print('  ' + fail[0])
        print(fail[1])
    self.assertEquals(num_failures, 0)
    return

  # def test_utils(self):
  #   """Test utils module."""
  #   source = open('src/unittest/python/utils/test.md').read()
  #   talk = Presentation(source=source)
  #   make_output_tree(output='src/unittest/python/utils/utils/')
  #   talk.save('src/unittest/python/utils/utils/')
  #   self.assertEqual(open('src/unittest/python/utils/test' + __pyver__ + '/index.html').read(),
  #                    open('src/unittest/python/utils/utils/index.html').read())
  #   rmtree('src/unittest/python/utils/utils')
  #   rmtree('src/unittest/python/utils/test' + __pyver__)
  #   return

  # def test_docstrings(self):
  #   """Test docstrings into modules."""
  #   num_failures = doctest.testmod(data)[0]
  #   self.assertEquals(num_failures, 0)
  #   num_failures = doctest.testmod(presentation.metadata)[0]
  #   self.assertEquals(num_failures, 0)
  #   num_failures = doctest.testmod(theme.slide.header)[0]
  #   self.assertEquals(num_failures, 0)
  #   num_failures = doctest.testmod(theme.slide.footer)[0]
  #   self.assertEquals(num_failures, 0)
  #   num_failures = doctest.testmod(theme.slide.sidebar)[0]
  #   self.assertEquals(num_failures, 0)
  #   num_failures = doctest.testmod(theme.slide.content)[0]
  #   self.assertEquals(num_failures, 0)
  #   num_failures = doctest.testmod(theme.slide.position)[0]
  #   self.assertEquals(num_failures, 0)
  #   num_failures = doctest.testmod(theme.slide.slide)[0]
  #   self.assertEquals(num_failures, 0)
  #   num_failures = doctest.testmod(theme.theme)[0]
  #   self.assertEquals(num_failures, 0)
  #   num_failures = doctest.testmod(theme.theme_element)[0]
  #   self.assertEquals(num_failures, 0)
  #   num_failures = doctest.testmod(utils.source_editor)[0]
  #   self.assertEquals(num_failures, 0)
  #   return

if __name__ == "__main__":
  unittest.main()
