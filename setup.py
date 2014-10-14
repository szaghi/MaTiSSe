#!/usr/bin/env python
"""Setup script for install MaTiSSe.py"""
import re
import sys
from setuptools import setup,find_packages
# metadata from main source
APPNAME = re.search(r'^__appname__\s*=\s*"(.*)"', open('MaTiSSe/MaTiSSe.py').read(), re.M).group(1)
VERSION = re.search(r'^__version__\s*=\s*"(.*)"', open('MaTiSSe/MaTiSSe.py').read(), re.M).group(1)
AUTHOR = re.search(r'^__author__\s*=\s*"(.*)"', open('MaTiSSe/MaTiSSe.py').read(), re.M).group(1)
AUTHOR_EMAIL = re.search(r'^__author_email__\s*=\s*"(.*)"', open('MaTiSSe/MaTiSSe.py').read(), re.M).group(1)
LICENSE = re.search(r'^__license__\s*=\s*"(.*)"', open('MaTiSSe/MaTiSSe.py').read(), re.M).group(1)
URL = re.search(r'^__url__\s*=\s*"(.*)"', open('MaTiSSe/MaTiSSe.py').read(), re.M).group(1)
#setting up setup
setup(name = APPNAME,
      packages = ['MaTiSSe'],
      py_modules = ['MaTiSSe.MaTiSSe'],
      entry_points = {"console_scripts": ['MaTiSSe = MaTiSSe.MaTiSSe:main']},
      package_data = {'': ['*.md']},
      install_requires = ['argparse'],
      version = VERSION,
      author = AUTHOR,
      author_email = AUTHOR_EMAIL,
      url = URL,
      description = "MaTiSSe.py, Markdown To Impressive Scientific Slides",
      classifiers = ["Development Status :: 5 - Production/Stable", "License :: OSI Approved :: "+LICENSE])
