---metadata
title              = a simple example of MaTiSSe.py usage
subtitle           = a bad-showacase of the basic features of MaTiSSe.py
authors            = ['Stefano Zaghi','Jhon Doe']
authors_short      = ['S. Zaghi','J. Doe']
emails             = ['stefano.zaghi@gmail.com','jdoe@zzz.com']
affiliations       = ['CNR-INSEAN, The Maritime Research Institute of National Research Council','ZZZ Research Institute']
affiliations_short = ['CNR-INSEAN','ZZZ']
location           = Via di Vallerano 139, Rome, Italy
location_short     = Rome, Italy
date               = 23th August, 2014
conference         = Nhill Symposium 2014
conference_short   = NS2014
session            = Third High Performance Sleeping, HPS3
session_short      = HPS3
logo               = images/logo.png
max_time           = 10
dirs_to_copy       = ['images']
---endmetadata

$include(main_theme.md)

# Introduction

## MaTiSSe.py, what is?

### The Acronym

_MaTiSSe.py_ means **Ma**rkdown **T**o **I**mpressive **S**cientific **S**lid**e**s

It is basically a very simple and stupid (KISS) presentation maker based on simple `markdown` syntax.

For example the markdown code of this slide is:

```
_MaTiSSe.py_ means **Ma**rkdown **T**o **I**mpressive **S**cientific **S**lid**e**s

It is basically a very simple and stupid (KISS) presentation maker based on simple `markdown` syntax.
```

All other elements (headers, footers, sidebars, etc...) are handled by MaTiSSe.py once you have setup the theme of your presentation. 

The real cool feature is that for setting up your theme (as the one of the presentation you are reading) **you do not need to be a html-css guru!**

## Getting started

### From markdown to html...

# Customize the Theme

## MaTiSSe.py Universe

### MaTiSSe.py Universe

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
$caption[font-size:80%;color:#4788B3;]{ MaTiSSe.py Universe }
$endfigure

$box
$style[font-variant:small-caps;box-shadow: 7px 7px 5px rgba(200,200,200,0.3);border-radius:20px]
$caption(Note)[padding:0 2%;color:#4788B3;border-bottom:1px solid #4788B3;display:inline-block;]
$content(note)[padding:0 2%;font-size:120%;]{a slide has always one *content* element whereas, *headers*, *footers* and *sidebars* are optional.}
$endbox

## Canvas Theme

### Canvas container, available options and their setting

Presently, the **canvas** container has only one option:

+ `background`, default `radial-gradient(rgb(240, 240, 240), rgb(190, 190, 190))`.

$box
$style[font-variant:small-caps;box-shadow: 7px 7px 5px rgba(200,200,200,0.3);border-radius:20px]
$caption(Note)[padding:0 2%;color:#4788B3;border-bottom:1px solid #4788B3;display:inline-block;]
$content(note)[padding:0 2%;font-size:120%;]{The canvas options are applied to the **body** html element. As a consequence it can be customized only at the beginning of the presentation for all slides: an eventual slide's overriding theme cannot change the canvas options!}
$endbox

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
$content{Such a theme data can placed anywhere inside your markdown source, however it has sense to place it at the beginning, inside the presentantion _preamble_, that is just a convention rather than a physical part of the markdown document.}
$endnote

## Headings Theme

## Custom Selector Theme

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

### MaTiSSe.py Universe: the `element` option




### Why?
There are tons of markdown to html presentation tools. Why yet another presenter? 

Essentially, because other tools are designed for _hackers_ for producing short, essentially **not structured** presentation with cools effects. 

We also love html-based slides with cool effects, but we need more structured slides style for long, scientific presentation with support for *sections*, *subsections*, *TOC*, etc... 

MaTiSSe.py should:

* use simple markdown source to produce high-quality html-based presentation;
* support structured, long presentations:
    + presentation metadata; 
    + sections and subsections; 
    + toc; 
    + countdown timer; 
    + navigation-controls; 
    + ...
* support non structured, short and impressive presentations;
* support latex equations (both offline and online);
* support for easy theming;
* provide an output quality comparable to latex-beamer standard, but:
    + be faster than latex compilation;
    + be easier than latex programming;
* support cool effects as the modern _prezi_-like tools have.

### For whom?
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

Scientific researchers \(at least the brave ones\) are used to write presentation with _latex-beamer_. 

_LaTeX_ is great and the **beamer** class quality is incredible, however some drawbacks can be highlighted:

1. the compilation of an even small presentation can be _time consuming_;
2. latex _programming_ can be very inflexible frustrating the presenter;
3. the pdf output has great quality but it behaves not so well with multimedia content; 
4. it is rather complicated to introduce _prezi_-like effects.

MaTiSSe.py is designed for scientific researchers that want retain the best of _latex-beamer_ and _prezi_ worlds together. 

### How it works?
You write your presentation in markdown and MaTiSSe.py creates an impressive presentation even if you are a boring scientific researcher.

Inline equation $\frac{1}{2}$ example.

$$
x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}
$$

\begin{align*}
a=&1\\
\int_{a}^{b}\frac{c}{d}\,dx=&2
\end{align*}

### Requirements
MaTiSSe.py relies on other great python module for making its magic:

* Python 2.7+ or Python 3.x;
    + required modules:
        + `sys`;
        + `os`;
        + `argparse`;
        + `re`;
        + `yattag`;
        + `markdown`;
    + optional modules:
        + `multiprocessing`;
* Javascript:
    + `impress.js`;

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

```
# Section Title
```

### Subsections

A section is created by _h2 heading_ of markdown syntax, i.e.

```
## Subection Title
Subsection contents
### Slide1
Slide1 contents
### Slide2
Slide2 contents
...
```

### Slides

A section is created by _h3 heading_ of markdown syntax, i.e.

```fortran
function fo(in1)
integer, intent(IN):: in1
real::                fo
fo=real(in1)
return
endfunction fo
```

### Slides

```
### Slide Title
```
### Lists
* reveal.js;
* impress.js;
* latex;

### $overview
---slide
---theme_slide_global
data-scale       = 10
---endtheme_slide_global
---endslide
