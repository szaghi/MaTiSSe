#!/usr/bin/env python
"""Build script for install MaTiSSe.py"""
import re
from pybuilder.core import Author,init, use_plugin
use_plugin('python.core')
#use_plugin('python.unittest')
#use_plugin('python.coverage')
#use_plugin('python.distutils')

name = re.search(r'^__appname__\s*=\s*"(.*)"', open('matisse/matisse.py').read(), re.M).group(1)
version = re.search(r'^__version__\s*=\s*"(.*)"', open('matisse/matisse.py').read(), re.M).group(1)
authors = [Author(re.search(r'^__author__\s*=\s*"(.*)"', open('matisse/matisse.py').read(), re.M).group(1),
                  re.search(r'^__author_email__\s*=\s*"(.*)"', open('matisse/matisse.py').read(), re.M).group(1))]
license = re.search(r'^__license__\s*=\s*"(.*)"', open('matisse/matisse.py').read(), re.M).group(1)
url = re.search(r'^__url__\s*=\s*"(.*)"', open('matisse/matisse.py').read(), re.M).group(1)

#default_task = ['analyze','publish']
default_task = ['publish']

@init
def initialize(project):
  project.set_property("dir_source_main_python", "matisse")
