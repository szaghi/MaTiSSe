 <a name="top"></a>
# MaTiSSe.py [![Latest Version](https://pypip.in/version/MaTiSSe.py/badge.svg?style=flat)](https://pypi.python.org/pypi/MaTiSSe.py/) [![GitHub tag](https://img.shields.io/github/tag/szaghi/MaTiSSe.svg)]()
# MaTiSSe.py [![Latest Version](https://img.shields.io/pypi/v/MaTiSSe.py.svg)](https://img.shields.io/pypi/v/MaTiSSe.py.svg) [![GitHub tag](https://img.shields.io/github/tag/szaghi/MaTiSSe.svg)]()

[![Join the chat at https://gitter.im/szaghi/MaTiSSe](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/szaghi/MaTiSSe?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![License](https://img.shields.io/badge/license-GNU%20GeneraL%20Public%20License%20v3,%20GPLv3-blue.svg)]()

### MaTiSSe.py, Markdown To Impressive Scientific Slides
MaTiSSe.py is a very simple and stupid (KISS) presentation maker based on simple `markdown` syntax producing high quality first-class html/css presentation with great support for scientific contents.

+ MaTiSSe.py is **NOT** *WYSIWYG*: it converts your sources to high quality html presentation with the same approach of LaTeX typesetting;
+ MaTiSSe.py is tailored to scientific contents (equations, figures, tables, etc...);
+ MaTiSSe.py is a Command Line Tool;
+ MaTiSSe.py is a Free, Open Source Project.

### Status

[![Build Status](https://travis-ci.org/szaghi/MaTiSSe.svg?branch=master)](https://travis-ci.org/szaghi/MaTiSSe)
[![Coverage Status](https://img.shields.io/coveralls/szaghi/MaTiSSe.svg)](https://coveralls.io/r/szaghi/MaTiSSe)
[![Code Health](https://landscape.io/github/szaghi/MaTiSSe/master/landscape.svg?style=flat)](https://landscape.io/github/szaghi/MaTiSSe/master)

#### Issues
[![GitHub issues](https://img.shields.io/github/issues/szaghi/MaTiSSe.svg)]()
[![Ready in backlog](https://badge.waffle.io/szaghi/matisse.png?label=ready&title=Ready)](https://waffle.io/szaghi/matisse)
[![In Progress](https://badge.waffle.io/szaghi/matisse.png?label=in%20progress&title=In%20Progress)](https://waffle.io/szaghi/matisse)
[![Open bugs](https://badge.waffle.io/szaghi/matisse.png?label=bug&title=Open%20Bugs)](https://waffle.io/szaghi/matisse)

#### Python support [![Supported Python versions](https://img.shields.io/badge/Py-%202.7,%203.4-blue.svg)]()

#### Documentation

MaTiSSe.py has a comprehensive [wiki](https://github.com/szaghi/MaTiSSe/wiki): read it to know how to install and use MaTiSSe.py.

#### A Taste of MaTiSSe.py
See MaTiSSe.py in action with the [getting started presentation](http://szaghi.github.io/MaTiSSe/#/slide-1) or see the following screenshots.

##### The Titlepage
![shot01](screenshots/01.png)

##### Figure environment
![shot02](screenshots/02.png)

##### LaTeX Equations support
![shot03](screenshots/03.png)

##### LaTeX-Beamer Themes support
![shot04](screenshots/04.png)

Go to [Top](#top)

## Main Features
MaTiSSe.py has a too much long list of features. Here the main features are listed whereas for a complete list read all the documentation material (examples, wiki, etc...).

* [x] `markdown-to-html` slides maker (with extended markdown syntax);
* [ ] support for structured, long presentations:
    * [x] presentation metadata;
    * [x] presentation sectioning:
        * [x] `titlepage`;
        * [x] `section`;
        * [x] `subsection`;
        * [x] `slide`;
    * [ ] helpers:
        * [x] `TOC`;
        * [x] `countdown timer`;
        * [ ] `navigation controls`;
* [x] easy theming:
    * [x] `canvas`;
    * [x] `headings` (h1,h2,...);
    * [x] global slide theme as well theme of a specific slide (local slide theme):
        * [x] `headers` (unlimited number);
        * [x] `footers` (unlimited number);
        * [x] `left and right sidebars` (unlimited number);
        * [x] `content`;
    * [x] `beamer-like-styles` support;
* [x] `latex equations` support;
* [x] `scientific contents` support:
    * [x] `boxes` with fully customizable environment;
    * [x] `figures` with fully customizable environment;
    * [ ] `tables` with fully customizable environment;
    * [x] `notes` with fully customizable environment;
    * [x] `code listings` with syntax highlighting;
    * [x] `columns` fully customizable environment;
* [ ] `note handouts` support;
* [x] `impress.js` support;
* [ ] `jmpress.js` support;
* [ ] `reveal.js` support;

## Copyrights
MaTiSSe.py is an open source project, it is distributed under the [GPL v3](http://www.gnu.org/licenses/gpl-3.0.html) license. A copy of the license should be distributed within MaTiSSe.py. Anyone interested to use, develop or to contribute to MaTiSSe.py is welcome. Take a look at the [contributing guidelines](CONTRIBUTING.md) for starting to contribute to the project.

Go to [Top](#top)
