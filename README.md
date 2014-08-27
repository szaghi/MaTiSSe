[![Build Status](https://travis-ci.org/szaghi/MaTiSSe.png)](https://travis-ci.org/szaghi/MaTiSSe)

# MaTiSSe.py
### <a name="top">MaTiSSe.py, Markdown To Impressive Scientifiic Slides
A very simple and stupid presentation maker based on simple `markdown` syntax.

## <a name="toc">Table of Contents
* [Team Members](#team-members)
    + [Contributors](#contributors)
* [Why?](#why)
* [Main features](#main-features)
* [Todos](#todos)
* [Requirements](#requirements)
* [Install](#install)
    + [Manual Installation](#manual-install)
    + [PyPI Installation, the Python Package Index](#pip-install)
* [Getting Help](#help)
* [Copyrights](#copyrights)
* [Usage](#usage)
* [Examples](#examples)
* [Tips for non pythonic users](#tips)
* [Version History](#versions)

## <a name="team-members"></a>Team Members
* Stefano Zaghi, aka _szaghi_ <https://github.com/szaghi>

### <a name="contributors"></a>Contributors
* not yet...

Go to [Top](#top) or [Toc](#toc)
## <a name="why"></a>Why?
To be written.

Go to [Top](#top) or [Toc](#toc)
## <a name="main-features"></a>Main features
To be written.

* [ ] `markdown-to-html` slides maker;
* [ ] `beamer-like-styles` support;
* [ ] `impress.js` support;
* [ ] `reveal.js` support;
* [ ] `latex equations` support;

Go to [Top](#top) or [Toc](#toc)
## <a name="todos"></a>Todos
To be written.
+ any feature request is welcome.

Go to [Top](#top) or [Toc](#toc)
## <a name="requirements"></a>Requirements
To be written.

+ Python 2.7+ or Python 3.x;
    + required modules:
        + sys;
        + os;
        + argparse;
        + configparser;
        + re;
    + optional modules:
        + datetime;
        + multiprocessing;
+ a lot of patience with the author.

MaTiSSe.py is developed on a GNU/Linux architecture. For Windows architecture there is no support, however it should work out-of-the-box.

Go to [Top](#top) or [Toc](#toc)
## <a name="install"></a>Install
To be written.

### <a name="manual-install"></a>Manual Installation
MaTiSSe.py is a one-file-script, consequently it does not need a real installation: simply download the script and placed into your PATH. See the [requirements](#requirements) section.

However, note that the script placed into the root of MaTiSSe.py project is just a wrapper to the real script. As a matter of fact, the tree structure of the MaTiSSe.py project is the following:
```bash
├── CONTRIBUTING.md
├── LICENSE.gpl3.md
├── MaTiSSe
│   ├── __init__.py
│   ├── __main__.py
│   └── MaTiSSe.py
├── MaTiSSe.py
├── README.md
└── setup.py
```
Therefore, the actual script that you need to download is `MaTiSSe/MaTiSSe.py `. This cumbersome files tree is necessary to create a valid `PyPI egg`, see PyPI [install](#pip-install) procedure.

It can be convenient to _clone_ the project:
```bash
git clone https://github.com/szaghi/MaTiSSe
```
and then make a link to the script where your environment can find it.

### <a name="pip-install"></a>Using, PyPI the Python Package Index
MaTiSSe.py can be installed by means of `pip`, the python installer that search into the PyPI (Python Package Index) for packages and automatically install them. Just type:
```bash
pip install MaTiSSe.py
```
Note that you need root permissions if you are not using your virtualenv or you are trying to install MaTiSSe.py into your system space.

It is worth noting that the `pip` installation will create a command line tool named `MaTiSSe` and not `MaTiSSe.py`: take this into account when using MaTiSSe.py.

It is also worth noting that the `pip` installation will allow you to directly import MaTiSSe.py code into your Python application by means of module import, e.g.
```python
from MaTiSSe.MaTiSSe import parse_file
```
will import the `parse_file` function into your python application.

Go to [Top](#top) or [Toc](#toc)
## <a name="help"></a>Getting Help]
You are reading the main documentation of MaTiSSe.py that should be comprehensive. For more help contact directly the [author](stefano.zaghi@gmail.com).

Go to [Top](#top) or [Toc](#toc)
## <a name="Copyrights"></a>Copyrights
MaTiSSe.py is an open source project, it is distributed under the [GPL v3](http://www.gnu.org/licenses/gpl-3.0.html) license. A copy of the license should be distributed within MaTiSSe.py. Anyone interested to use, develop or to contribute to MaTiSSe.py is welcome. Take a look at the [contributing guidelines](CONTRIBUTING.md) for starting to contribute to the project.

Go to [Top](#top) or [Toc](#toc)
## <a name="usage"></a>Usage
To be written.

Printing the main help message:
```bash
MaTiSSe.py -h
```
This will echo:
```bash
usage: MaTiSSe.py [-h] [-v] [-o OUTPUT] [-D D [D ...]] [-lm] input

MaTiSSe.py, Preprocessor for Fortran poor Men

positional arguments:
  input                 Input file name of source to be preprocessed

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show version
  -o OUTPUT, --output OUTPUT
                        Output file name of preprocessed source
  -D D [D ...]          Define a list of macros in the form NAME1=VALUE1
                        NAME2=VALUE2...
  -lm, --list-macros    Print the list of macros state as the last parsed line
                        left it
```

Go to [Top](#top) or [Toc](#toc)
## <a name="examples"></a>Examples
Into the directory _examples_ there are some KISS examples, just read their provided _REAMDE.md_.

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
Very first, totally UNSTABLE release.

Go to [Top](#top) or [Toc](#toc)
