#!/usr/bin/env python
"""Build script for MaTiSSe.py"""
from pybuilder.core import Author,init,use_plugin
import re

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.coverage')
use_plugin('python.pylint')
use_plugin('python.install_dependencies')

__source__ = open('src/main/python/matisse/matisse.py').read()

authors = [Author(re.search(r'^__author__\s*=\s*"(.*)"', __source__, re.M).group(1),
                  re.search(r'^__author_email__\s*=\s*"(.*)"', __source__, re.M).group(1))]
version = re.search(r'^__version__\s*=\s*"(.*)"', __source__, re.M).group(1)
license = re.search(r'^__license__\s*=\s*"(.*)"', __source__, re.M).group(1)
description       = re.search(r'^__description__\s*=\s*"(.*)"', __source__, re.M).group(1)
url               = re.search(r'^__url__\s*=\s*"(.*)"', __source__, re.M).group(1)

@init
def initialize(project):
  """Initializing the building class."""
  project.version = version
  project.build_depends_on('coverage')
  project.build_depends_on('pylint')
  #project.build_depends_on('re')
  #project.build_depends_on('unittest')
  project.depends_on('markdown')
  project.depends_on('yattag')

  project.set_property('verbose', True)

  project.set_property('coverage_break_build',False)
  project.set_property('dir_target','release')
  project.set_property('dir_dist','release/'+project.name+'-'+project.version)
  project.set_property('dir_reports','release/reports-'+project.name+'-'+project.version)

  project.default_task = ['analyze','publish']
