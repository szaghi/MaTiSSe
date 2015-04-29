#!/usr/bin/env python
"""Setup script for install MaTiSSe.py"""
import os
import re
from setuptools import setup
__data_files_builtin_themes__ = [os.path.join(dp, f) for dp, dn, filenames in os.walk('matisse/utils/builtin_themes/') for f in filenames]
__data_files_css__ = [os.path.join(dp, f) for dp, dn, filenames in os.walk('matisse/utils/css/') for f in filenames]
__data_files_js__ = [os.path.join(dp, f) for dp, dn, filenames in os.walk('matisse/utils/js/') for f in filenames]
__data_files_pairs__ = []
for data in __data_files_builtin_themes__:
  __data_files_pairs__.append((os.path.dirname(data), [data]))
for data in __data_files_css__:
  __data_files_pairs__.append((os.path.dirname(data), [data]))
for data in __data_files_js__:
  __data_files_pairs__.append((os.path.dirname(data), [data]))

__source__ = open('matisse/matisse.py').read()
__license__ = re.search(r'^__license__\s*=\s*"(.*)"', __source__, re.M).group(1)

if __name__ == '__main__':
  setup(name=re.search(r'^__appname__\s*=\s*"(.*)"', __source__, re.M).group(1),
        version=re.search(r'^__version__\s*=\s*"(.*)"', __source__, re.M).group(1),
        description=re.search(r'^__description__\s*=\s*"(.*)"', __source__, re.M).group(1),
        long_description=re.search(r'^__long_description__\s*=\s*"(.*)"', __source__, re.M).group(1),
        author=re.search(r'^__author__\s*=\s*"(.*)"', __source__, re.M).group(1),
        author_email=re.search(r'^__author_email__\s*=\s*"(.*)"', __source__, re.M).group(1),
        url=re.search(r'^__url__\s*=\s*"(.*)"', __source__, re.M).group(1),
        scripts=['MaTiSSe.py'],
        packages=['matisse', 'matisse.data', 'matisse.presentation', 'matisse.utils', 'matisse.theme', 'matisse.theme.slide'],
        py_modules=[],
        classifiers=['Development Status :: 5 - Production/Stable',
                     'License :: OSI Approved :: ' + __license__,
                     'Environment :: Console',
                     'Intended Audience :: End Users/Desktop',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.4',
                     'Topic :: Text Processing'],
        entry_points={'console_scripts': []},
        package_data={'': ['*.md', '*.css', '*.js', '*.png']},
        data_files=__data_files_pairs__,
        include_package_data=True,
        install_requires=["markdown", "yattag"])
