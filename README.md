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

#### For whom?

Let me be clear: MaTiSSe.py is designed for **scientific researchers**, _at least the brave ones_, being used to write presentation with _LaTeX-beamer_ or other no *WYSIWYG* presentation makers. Do not you aspect a *Powerpoint* like tool: MaTiSSe.py is a converter that parses a *markdown* (extended) source and produce high-quality html presentation, very similar to  LaTeX-beamer that parsing a tex source generates a high-quality pdf presentation. 

_LaTeX_ is great, but some drawbacks can be highlighted:

1. the compilation of an even small presentation can be _time consuming_;
2. LaTeX _programming_ can be very inflexible frustrating the user;
3. the pdf output has great quality, but it behaves not so well with multimedia content (especially if the Adobe Reader is not available); 
4. it is rather complicated to introduce _prezi_-like effects.
5. themes handling is very cumbersome, i.e. inner/outer themes handling can be a nightmare; 

MaTiSSe.py is designed for scientific researchers that want retain the best of _LaTeX-beamer_ and _prezi_ worlds together overcoming the above listed drawbacks. 
 
Go to [Top](#top) or [Toc](#toc)

## <a name="main-features"></a>Main features
MaTiSSe.py has a too much long list of features. Here the main features are listed whereas for a complete list read the documentation material (examples, wiki, etc...).

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
    * [x] `columns` fully customizable environment; 
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
+ replicate all the useful features of LaTeX-beamer approach;
+ any feature request is welcome.

Go to [Top](#top) or [Toc](#toc)

## <a name="requirements"></a>Requirements
MaTiSSe.py is written in Python and should be portable. It relies on other external programs (also free open-source codes, used for only html rendering) that are shipped within MaTiSSe.py, thus there is no need to install them separately. Only some Python modules that are not into the standard library must be installed.

Requirements:
+ Python 2.7+ or Python 3.x;
    + required modules that are into the standard library and should be present in any recent Python implementation:
        + argparse;
        + ast;
        + collections;
        + copy;
        + os;
        + re;
        + shutil;
        + sys;
    + required modules that are not into the standard library:
        + [markdown](https://pythonhosted.org/Markdown/);
        + [yattag](http://www.yattag.org/);
+ a lot of patience with the author.

As aforementioned MaTiSSe.py relies on other programs that are shipped within MaTiSSe.py itself. The author would like to thank the authors of these programs singularly:

* for `prezi`-like effects MaTiSSe.py relies on:
    + [impress.js](https://github.com/bartaz/impress.js/);
* for LaTeX equation rendering MaTiSSe.py relies on:
    + [MathJax](http://www.mathjax.org/);
    + [md_mathjax](https://github.com/epsilony/md_mathjax);
* for syntax highlighting MaTiSSe.py relies on:
    + [highlight.js](https://highlightjs.org/);
* for resetting the main CSS theme MaTiSSe.py relies on:
    + [normalize.css](https://github.com/necolas/normalize.css);

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
MaTiSSe.py is a no WYSISWYG command line (CLI) tool. Printing the main help message:
```bash
MaTiSSe.py -h
```
This will echo:
```bash
usage: MaTiSSe.py [-h] [-v] [-i INPUT] [-o OUTPUT] [-hs STYLE.CSS]
                  [--toc-at-sec-beginning TOC-DEPTH]
                  [--toc-at-subsec-beginning TOC-DEPTH] [--print-preamble]
                  [--print-css] [--print-options] [--print-highlight-styles]
                  [--verbose] [--indented] [--online-MathJax]

MaTiSSe.py, Markdown To Impressive Scientific Slides

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Show version
  -i INPUT, --input INPUT
                        Input file name of markdown source to be parsed
  -o OUTPUT, --output OUTPUT
                        Output directory name containing the presentation
                        files
  -hs STYLE.CSS, --highlight-style STYLE.CSS
                        Select the highlight.js style (default github.css);
                        select "disable" to disable highligth.js
  --toc-at-sec-beginning TOC-DEPTH
                        Insert Table of Contents at each section beginning
                        (default no): to activate indicate the TOC depth
  --toc-at-subsec-beginning TOC-DEPTH
                        Insert Table of Contents at each subsection beginning
                        (default no): to activate indicate the TOC depth
  --print-preamble      Print the preamble data as parsed from source
  --print-css           Print the css as parsed from source (if done)
  --print-options       Print the available options for each presentation
                        element
  --print-highlight-styles
                        Print the available highlight.js style (default
                        github.css)
  --verbose             More verbose printing messages (default no)
  --indented            Indent html output file (default no, may corrupt slide
                        rendering)
  --online-MathJax      Use online rendering of LaTeX equations by means of
                        online MathJax service; default use offline, local
                        copy of MathJax engine
```  

The basic usage is:
```bash
MaTiSse.py -i your_presentation.md
```
This command will generate a *new* directory (be careful: some sub-directories are re-initialized any time a compilation is performed) into which the html presentation is created. After the compilation the output path contains the file **index.html** that is your main presentation file. To visualize the presentation open this file your preferred browser:
```bash
chromium index.html
```
Note that MaTiSSe.py is tested with google Chrome browser (indeed with Chromium), but all other recent browser supporting html/css and javascripts should work.

In the following notes some typical usage-scenario are reported.

### Specifying a custom output directory
```bash
MaTiSse.py -i your_presentation.md -o your_output_dir
```
This will generate the html presentation into *your_output_dir* that will be created if it does not already exist. Note that into the output path some other sub-directories are created, besides the main html presentation (index.html): as an example the *css* and *js* directories which contains the css style files and the javascripts, respectively. Moreover, all other directories you have specified into the presentation source are copied inside the root output directory. Before copy such a directories they are removed from the output if already existing thus if you manually modify the contents of output path your modification will be lost after a presentation (re)compilation. Be very careful with `MaTiSSe.py -o .`: if you  use subdirectories for other contents (e.g. images, videos) these will be definitely lost! 

### Specifying a custom highligth.js style
```bash
MaTiSse.py -i your_presentation.md -hs zenburn.css
```
This will set the style for code highlighting to `zenburn.css` instead of using the default one `github.css`. To list all the available style type: 
```bash
MaTiSse.py --print-highlight-styles
```

### Inserting Table of Contents slide at the beginning of each section and/or subsection
For long presentation it could be useful to structuring your presentation in sections and/or subsections and insert a slide summarizing the Table of Contents at the beginning of each section and/or subsection for highlighting the current slide position with respect the whole presentation (and avoid your listeners to go away before an interesting argument). To this aim there are two helper switches `--toc-at-sec-beginning` and `--toc-at-subsec-beginning`, as an example:
```bash
MaTiSse.py -i your_presentation.md  --toc-at-sec-beginning 2
```
will insert a slide with TOC (and highligthed the current slide position) at the beginning of each section. The number after the switch indicates the *depth* of the TOC:
+ depth=1, the TOC is limited to the sections list;
+ depth=2, the TOC is limited to the sections/subsections list;
+ depth=3, the TOC contains sections/subsections/slides list;

### Print presentation informations/options
MaTiSSe.py has a long list of options/usage thus it is often useful listing the informations of the current presentation and/or listing other available options.
#### Print presentation informations
```bash
MaTiSse.py -i your_presentation.md --print-preamble 
```
This will print the metadata (authors, title, emails, etc...) and the theme styles (slide dimension, background color, slides transitions, etc...) you have specified into your source.

#### Print available options
```bash
MaTiSse.py --print-options
```
This will print the available options for the metadata and theme styles of each element (canvas, slide headers, slide footers, etc...). It could also be useful to print the css theme built up by MaTiSSe.py. To see the default theme type:
```bash
MaTiSse.py --print-css
```
while to print the css theme of your actual presentation (that is built up according to the options specified into your source) type:
```bash
MaTiSse.py -i your_presentation.md --print-css
```

### Indenting the html output
The default behaviour is to produce the html without indentation. This has two advantages:

1. a smaller size index.html;
2. a safe rendering (without any unwanted white spaces...).

However, if you want to manually modify or inspect the html the indentation is necessary. In such a case type:
```bash
MaTiSse.py -i your_presentation.md --indented
```
The rendering of such a html output is unsafe especially if you have defined *containers* where the white spaces are important (e.g. code listings) because unwanted white spaces could be added.

### Using Online MathJax service
By default MaTiSSe.py uses a local (simplified) copy of MathJax engine. However, even if the local copy has been strongly compressed it still occupy about 1.8MB. In case you prefer to use the full engine of MathJax by means of the online service type:
```bash
MaTiSse.py -i your_presentation.md --online-MathJax
```
In this case the local copy of MathJax is avoided and you can save about 1.8MB of your space.

Go to [Top](#top) or [Toc](#toc)
## <a name="examples"></a>Examples
Into the directory _examples_ there are some KISS examples, just read their provided _REAMDE.md_. In the following notes the guidelines for writing a presentation with MaTiSSe.py are reported.

## <a name="guidelines"></a>Guidelines: writing a presentation with MaTiSSe.py
In this section the general guidelines for writing a presentation with MaTiSSe.py are reported.

### Presentation metadata
For long scientific presentation it is often useful to define some (meta)data in order to reuse theme inside the presentation itself. Such a data are defined into MaTiSSe.py as *metadata*. You can define the presentation metadata anywhere into your markdown source, however it has sense to place it at the beginning, inside the presentation _preamble_, that is just a convention rather than a physical part of the markdown document. The available metadata are:
```lua
title = 
subtitle = 
authors = []
authors_short = []
emails = []
affiliations = []
affiliations_short = []
logo = 
location = 
location_short = 
date = 
conference = 
conference_short = 
session = 
session_short = 
max_time = 25
dirs_to_copy = []
```
All metadata values are treated as string except the one with `[]` brackets that are list of strings. A valid example is the following:
```lua
title              = Getting Started to play with MaTiSSe.py
subtitle           = a bad-showcase of MaTiSSe.py features 
authors            = ['Stefano Zaghi','John Doe']
authors_short      = ['S. Zaghi','J. Doe']
emails             = ['stefano.zaghi@gmail.com','jdoe@lost.com']
affiliations       = ['NERD Laboratory, The World Most Uncool Research Center','LOST Institute, Missed People Research Institute']
affiliations_short = ['NERD Laboratory','LOST Institute']
location           = Via dell'Isola del Giorno Prima 139, Utopia, Universo
location_short     = Utopia, Universo
date               = 29th February, 2015
conference         = Nhill Symposium 2015
conference_short   = NS2015
session            = Third High Performance Sleeping, HPS3
session_short      = HPS3
logo               = images/logo.png
max_time           = 10
dirs_to_copy       = ['images']
```
Note that defining the values you do not need to enclose them into `''`, while it is mandatory for list values (i.e. authors, emails, affiliations, etc...).

The metadata should be auto-explicative, whereas the last two merit a comment:

+ `max_time`: this indicates the time (in minutes) you have for your presentation; this value is used to the countdown timer if you used it inside the presentation (e.g. it can be useful to visualize the remaining time for terminating in time your talk);
+ `dirs_to_copy`: this list contains the directories that will be copied into the output directory; as a matter of fact, it is common to place some contents (images, videos, tables, etc...) into subdirectories of your root presentation: MaTiSSe.py uses relative paths thus such subdirectories must be copied into the output path.

Other two metadata are available, but do not need to be assigned a value:

+ `toc`: this the Table of Contents which is automatically built up; its using is shown in the following;
+ `total_slides_number`: this the total number of slide which is automatically built up; its using is shown in the following;

All the metadata can be used inside the presentation as shown in the following.

### Presentation structuring
MaTiSSe.py support the structuring of long presentation. As a matter of fact, for long scientific presentation, it is often useful to structure the talk into sections and/or subsections. Therefore, after the preamble, where typically the user defines theme and metadata, the presentation structuring starts:
```lua
# First section

## First subsection of first section

### First slide of first subsection of first section

...
```
As you can see defining a section/subsection/slide is very simple: just use the h1/h2/h3 headings of markdown, respectively. The titles of these structures are available as metadata (e.g. `sectiontitle`, `sectionnumber`, `slidetitle`, etc...) and can be used inside other elements.

Note that if you define at least one section all other subsections/slides before this section are omitted:
```lua
## Bad placed susection

### Bad placed slide

# First section

## First subsection of first section

### First slide of first subsection of first section

...
```
The same is valid if at least one subsection is defined. If `--verbose` is used this kind of  *issues* are highlighted into the standard output warnings, but the compilation is still completed. Note that you can define no sections/subsections:
```lua
### First slide of unstructured presentation

### Second slide of unstructured presentation

...
```
This is a valid unstructured presentation with no sections/subsections. 

The use of h1/h2/h3 headings precludes to insert such a title into the slides contents. However there other 3 headings (h4/h5/h6) that should be enough.

All the code after a slide title will be inserted into the **slide content** element. At this point is useful to define the MaTiSSe.py *universe*

![universe](examples/getting_started/images/matisse-universe-no_bg.png)

### Theming

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
