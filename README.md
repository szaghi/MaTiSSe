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
* [Guidelines: writing a presentation with MaTiSSe.py](#guidelines)
    + [Writing the markdown source](#writing-markdown)
    + [Theming: defining the presentation theme](#theming)
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
+ progress bar;
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
In this section the general guidelines for writing a presentation with MaTiSSe.py are reported. Writing a presentation with MaTiSSe.py means:

1. write the contents in (extended) markdown syntax;
2. define the theme of the presentation.

In both the steps MaTiSSe.py is strongly friendly. 

### <a name="writing-markdown"></a>Writing the markdown source

#### Presentation metadata
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
All metadata values are treated as string except the one with `[]` brackets that are list of strings. To define the presentation metadata you must use a specific environment, i.e. `---metadata`-`---endmetadata`:
```lua
---metadata
metadata_name1 = metadata_value1
metadata_name2 = metadata_value2
...
---endmetadata
```
A valid example is the following:
```lua
---metadata
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
---endmetadata
```
Note that defining the values you do not need to enclose them into `''`, while it is mandatory for list values (i.e. authors, emails, affiliations, etc...). In case a metadata value is too long (accordingly to your preference) to be written inside only one line you can split it into multi-lines by the `&&` line-break marker, e.g.:
```lua
---metadata
...
affiliations = ['NERD Laboratory, The World Most Uncool Research Center', &&
                'LOST Institute, Missed People Research Institute']
...
---endmetadata
```

The metadata should be auto-explicative, whereas the last two merit a comment:

+ `max_time`: this indicates the time (in minutes) you have for your presentation; this value is used to the countdown timer if you used it inside the presentation (e.g. it can be useful to visualize the remaining time for terminating in time your talk);
+ `dirs_to_copy`: this list contains the directories that will be copied into the output directory; as a matter of fact, it is common to place some contents (images, videos, tables, etc...) into subdirectories of your root presentation: MaTiSSe.py uses relative paths thus such subdirectories must be copied into the output path.

Other two metadata are available, but do not need to be assigned a value:

+ `toc`: this the Table of Contents which is automatically built up; its using is shown in the following;
+ `total_slides_number`: this the total number of slide which is automatically built up; its using is shown in the following;

All the metadata can be used inside the presentation as shown in the following.

#### Presentation structuring
MaTiSSe.py supports the structuring of long presentation. As a matter of fact, for long scientific presentation, it is often useful to structure the talk into sections and/or subsections. Therefore, after the preamble, where typically the user defines theme and metadata, the presentation structuring starts:
```md
# First section

## First subsection of first section

### First slide of first subsection of first section

...
```
As you can see defining a section/subsection/slide is very simple: just use the h1/h2/h3 headings of markdown, respectively. The titles of these structures are available as metadata (e.g. `sectiontitle`, `sectionnumber`, `slidetitle`, etc...) and can be used inside other elements.

Note that if you define at least one section all other subsections/slides before this section are omitted:
```md
## Bad placed subsection

### Bad placed slide

# First section

## First subsection of first section

### First slide of first subsection of first section

...
```
The same is valid if at least one subsection is defined. If `--verbose` is used this kind of  *issues* are highlighted into the standard output warnings, but the compilation is still completed. Note that you can define no sections/subsections:
```md
### First slide of unstructured presentation

### Second slide of unstructured presentation

...
```
This is a valid unstructured presentation with no sections/subsections. 

The use of h1/h2/h3 headings precludes to insert such a title into the slides contents. However there other 3 headings (h4/h5/h6) that should be enough.

At this point, it is useful to define the MaTiSSe.py *universe*

![universe](examples/getting_started/images/matisse-universe-no_bg.png)

Basically there is an *infinite canvas* over which the presentation is rendered. The main element of the presentation object is obviously the slide. The slide element is composed by:

* *N_H* **headers**, with *N_H* being an arbitrary number; 
* *N_F* **footers**, with *N_F* being an arbitrary number;
* *N_L* left **sidebars**, with *N_L* being an arbitrary number;
* *N_R* right **sidebars**, with *N_R* being an arbitrary number;
* *1* main **content**.

All the code after a slide title will be inserted into the **slide content** element, whereas the contents of headers, footers and sidebars are defined by the slide theme. These latter elements are by default disabled, thus the slide content occupies the 100% of the slide surface:
```md
### Example of slide contents

#### This is a h4 title example
This contents is placed into the **content** element of the slide that is the only one being enabled by default.

##### This is a h5 title example
This placed below the previous h4-titled paragraph. Note that an empty line defines a new paragraph into the html output. 
```
The headers, footers and sidebars are treated into the **Theming** section, while in the following is discussed only the slide contents writing.

Into the slide content you can place any valid markdown source. Note that the markdown used by MaTiSSe.py is an extended version of the [original one](http://daringfireball.net/projects/markdown/), that is very similar to the one used by github, the so called [GitHub Flavored Markdown](https://help.github.com/articles/github-flavored-markdown/). Indeed, the syntax supported by MaTiSSe.py is even more extended with respect the github flavored syntax: MaTiSSe.py supports latex equations and some specific environments (e.g. figure, note, table, columns, etc...). The markdown source is parsed by means of **markdown** python module: for more informations on the supported syntax see [Python-Markdown](https://pythonhosted.org/Markdown/). Here the focus is placed on the MaTiSSe.py specific syntax.

#### Code listings
The code listings is accomplished very similarly to the github flavored markdown approach. Just use fenced code blocks or in-line codes. Just remember that the syntax highlighting is achieved by means of [highlight.js](https://highlightjs.org/): only the languages supported by `highlight.js` are supported.

Note also that presently the code blocks defined by simple indentation, as the original markdown [definition](http://daringfireball.net/projects/markdown/syntax#precode) is not completely supported.

#### LaTeX equations
For scientific contents equations environments are mandatory. The *de facto* standard of equations typesetting is LaTeX. MaTiSSe.py supports LaTeX equations! Just type your equations as you do into your LaTeX source:

```md
### Equations, equations, equations... LaTeX is supported!

Just type your equations as you do into your LaTeX sources:


$$
x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}
$$
```

#### Box environment
One of the environments provided by MaTiSSe.py is a generic *box*. It is designed to contains any contents you want to be rendered with a different theme with respect other paragraph. The syntax is the following:

```md
$box
$style[style_options]
$caption(caption_type)[caption_options]{caption}
$content(content_type)[content_options]{content}
$endbox
```
where:
+ `$box` and `$endbox` are the tags defining the box environment;
+ `$style[style_options]` defines the style of the whole box (inherited by both caption and contents of the box); this is optional and can be omitted, but if defined the `[]` brackets must be present (even without options); the `style_options` are any valid css style definitions (see theming section); note that the box environment is converted to a `div` html element;
+ `$caption(caption_type)[caption_options]{caption}` defines the caption of the box that can be styled differently from the main box content and it is optional; the `(caption_type)` defines caption prefixing *class* (e.g. *Fig.* for figures) and it is itself optional: any sentences are valid; to disable the printing of the prefixing class use `$caption(none)...`; the `[caption_options]` defines the style options of the only caption: they are any valid css definitions; the `{caption}` defines the caption text (can contain anything, even multi-lines paragraph) and it must be present if `$caption` is defined; note that `(caption_type)` and `[caption_options]` are optional, thus the following statements are valid:
     + `$caption[font-variant:small-caps;]{My caption without caption_type}`;
     + `$caption{My caption without caption_type and caption_options}`;
+ `$content(content_type)[content_options]{content}` is not optional: it defines the box's content; the `(content_type)` defines defines the type of the content ('figure', 'table', 'note' and 'box' for generic environments, see the following subsections) and it is itself optional; the `[content_options]` defines the style options of the only content: they are any valid css definitions; the `{content}` defines the content data (can contain anything); note that `(content_type)` and `[content_options]` are optional, thus the following statements are valid:
     + `$content[font-variant:small-caps;]{My content without content_type}`;
     + `$content{My content without content_type and content_options}`.

Consider the following code:

```md
### Box environment example

$box
$style[background:rgb(100,100,100);]
$caption(Mybox)[font-size:90%;color:white;]{An example of a generic Box}
$content[font-size:120%;color:white;]{This box has a grey background with white colored text. The caption has a 90% (with respect the slide content font-size) font-size, whereas the box contents itself has a 120% font-size.}
$endbox
```
This example defines a box having a grey background with white colored text. The caption has a 90% (with respect the slide content font-size) font-size, whereas the box contents itself has a 120% font-size.}

Note that the themes of box environments can be defined, as all other theme elements, once for all into the preamble in order to not have to repeat the styling options for each box. The syntax for defining the boxes styles is commented into the theming section in the following. 

#### Figure environment
The *figure* environment is a subclass of box one that is specialized for rendering figures. The syntax is the following:
```md
$figure
$style[style_options]
$caption[caption_options]{caption}
$content[content_options]{content}
$endfigure
```
where the elements are the same of box environment, but:

+ the `content_type` and `caption_type` are automatically set to `figure` and `Figure` respectively; anyhow they can be still specified inside the `$figure/$endfigure` environment;
+ the `content` must be the (relative to the root) path of an external figure file;
+ no matter the order of `$caption`/`$content` statements, the caption is always placed below the content.

Consider the following code:
```md
$figure
$content[padding:1% 5%;width:44%;box-shadow: 7px 7px 5px rgba(200,200,200,0.3);border-radius:25px]{images/matisse-universe-no_bg.png}
$caption(none){MaTiSSe.py **Universe**}
$endfigure
```
This example defines a figure with a shadowed box and a caption without a prefixing class into which the contents are formatted by means of markdown syntax (do you note the double `**` emphasizing the word Universe?).

Note that, as all other box subclass, the themes of figure environments can be defined once for all into the preamble in order to not have to repeat the styling options for each figure. The syntax for defining the figures styles is commented into the theming section in the following. 

#### Note environment
The *note* environment is a subclass of box one that is specialized for rendering notes. The syntax is the following:
```md
$note
$style[style_options]
$caption[caption_options]{caption}
$content[content_options]{content}
$endnote
```
where the elements are the same of box environment, but:

+ the `content_type` and `caption_type` are automatically set to `note` and `Note` respectively; anyhow they can be still specified inside the `$note/$endnote` environment;
+ no matter the order of `$caption`/`$content` statements, the caption is always placed above the content.

Consider the following code:
```md
$note
$content{a slide has always one *content* element whereas, *headers*, *footers* and *sidebars* are optional.}
$endnote
```
This example defines a plain style note with just a text contents being formatted by means of markdown syntax. Into the rendered html you will see a caption containing `Note` similar to
```md
Note

a slide has always one *content* element whereas, *headers*, *footers* and *sidebars* are optional.
```

Note that, as all other box subclass, the themes of note environments can be defined once for all into the preamble in order to not have to repeat the styling options for each note. The syntax for defining the notes styles is commented into the theming section in the following. 
 
#### Table environment
To be written.

#### Columns environment
It is often useful to subdivide the contents into columns, e.g. to place comments aside figures. MaTiSSe.py provides an environment for such a contents layout. The syntax is:

```md
$columns
$column[column1_options]
column1_contents
$endcolumn
$column[column2_options]
column2_contents
$endcolumn
...
$endcolumns
```
where:

+ `$columns` and `$endcolumns` are the tags defining the columns environment;
+ `$column[column_options]` defines one column; the `[column_options]` is optional and defines the css style options applied to the column contents;
+ the column contents are all data that follow the `$column` statement.

Note that the number of columns defined is automatically computed by MaTiSSe.py and it is not necessary to explicitly define it. Note also that the user should always specify the *width* option of each column for avoiding unpredictable output.

Consider the following code:
```md
$columns

$column[width:60%;padding-right:1%;border-right:1px solid #4788B3;]
This is a two columns contents with a vertical line between the two columns

$column[width:40%;padding-left:1%;]
The left column is large 60% of the slide content width, while the right one is 40% wide.

$endcolumns
```
This example defines a two columns contents separated by a vertical line with the left column being large 60% of the slide content width, while the right one is 40% wide.

#### Titlepage
To be written.

#### Including external files
It is common to split long presentation into multiple files. These file can be included into the main source by

```md
$include(relative_path_to_external_file)
```

As an example the metadata and theme definition can be placed into separate files and included into the presentation as in the following example:
```md
$include(metadata.dat)

$include(theme.dat)

# First section

# First subsection

# First slide
```
The `$include` statements are parsed one time at the beginning of the MaTiSSe.py execution, therefore no recursive inclusions are admitted.

### <a name="theming"></a>Theming: defining the presentation theme
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
