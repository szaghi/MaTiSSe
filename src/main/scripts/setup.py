#!/usr/bin/env python
import os
import re
from setuptools import setup
from shutil import rmtree
import sys
__data_files_css__ = [os.path.join(dp, f) for dp, dn, filenames in os.walk('matisse/utils/css/') for f in filenames]
__data_files_js__  = [os.path.join(dp, f) for dp, dn, filenames in os.walk('matisse/utils/js/' ) for f in filenames]
__data_files_pairs__ = []
for data in __data_files_css__:
  __data_files_pairs__.append((os.path.dirname(data),[data]))
for data in __data_files_js__:
  __data_files_pairs__.append((os.path.dirname(data),[data]))

__source__ = open('matisse/matisse.py').read()
__license__ = re.search(r'^__license__\s*=\s*"(.*)"', __source__, re.M).group(1)
if __name__ == '__main__':
  setup(name              = re.search(r'^__appname__\s*=\s*"(.*)"', __source__, re.M).group(1),
        version           = re.search(r'^__version__\s*=\s*"(.*)"', __source__, re.M).group(1),
        description       = re.search(r'^__description__\s*=\s*"(.*)"', __source__, re.M).group(1),
        author            = re.search(r'^__author__\s*=\s*"(.*)"', __source__, re.M).group(1),
        author_email      = re.search(r'^__author_email__\s*=\s*"(.*)"', __source__, re.M).group(1),
        license           = __license__,
        url               = re.search(r'^__url__\s*=\s*"(.*)"', __source__, re.M).group(1),
        scripts           = ['MaTiSSe.py'],
        packages          = ['matisse', 'matisse.data', 'matisse.md_mathjax', 'matisse.presentation', 'matisse.utils', 'matisse.theme', 'matisse.theme.slide'],
        py_modules        = [],
        classifiers       = ['Development Status :: 4 - Beta',
                             'Environment :: Console',
                             'Intended Audience :: Scientific Researchers',
                             'License :: OSI Approved :: '+__license__,
                             'Programming Language :: Python',
                             'Programming Language :: Python :: 2',
                             'Programming Language :: Python :: 2.7',
                             'Programming Language :: Python :: 3',
                             'Programming Language :: Python :: 3.2',
                             'Programming Language :: Python :: 3.3',
                             'Programming Language :: Python :: 3.4',
                             'Topic :: Utilities'],
        entry_points      = { 'console_scripts': [] },
        data_files        = __data_files_pairs__,
        install_requires  = [ "markdown", "yattag" ],
        zip_safe          = False)
  if len(sys.argv) >= 2:
    if sys.argv[1] == 'install':
      rmtree('build')
      rmtree('dist')
      rmtree('MaTiSSe.py.egg-info')
