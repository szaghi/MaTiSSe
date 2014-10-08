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

$include(main_theme.md)

#titlepage[plain]

$box
$style[width:100%;height:35%;background:#4788B3;font-family:'Comic Sans MS', cursive, sans-serif;]
$content[color:white;text-align:center;]{
$title[font-size:200%;padding-top:2%;]
$subtitle[font-size:120%;padding-top:2%;] 
$logo[height:50px;] 
}
$endbox

$box
$style[width:100%;font-family:'Comic Sans MS', cursive, sans-serif;]
$content[text-align:center;]{
a presentation by $authors[font-size:150%]
$emails[font-size:90%;]
$affiliations
}
$endbox

$box
$style[width:100%;padding-top:2%;font-family:'Comic Sans MS', cursive, sans-serif;]
$content[text-align:center;color:#4788B3;]{
$conference[font-size:150%;]
$session[font-size:120%;]
$location[font-size:90%;text-align:right;padding-right:5%;padding-top:5%;]
$date[font-size:90%;text-align:right;padding-right:5%;]
}
$endbox

# Introduction

## MaTiSSe.py, what is?

### The Acronym

_MaTiSSe.py_ means **Ma**rkdown **T**o **I**mpressive **S**cientific **S**lid**e**s

It is basically a very simple and stupid *KISS* presentation maker based on simple *markdown* syntax.

For example the markdown code of this slide is:

```md
_MaTiSSe.py_ means **Ma**rkdown **T**o **I**mpressive 
**S**cientific **S**lid**e**s

It is basically a very simple and stupid *KISS* 
presentation maker based on simple *markdown* syntax.
```

All other elements, _headers, footers, sidebars, etc...,_ are handled by MaTiSSe.py once you have setup the theme of your presentation. 

$note
$content{The real cool feature is that for setting up your theme, as the one of the presentation you are reading, **you do not need to be a html-css guru!**}
$endnote

### Why?

There are tons of markdown to html presentation tools. **Why yet another presenter?** 

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

### For whom?

Let me be clear: MaTiSSe.py is designed for **scientific researchers**, _at least the brave ones_, being used to write presentation with _LaTeX-beamer_ or other no *WYSIWYG* presentation makers. _LaTeX_ is great, but some drawbacks can be highlighted:

1. the compilation of an even small presentation can be _time consuming_;
2. LaTeX _programming_ can be very inflexible frustrating the user;
3. the pdf output has great quality, but it behaves not so well with multimedia content; 
4. it is rather complicated to introduce _prezi_-like effects.
5. themes handling is very cumbersome, i.e. inner/outer themes = a nightmare; 

MaTiSSe.py is designed for scientific researchers that want retain the best of _LaTeX-beamer_ and _prezi_ worlds together overcoming the above listed drawbacks. 

$note
$content{MaTiSSe.py is not a *wysiwyg* tool: the content is separated from the layout exactly as in the LaTeX approach.}
$endnote

$figure
$content[padding:1% 5%;width:74%;box-shadow: 7px 7px 5px rgba(200,200,200,0.3);border-radius:25px]{images/types_of_editors.png}
$caption(None){copyrights of http://xkcd.com/}
$endfigure
 
### Requirements

$columns

$column[width:50%;padding-rigth:1%;]

##### Python dependencies
MaTiSSe.py relies on other great python module for making its magic:

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

$column[width:50%;padding-left:1%;]

##### External dependencies
MaTiSSe.py relies on other programs that are shipped within MaTiSSe.py itself. The author would like to thank the authors of these programs singularly:

* for `prezi`-like effects MaTiSSe.py relies on:
    + [impress.js](https://github.com/bartaz/impress.js/);
* for LaTeX equation rendering MaTiSSe.py relies on:
    + [MathJax](http://www.mathjax.org/);
    + [md_mathjax](https://github.com/epsilony/md_mathjax);
* for syntax highlighting MaTiSSe.py relies on:
    + [highlight.js](https://highlightjs.org/);
* for resetting the main CSS theme MaTiSSe.py relies on:
    + [normalize.css](https://github.com/necolas/normalize.css);
 
$endcolumns

## Getting started

### Manual Installation
MaTiSSe.py is a complex program built-up by many python modules. However, a one-file-script wrapper is provided.

The tree structure of the MaTiSSe.py project is the following:
```bash
|-- CONTRIBUTING.md
|-- examples
|-- LICENSE.gpl3.md
|-- logo
|-- matisse
|-- MaTiSSe.py
|-- README.md
|-- setup.py
```
`MaTiSSe.py` is the wrapper of `matisse/matisse.py`. To manual install just download the whole project tree and use the wrapper script.

It can be convenient to _clone_ the project:
```bash
git clone https://github.com/szaghi/MaTiSSe
```
and then make a link to the script where your environment can find it.
 
$note
$content{
PIP installation is under developing.
}
$endnote

After installation, you are ready to convert your markdown source into impressive html presentation...

### How it works?
You write your presentation in markdown and MaTiSSe.py creates an impressive presentation even if you are a *boring scientific researcher*. MaTiSSe.py is a no-WYSISWYG command line, CLI, tool. Printing the main help message:
```bash
MaTiSSe.py -h
```
will echo:
```bash
usage: MaTiSSe.py [-h] [-v] [-i INPUT] [-o OUTPUT] [-hs STYLE.CSS]
                  [--toc-at-sec-beginning TOC-DEPTH]
                  [--toc-at-subsec-beginning TOC-DEPTH] [--print-preamble]
                  [--print-css] [--print-options] [--print-highlight-styles]
                  [--verbose] [--indented] [--online-MathJax]

MaTiSSe.py, Markdown To Impressive Scientific Slides

optional arguments:
  -h, --help            show this help message and exit
...
```  

The basic usage is:
```bash
MaTiSse.py -i your_presentation.md
```
This command will generate a *new* directory into which the html presentation is created. To visualize the presentation open the **index.html** file just created with your preferred browser:
```bash
chromium index.html
```

### How it works? (continued)

To generate the presentation you are reading I have used the following command line arguments:

```bash
MaTiSSe.py -i getting_started.md --indented --toc-at-subsec-beginning 2
```
That means:

+ process the source file `getting_started.md`;
+ indent the html output, `--indented`; 
+ insert a TOC at the beginning of each subsection with a depth of 2, `--toc-at-subsec-beginning 2`; 

MaTiSSe.py will create a directory, named *getting_started*, into which the compiled html presentation is placed.

$note
$content{
For a comprehensive explanation of the CLI arguments see the main documentation at the official GitHub [repository](https://github.com/szaghi/MaTiSSe)
}
$endnote

Now you must learn how to write your markdown source... Writing a presentation with MaTiSSe.py means:

1. write the contents in (extended) markdown syntax;
2. define the theme of the presentation.

In both the steps MaTiSSe.py is strongly friendly. 

Firstly we see the MaTiSSe.py *flavored* markdown syntax.

### MaTiSSe.py flavored markdown syntax: presentation metadata

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
All metadata values are treated as string except the one with `[]` brackets that are list of strings. 

### MaTiSSe.py flavored markdown syntax: presentation metadata (continued)

To define the presentation metadata you must use a specific environment, i.e. `---metadata`-`---endmetadata`:
```lua
---metadata
metadata_name1 = metadata_value1
metadata_name2 = metadata_value2
...
---endmetadata
```
The metadata of this presentation is the following:
```lua
---metadata
title              = Getting Started to play with MaTiSSe.py
subtitle           = a bad-showcase of MaTiSSe.py features 
authors            = ['Stefano Zaghi','John Doe']
authors_short      = ['S. Zaghi','J. Doe']
emails             = ['stefano.zaghi@gmail.com','jdoe@lost.com']
affiliations       = ['NERD Laboratory, The World Most Uncool Research Center','LOST Institute, Missed People Research Institute']
affiliations_short = ['NERD Laboratory','LOST Institute']
location           = "Via dell'Isola del Giorno Prima 139, Utopia, Universo"
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
### Presentation structuring
MaTiSSe.py supports the structuring of long presentation. As a matter of fact, for long scientific presentation, it is often useful to structure the talk into sections and/or subsections. Therefore, after the preamble, where typically the user defines theme and metadata, the presentation structuring starts:
```md
# First section
## First subsection of first section
### First slide of first subsection of first section
```
As you can see defining a section/subsection/slide is very simple: just use the h1/h2/h3 headings of markdown, respectively. The titles of these structures are available as metadata (e.g. `sectiontitle`, `sectionnumber`, `slidetitle`, etc...) and can be used inside other elements.

Note that if you define at least one section all other subsections/slides before this section are omitted:
```md
## Bad placed subsection
### Bad placed slide
# First section
## First subsection of first section
### First slide of first subsection of first section
```
The same is valid if at least one subsection is defined. If `--verbose` is used this kind of  *issues* are highlighted into the standard output warnings, but the compilation is still completed.

At this point, it is useful to define the MaTiSSe.py *universe*...

### Presentation structuring (continued)
 
The **universe** of MaTiSSe.py is composed by an _infinite canvas_ over which the presentation slides are rendered:

$columns

$column[width:45%;padding: 0 1%;]

* **presentation** with its own options, having:
    + one **canvas** with its own options over wich the slides are rendered:
    + N **slide**(s) with their own options; each slide has: 
        * $N_H$ **headers**, with $N_H \in [0,\infty]$; 
        * $N_F$ **footers**, with $N_F \in [0,\infty]$; 
        * $N_L$ left **sidebars**, with $N_L \in [0,\infty]$; 
        * $N_R$ right **sidebars**, with $N_R \in [0,\infty]$; 
        * 1 main **content**.

$column[width:55%;padding-left:1%;]

$figure
$content[padding:1% 5%;width:100%;box-shadow: 5px 5px 3px rgba(200,200,200,0.3);border-radius:15px;]{images/matisse-universe-no_bg.png}
$caption(none){MaTiSSe.py **Universe**}
$endfigure

$endcolumns

$note
$content{a slide has always one *content* element whereas, *headers*, *footers* and *sidebars* are optional.}
$endnote

# Customize the Theme

## MaTiSSe.py Universe

### MaTiSSe.py Universe
---slide
---theme_slide_global
slide-transition = diagonal
data-z           = -2000
data-scale       = 2
data-rotate      = 90
data-rotate-y    = 30
---endtheme_slide_global

---theme_slide_content
background = rgba(200,200,200,0.9)
---endtheme_slide_content

---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1
---endslide

The **universe** of MaTiSSe.py is composed by an _infinite canvas_ over which the presentation's slides are rendered:

* **presentation** with its own options, having:
    + one **canvas** with its own options over wich the slides are rendered:
    + N **slide**(s) with their own options; each slide has: 
        * $N_H$ **headers**, with $N_H \in [0,\infty]$; 
        * $N_F$ **footers**, with $N_F \in [0,\infty]$; 
        * $N_L$ left **sidebars**, with $N_L \in [0,\infty]$; 
        * $N_R$ right **sidebars**, with $N_R \in [0,\infty]$; 
        * 1 main **content**.

$figure
$content[padding:1% 5%;width:44%;box-shadow: 7px 7px 5px rgba(200,200,200,0.3);background:linear-gradient(rgba(184,55,0,0.8),rgba(230,126,0,0.8));border-radius:25px]{images/matisse-universe-no_bg.png}
$caption(none){MaTiSSe.py **Universe**}
$endfigure

$note
$content{a slide has always one *content* element whereas, *headers*, *footers* and *sidebars* are optional.}
$endnote

## Canvas Theme

### Canvas container, available options and their setting

Presently, the **canvas** container has only one option:

+ `background`, default `radial-gradient(rgb(240, 240, 240), rgb(190, 190, 190))`.

$note
$content{The canvas options are applied to the **body** html element. As a consequence it can be customized only at the beginning of the presentation for all slides: an eventual slide overriding theme cannot change the canvas options!}
$endnote

To set the canvas options use the following syntax:

```lua
---theme_canvas
background = #background_value
---endtheme_canvas
```

The canvas you are viewing is made by:

```lua
---theme_canvas
background = radial-gradient(rgb(240, 240, 240), rgb(110, 110, 110))
---endtheme_canvas
```

$note
$content{Such a theme data can placed anywhere inside your markdown source, however it has sense to place it at the beginning, inside the presentation _preamble_, that is just a convention rather than a physical part of the markdown document.}
$endnote

## Headings and Custom Selector Themes

### Headings and Custom Selector Themes

Besides the main presentation theme, you can set the default theme of headings (h1,h2,...,h6) and you can specify the theme of **custom selectors** for customizing special elements of the presentation that are not part of the main theme, e.g. the blocks of code. 

$note
$content{Both headings and custom selectors can be re-defined by the slide overriding theme, read the following.}
$endnote

### Headings, available options

The **headings** themes, that are 6, have the following _user_ options:

+ `width`;
+ `height`;
+ `background`, default `inherit`;
+ `border`, default `0`;
+ `border-radius`, default `0 0 0 0`;
+ `color`, default `black`;
+ `font`, default `inherit`;
+ `font-size`, default `[120%,140%,160%,180%,200%,220%]` for `[h6,h5,h4,h3,h2,h1]`;
+ `font-family`, default `Open Sans, Arial, sans-serif`;
+ `margin`, default `0`;
+ `padding`, default `0`;
+ `text-decoration`, default `inherit`;
+ `border-bottom`, default `inherit`.

The options are all standard `CSS` ones.

$note
$content{The headings `H1`, `H2` and `H3` are not available for standard use being MaTiSSe.py protected keywords; as a matter of facts, MaTiSSe.py uses these three headings for the definition of sections, subsections and slides respectively. To effectively use the first 3 headings you must use html syntax rather than markdown one.}
$endnote

### Headings, setting options

To customize the _global_ options of **heading** n. N the syntax is the following

```lua
---theme_heading_N
option_name1 = option_value1
option_name2 = option_value2
...
---endtheme_heading_N
```
where `option_name` is one of the previously cited options, e.g. `height`, `background`, etc, while `option_value` is its value. The heading options **must** be enclosed into the tags `---theme_heading_N` and  `---endtheme_heading_N` otherwise they will not considered.

$note
$content{Such a theme data can placed anywhere inside your markdown source, however it has sense to place it at the beginning, inside the presentation _preamble_, that is just a convention rather than a physical part of the markdown document.}
$endnote

### Custom Selector, available options

The **custom** selector has the following _user_ options:

+ `width          `;
+ `height         `;
+ `background     `, default `white  `;
+ `border         `, default `0      `;
+ `border-radius  `, default `0 0 0 0`;
+ `color          `, default `black  `;
+ `font           `;
+ `font-size      `, default `100%`;
+ `font-family    `, default `Open Sans, Arial, sans-serif`;
+ `display        `;
+ `margin         `;
+ `padding        `;
+ `text-decoration`;
+ `border-bottom  `;
+ `box-shadow     `;
+ `white-space    `;
+ `overflow-x     `, default `auto`;

The options are all standard `CSS` ones.

### Custom Selector, setting options

To customize a _custom_ selector the syntax is the following

```lua
---theme_selector_selname
option_name1 = option_value1
option_name2 = option_value2
...
---endtheme_selector_selname
```
where `option_name` is one of the previously cited options, e.g. `height`, `background`, etc, while `option_value` is its value. The theme data **must** be enclosed into the tags `---theme_selector_selname` and  `---endtheme_selector_selname` otherwise they will not considered.

$note
$content{Such a theme data can placed anywhere inside your markdown source, however it has sense to place it at the beginning, inside the presentation _preamble_, that is just a convention rather than a physical part of the markdown document.}
$endnote

The selector has a particular behavior for selecting nested selectors, continue read... 

### Custom Selector, setting options
continued...
```lua
---theme_selector_selname
option_name1 = option_value1
option_name2 = option_value2
...
---endtheme_selector_selname
```
$note
$content{The **selname** indicate the **class** of css element to which the theme will be applied; you can also define nested class}
$endnote
Let us suppose we want customized the theme of blocks of code that are generally defined as a `code` tag inside a `pre` tag; our custom selector should look like:
```lua
---theme_selector_pre-code
display     = block
white-space = pre
font-family = monospace, monospace
---endtheme_selector_pre-code
```
the selector name, `pre-code` will be converted into the nested css tags selector `pre code {...}` doing the magic for you: the symbol `-` is used to select nested selectors like `pre code` one.

Simple and elegant!

## Slide Theme

### Slide container, available options

The **slide** container has the following _user_ options:

+ `width           `, default `900px`;
+ `height          `, default `700px`;
+ `background      `, default `white`;
+ `border          `, default `0`;
+ `border-radius   `, default `0 0 0 0`;
+ `color           `, default `black`;
+ `font            `;
+ `font-size       `, default `100%`;
+ `font-family     `, default `Open Sans, Arial, sans-serif`;
+ `active          `, default `True`;
+ `slide-transition`, default `horizontal`;
+ `data-scale      `, default `1`;
+ `data-rotate     `, default `0`;
+ `data-rotate-x   `, default `0`;
+ `data-rotate-y   `, default `0`;
+ `data-rotate-z   `, default `0`;
+ `data-x          `, default `0`;
+ `data-y          `, default `0`;
+ `data-z          `, default `0`.

The most part of options are standard `CSS` options. However some exceptions are present. Before read about them, we discuss how set the slide options.

### Slide container, setting options

To customize the _global_ options of **slide** container the syntax is the following
```lua
---theme_slide_global
option_name1 = option_value1
option_name2 = option_value2
...
---endtheme_slide_global
```
where `option_name` is one of the previously cited options, e.g. `height`, `background`, etc, while `option_value` is its value. The slide options **must** be enclosed into the tags `---theme_slide_global` and  `---endtheme_slide_global` otherwise they will not considered. Such a theme data can placed anywhere inside your markdown source, however it has sense to place it at the beginning inside the presentantion _preamble_, that is just a convention rather than a physical part of the markdown document. 

The slide options of the slide you are reading is made by
```lua
---theme_slide_global
width            = 900px
height           = 700px
border-radius    = 10px
background       = green
color            = rgb(102,102,102)
font-size        = 100%
slide-transition = horizontal
---endtheme_slide_global
```

Let us now discuss about some of the special options.

### Slide container, SLIDE-TRANSITION option

The **slide-transition** option set the transition effect between subsequent slides. Presently, the available values for this options are:

+ `horizontal`: the slides are placed into a horizontal raw from left-to-right direction; this the default setting;
+ `-horizontal`: the slides are placed into a horizontal raw from right-to-left direction;
+ `vertical`: the slides are placed into a vertical column from top-to-bottom direction;
+ `-vertical`: the slides are placed into a vertical column from bottom-to-top direction;
+ `diagonal`: the slides are placed into a diagonal line from top/left-to-bottom/right direction;
+ `-diagonal`: the slides are placed into a diagonal line from bottom/right-to-top/left direction;
+ `diagonal-x`: the slides are placed into a diagonal line from top/right-to-bottom/left direction;
+ `diagonal-y`: the slides are placed into a diagonal line from bottom/left-to-top/right direction;
+ `absolute`: the slides are placed exactly where indicated by `data-x`, `data-y` and `data-z` options.

The **absolute** transition mode has a practical use just for a _local-slide overriding theme_ that is the subject of a following subsection: if you set `slide-transition = absolute` in the preamble settings and you do **not** set the `data-x`, `data-y` and `data-z` values for each slide **all** slides will be placed in the same point... the canvas center!

### Slide container, DATA-SCALE option

The **data-scale** option set the scaling factor of the slides. By default it is set to `1`. This option has a practical use just for a _local-slide overriding theme_ that is the subject of a following subsection: changing its value in the preamble settings has no visual effect because all slides will be rendered with the same scaling factor. On the contrary, setting different scale for different slides using _local-slide overriding theme_ will produce a nice zooming effect...

### Slide container, DATA-ROTATE, DATA-ROTATE-X/Y/Z options

### MaTiSSe.py Universe: header element, available options

The *header* element is designed to render data in a _single row_ rather than wrap the content into multilines.

Header element has the following _user_ options:

+ `height       `,  preferably expressed in percent _of the slide height_;
+ `background   `, default `white`;
+ `border       `, default `0`;
+ `border-radius`, default `0 0 0 0`;
+ `color        `, default `black`
+ `font         `; 
+ `font-size    `, default `100%`;
+ `font-family  `, default `Open Sans, Arial, sans-serif`;
+ `elements     `, a list of objects to be inserted, e.g. slide-title, presentation-title, presentation-logo,etc...;
+ `active       `, default `True`.

The most part of options are standard `CSS` options. The special thing is the `elements` option... but let it to the following!

Note that the `width` is automatically set to `100%` and should not be customized from users.

### MaTiSSe.py Universe: header element, setting options

To customize the options of header n. _N_ the syntax is the following
```lua
---theme_slide_header_N
option_name1 = option_value1
option_name2 = option_value2
...
---endtheme_slide_header_N
```
where `option_name` is one of the previously cited options, e.g. `height`, `background`, etc, while `option_value` is its value. Each header is indicated by its own number: the numeration can be not strictly consecutive, e.g. you can start with header 2 instead of header 1. However, the insertion follows the number order, thus header 1, if present, is inserted **before** header 2. 

The header of the slide you are reading is made by
```lua
---theme_slide_header_1
height        = 6%
background    = #4788B3
color         = white
border-radius = 10px 10px 0 0
padding       = 1%
elements      = [['slidetitle','font-variant:small-caps;font-size:180%;padding:2%'],&&
                 ['logo','float:right;height:90%;']]
---endtheme_slide_header_1
```

### MaTiSSe.py Universe: the element option

# API

## Main Structures

### Sections-subsections-slides
For providing a more structured template for long presentation, _MaTiSSe.py_ supports a three-levels-hierarchy:

* sections;
    * subsections;
        * slides;

A presentation is a collection of slides organized in sections-subsections. The sections-subsections can be used for building table of contents indexes used to facilitate navigation of long presentation. Obviously, sections-subsections are not mandatory and you can create a presentation of only slides with no structure.

### Sections

A section is created by _h1 heading_ of markdown syntax, i.e.

```md
# Section Title
...
```

### Subsections

A subsection is created by _h2 heading_ of markdown syntax, i.e.

```md
## Subection Title
...
```

### Slides

A slide is created by _h3 heading_ of markdown syntax, i.e.

```md
### Slide Title
```

### Lists
* reveal.js;
* impress.js;
* LaTeX;

### $overview
---slide
---theme_slide_global
data-scale       = 10
---endtheme_slide_global
---endslide

### The Columns environment
It is often useful to subdivide the contents into columns, e.g. to place comments aside figures. MaTiSSe.py provides an
environment for such a contents layout. The syntax is:
```bash
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
#### Example

$columns

$column[width:60%;padding-right:1%;border-right:1px solid #4788B3;]
This two columns environment has been made by means of the following code:

```
$columns
$column[width:60%;padding-right:1%;border-right:1px solid #4788B3;]
This two columns...

$column[width:40%;padding-left:1%;]
...
$endcolumns
```

$column[width:40%;padding-left:1%;]
$note
$content{
The column *options* can contain any css style options, however to the options *display:block;float:left;* are automatically added. Moreover, the user should always specify the *width* option for avoiding unpredictable output.
}
$endnote

$endcolumns
 
