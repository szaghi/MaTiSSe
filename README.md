[![Build Status](https://travis-ci.org/szaghi/MaTiSSe.png)](https://travis-ci.org/szaghi/MaTiSSe)

# MaTiSSe.py
### <a name="top">MaTiSSe.py, Markdown To Impressive Scientifiic Slides
A very simple and stupid (KISS) presentation maker based on simple `markdown` syntax producing high quality first-class html/css presentation with great support for scientific contents.

## <a name="toc">Table of Contents
* [Team Members](#team-members)
    + [Contributors](#contributors)
* [Why?](#why)
* [Main features](#main-features)
* [Todos](#todos)
* [Requirements](#requirements)
* [Install](#install)
    + [Manual Installation](#manual-install)
* [Getting Help](#help)
* [Copyrights](#copyrights)
* [Usage](#usage)
* [Examples](#examples)
* [Tips for non pythonic users](#tips)
* [Version History](#versions)

## <a name="team-members"></a>Team Members
* Stefano Zaghi, aka _szaghi_ <https://github.com/szaghi>

### <a name="contributors"></a>Contributors
* not yet... be the first!

Go to [Top](#top) or [Toc](#toc)
## <a name="why"></a>Why?

There are tons of markdown to html presentation tools. 

#### Why yet another presenter?

Because other tools are designed for _hackers_ for producing short, essentially **not structured** presentation. For high quality scientific presentations we need more, thus MaTiSSe.py born!

MaTiSSe.py should:

* use simple markdown source to produce high-quality html-based presentation;
* support for structured, long presentations:
    + presentation metadata; 
    + sections and subsections; 
    + helpers, e.g TOC, countdown timer, navigation-controls, etc...; 
* support for non structured, short and impressive presentations;
* support for LaTeX equations, both off and online;
* support for scientific contents:
    + figure environment fully customizable;
    + note environment fully customizable;
    + code environment fully customizable;
* support for multimedia contents:
* support for easy theming:
    + the user should be able to easily create complex theme without any or with a very poor knowledge of html/css;
* provide an output quality comparable to LaTeX-beamer standard, but:
    + be faster than LaTeX compilation;
    + be easier than LaTeX programming;
* support cool effects as the modern _prezi_-like tools have.

If you like these features give a try to MaTiSSe.py, continue to read!
 
Go to [Top](#top) or [Toc](#toc)
## <a name="main-features"></a>Main features
MaTiSSe.py has a too long list of features. Here the main features are listed whereas for a complete list read the documentation materail (examples, wiki, etc...).

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
    * [x] `figures` with fully customizable environment; 
    * [x] `tables` with fully customizable environment; 
    * [x] `notes` with fully customizable environment; 
    * [x] `code listings` with syntax highlighting;
* [ ] `note handouts` support;
* [x] `impress.js` support;
* [ ] `jmpress.js` support;
* [ ] `reveal.js` support;

Go to [Top](#top) or [Toc](#toc)
## <a name="todos"></a>Todos
MaTiSSe.py is under development. Presently the most part of improvement efforts are devoted to:

+ documentation;
+ navigation control;
+ `jmpress.js` support;
+ any feature request is welcome.

Go to [Top](#top) or [Toc](#toc)
## <a name="requirements"></a>Requirements
MaTiSSe.py is written in Python and should be portable. It relies on other external programs (also free open-source codes) that are shipped within MaTiSSe.py, thus there is no need to install them separately. Only some Python modules that are not into the standard library must be installed.

Requirements:
+ Python 2.7+ or Python 3.x;
    + required modules that are not into the standard library:
        + [markdown](https://pythonhosted.org/Markdown/);
        + [yattag](http://www.yattag.org/);
+ a lot of patience with the author.

MaTiSSe.py is developed on a GNU/Linux architecture. For Windows architecture there is no support, however it should work out-of-the-box.

Go to [Top](#top) or [Toc](#toc)
## <a name="install"></a>Install

### <a name="manual-install"></a>Manual Installation
MaTiSSe.py is a complex program built-up by many python modules. However, a one-file-script wrapper is provided.

The tree structure of the MaTiSSe.py project is the following:
```bash
├── CONTRIBUTING.md
├── examples
├── LICENSE.gpl3.md
├── logo
├── matisse
├── MaTiSSe.py
├── README.md
└── setup.py
```
`MaTiSSe.py` is the wrapper of `matisse/matisse.py`. To manual install just download the whole project tree and use the wrapper script.

It can be convenient to _clone_ the project:
```bash
git clone https://github.com/szaghi/MaTiSSe
```
and then make a link to the script where your environment can find it.

Go to [Top](#top) or [Toc](#toc)
## <a name="help"></a>Getting Help]
You are reading the main documentation of MaTiSSe.py that should be comprehensive. 

However, the documentation is under developing. In particular this file is still in working in progress. A comprehensive *getting started example* is also under developing as well as other examples for reproducing *LaTeX-beamer* layouts. Finally, it is planned to maintain a wiki on the github repo.

For more help contact directly the [author](stefano.zaghi@gmail.com).

Go to [Top](#top) or [Toc](#toc)
## <a name="Copyrights"></a>Copyrights
MaTiSSe.py is an open source project, it is distributed under the [GPL v3](http://www.gnu.org/licenses/gpl-3.0.html) license. A copy of the license should be distributed within MaTiSSe.py. Anyone interested to use, develop or to contribute to MaTiSSe.py is welcome. Take a look at the [contributing guidelines](CONTRIBUTING.md) for starting to contribute to the project.

Go to [Top](#top) or [Toc](#toc)
## <a name="usage"></a>Usage
To be written.

Go to [Top](#top) or [Toc](#toc)
## <a name="examples"></a>Examples
To be written.

Go to [Top](#top) or [Toc](#toc)
## <a name="tips"></a>Tips for non pythonic users
In the examples above MaTiSSe.py is supposed to have the executable permissions, thus it is used without an explicit invocation of the Python interpreter. In general, if MaTiSSe.py is not set to have executable permissions, it must be executed as:

```bash
python MaTiSSe.py ...
```
Go to [Top](#top) or [Toc](#toc)
## <a name="versions"></a>Version History
In the following the changelog of most important releases is reported.
### v0.0.1
##### Download [ZIP](https://github.com/szaghi/MaTiSSe/archive/v0.0.1.zip) ball or [TAR](https://github.com/szaghi/MaTiSSe/archive/v0.0.1.tar.gz) one
First, STABLE release.

Go to [Top](#top) or [Toc](#toc)
