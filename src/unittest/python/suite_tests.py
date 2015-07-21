#!/usr/bin/env python
"""Testing columns environment"""
# import doctest
from __future__ import print_function
import os
from shutil import rmtree
import sys
import subprocess
import unittest
from matisse.markdown_utils import __mdx_checklist__
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
    for cdir in __compare_dirs__:
      print('Preparing ' + cdir)
      if cdir.endswith('checklists') and not __mdx_checklist__:
        continue
      old_pwd = os.getcwd()
      os.chdir(cdir)
      if os.path.exists('test' + __pyver__):
        rmtree('test' + __pyver__)
      syswork('MaTiSSe.py -i test.md -o test' + __pyver__)
      os.chdir(old_pwd)
    self.assertEqual(0, 0)

  def compare(self, directory, passed, failed):
    """Compare utility.

    Parameters
    ----------
    directory: str
      where the compare test is located
    passed: list
      passed tests list
    failed: list
      failed tests list
    """
    if os.path.exists(os.path.join(directory, 'test.md')):
      source = open(os.path.join(directory, 'test.md')).read()
      talk = Presentation()
      talk.parse(config=self.config, source=source)
      if os.path.exists(os.path.join(directory, 'test' + __pyver__)):
        html_dir = os.path.join(directory, 'test' + __pyver__)
        if open(os.path.join(html_dir, 'index.html')).read() != talk.to_html(config=self.config):
          failed.append([directory, talk.to_html(config=self.config)])
        else:
          passed.append(directory)
        rmtree(os.path.join(directory, 'test' + __pyver__))
      else:
        failed.append([directory, talk.to_html(config=self.config)])

  def test_compares(self):
    """Comparing tests."""
    def print_results(passed, failed):
      """Print results.

      Parameters
      ----------
      passed: list
        passed tests list
      failed: list
        failed tests list
      """
      if len(passed) > 0:
        print('Tests Passed')
        for done in passed:
          print('  ' + done)
      if len(failed) > 0:
        print('Tests Failed')
        for fail in failed:
          print('  ' + fail[0])
          print(fail[1])

    self.maxDiff = None
    passed = []
    failed = []
    for cdir in __compare_dirs__:
      if cdir.endswith('checklists') and not __mdx_checklist__:
        continue
      self.compare(directory=cdir, passed=passed, failed=failed)
    print_results(passed=passed, failed=failed)
    self.assertEquals(len(failed), 0)

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
