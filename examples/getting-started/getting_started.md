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
max_time           = 60
dirs_to_copy       = ['images']
---endmetadata

$include(main_theme.md)

#titlepage[plain]

$box
$style[width:100%;height:35%;background:#4788B3;font-family:'Comic Sans MS', cursive, sans-serif;]
$content[color:white;text-align:center;]{
$title[display:block;font-size:200%;padding-top:2%;]
$subtitle[display:block;font-size:120%;padding-top:2%;] 
$logo[height:50px;] 
}
$endbox

$box
$style[width:100%;font-family:'Comic Sans MS', cursive, sans-serif;]
$content[text-align:center;]{
a presentation by $authors[display:block;font-size:150%]
$emails[display:block;font-size:90%;]
$affiliations[display:block;]
}
$endbox

$box
$style[width:100%;padding-top:2%;font-family:'Comic Sans MS', cursive, sans-serif;]
$content[text-align:center;color:#4788B3;]{
$conference[display:block;font-size:150%;]
$session[display:block;font-size:120%;]
$location[display:block;font-size:90%;text-align:right;padding-right:5%;padding-top:5%;]
$date[display:block;font-size:90%;text-align:right;padding-right:5%;]
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


### Prezi-effect
---slide
---theme_slide_global
background    = white
border-radius = 50%
data-offset   = 200
---endtheme_slide_global

---theme_slide_content
border-radius = 50%
padding       = 15% 20%
font-size     = 200%
---endtheme_slide_content

---theme_slide_header_1
active = False
---endtheme_slide_header_1

---theme_slide_footer_1
active = False
---endtheme_slide_footer_1

---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1
---endslide

The *elliptic* theme of this slide is made just

```lua
---theme_slide_global
border-radius = 50%
---endtheme_slide_global

---theme_slide_content
border-radius = 50%
---endtheme_slide_content
```

This is not so complicated, rigth?

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

Let me be clear: MaTiSSe.py is designed for **scientific researchers**, _at least the brave ones_, being used to write presentation with _LaTeX-beamer_ or other not *WYSIWYG* presentation makers. _LaTeX_ is great, but some drawbacks can be highlighted:

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

# Getting started

## Installation

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


## Usage

### How it works?
You write your presentation in markdown and MaTiSSe.py creates an impressive presentation even if you are a *boring scientific researcher*. MaTiSSe.py is a not-WYSISWYG command line, CLI, tool. Printing the main help message:
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

## MaTiSSe.py flavored markdown syntax

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
$content{
A slide has always one *content* element whereas, *headers*, *footers* and *sidebars* are optional.

The headers, footers and sidebars are designed to be *theme-containers* rather than directly accessible containers. This means that the contents of these slide elements is defined by the theme setting, whereas the *content* element is the one that is directly accessed and where you put your slide contents. 
}
$endnote
 
### Slide: how write it?
Once you have structured your talk into section/subsections it is time to write the slide contents! As aforementioned a slide starts with:

```md
### Slide title
...
```
The `Slide title` is stored by MaTiSSe.py into the *metadata*, see the following, and can be handled as a local-to-the-slide variable. What follows the slide title is actually the slide contents: these data is place into the slide *content* element. 

$note
$content{
Into the slide content you can place any valid markdown source. 

Note that the markdown used by MaTiSSe.py is an extended version of the [http://daringfireball.net/projects/markdown/](http://daringfireball.net/projects/markdown/), that is very similar to the one used by github, the so called [GitHub Flavored Markdown](https://help.github.com/articles/github-flavored-markdown/). 

Indeed, the syntax supported by MaTiSSe.py is even more extended with respect the github flavored syntax: MaTiSSe.py supports latex equations and some specaial environments. 

The markdown source is parsed by means of **markdown** python module: for more informations on the supported syntax see [https://pythonhosted.org/Markdown/](https://pythonhosted.org/Markdown/).
}
$endnote

The first extension to the standard markdown syntax is the **metadata** objects...

### Presentation metadata

For long scientific presentation it is often useful to define some (meta)data in order to reuse them inside the presentation itself. Such data are defined into MaTiSSe.py as *metadata*. You can define the presentation metadata anywhere into your markdown source, however it has sense to place it at the beginning, inside the presentation _preamble_, that is just a convention rather than a physical part of the markdown document. The available metadata are:

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
$note
$content{
All metadata values are treated as string except the one with `[]` brackets that are list of strings. To split long metadata definitions use the symbol `&&` as line continuation.
}
$endnote

### Presentation metadata (continued)

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
affiliations       = ['NERD Laboratory, The World Most Uncool Research Center',&&
                      'LOST Institute, Missed People Research Institute']
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

### Presentation metadata (continued)
Besides the presentation metada above described, that are the ones whose value must be set by the user, there are many other metadata whose values are automatically computed by MaTiSSe.py. The following is a not complete list of such metadata:

+ *sectiontitle*;
+ *sectionnumber*;
+ *subsectiontitle*;
+ *subsectionnumber*;
+ *slidetitle*;
+ *slidenumber*;
+ *total_slides_number*;
+ *toc*.

$note
$content{
The slide you are reading is composed using such metadata: the header contains the *slidetitle*, the right sidebar contains the *toc*, while the footer contains the current *slidenumber* and *total_slides_number* among other things.
Such metadata can be directly used also inside the main content slide and not only into the other slide containers. Just use the `$metadata[style]` notation, where the `[style]` is the css style for rendering the metadata value and it is optional.
}
$endnote
For example inserting 
```
$authors[color:#4788B3;]
```
into the slide content will be replaced by $authors[color:#4788B3;]

### Code listings
The code listings is accomplished very similarly to the github flavored markdown approach. 

Just use fenced code blocks or in-line codes. 

$note
$content{
Remember that the syntax highlighting is achieved by means of [highlight.js](https://highlightjs.org/): only the languages supported by `highlight.js` are supported.
}
$endnote

For example:

```python
#!/usr/bin/env python
"""
MaTiSSe.py, Markdown To Impressive Scientific Slides
"""
__appname__ = "MaTiSSe.py"
__description__ = "MaTiSSe.py, Markdown To Impressive Scientific Slides"
__version__ = "v0.0.1"
__author__ = "Stefano Zaghi"
__author_email__ = "stefano.zaghi@gmail.com"
__license__ = "GNU General Public License v3 (GPLv3)"
__url__ = "https://github.com/szaghi/MaTiSSe"
```

$note
$content{
Presently the code blocks defined by simple indentation, as the original markdown [definition](http://daringfireball.net/projects/markdown/syntax#precode) is not completely supported.
}
$endnote

### LaTeX equations
For scientific contents equations environments are mandatory. 

The *de facto* standard of equations typesetting is LaTeX. 

##### MaTiSSe.py supports LaTeX equations! 

Just type your equations as you do into your LaTeX source:

```md
### Equations, equations, equations... LaTeX is supported!

Just type your equations as you do into your LaTeX sources:


$$
x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}
$$
```
and you get:
$$
x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}
$$
 
### Special Environments
As aforementioned, MaTiSSe.py supports some special environments as helpers for some special contents handling. Presently the special environments supported are:

+ `Columns` environment;
+ `Box` environment, that has 3 sub-class environments for more specialized contents:
    * `Figure` environment;
    * `Table` environment;
    * `Note` environment;

$note
$content{
The `Columns` environment can contain any other data, whereas the `Box`-like environments can contain any valid markdown source, the metadata, their own specific contents, etc... but they cannot contain the `Columns` environment. 

There is a hierarchy:

+ `Columns` environment can contain anything, also other envs;
    * `Box`-like environments can contain anything, except the `Columns` one.

}
$endnote

Let us dive into these environments... 

### The Columns environment
It is often useful to subdivide the contents into columns, e.g. to place comments aside figures. 

MaTiSSe.py provides an environment for such a contents layout. The syntax is very simple:
```bash
$columns
$column[column1_options]
column1_contents
$column[column2_options]
column2_contents
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
The column *options* can contain any css style options, however the options *display:block;float:left;* are automatically added. Moreover, the user should always specify the *width* option for avoiding unpredictable output.
}
$endnote
$endcolumns
 
In case the column style options are completely omitted MaTiSSe.py defines the width of each column as `100/columns_numer%` by default for having an uniform spaced columns environment.

### Box environment
The generic *box* is designed to contains any contents you want to be rendered with a different theme with respect other paragraph. The syntax is the following:

```md
$box
$style[style_options]
$caption(caption_type)[caption_options]{caption}
$content(content_type)[content_options]{content}
$endbox
```
where:

+ <code>$box</code> and <code>$endbox</code> are the tags defining the box environment;
+ `$style[style_options]` defines the style of the whole box; this is optional and can be omitted; the `style_options` are any valid css style definitions;
+ `$caption(caption_type)[caption_options]{caption}` defines the caption of the box that can be styled differently from the main box content and it is optional; the `(caption_type)` defines caption prefixing *class*, e.g. *Fig.* for figures, and it is itself optional: any sentences are valid; to disable the printing of the prefixing class use `$caption(none)...`; the `[caption_options]` defines the style options of the only caption: they are any valid css definitions; the `{caption}` defines the caption text and it must be present if `$caption` is defined;
+ `$content(content_type)[content_options]{content}` is not optional: it defines the box's content; the `(content_type)` defines defines the type of the content, 'figure', 'table', 'note' and 'box' for generic environments, and it is itself optional; the `[content_options]` defines the style options of the only content: they are any valid css definitions; the `{content}` defines the content data;

### Box environment (continued)

Consider the following code:

```md
### Box environment example

$box
$style[background:rgb(100,100,100);]
$caption(Mybox)[font-size:90%;color:white;]{An example of a generic Box}
$content[font-size:120%;color:white;]{This box has a grey background with white colored text. The caption has a 90% with respect the slide content font-size, whereas the box contents itself has a 120% font-size.}
$endbox
```

This example defines a box having a grey background with white colored text:

$box
$style[background:rgb(100,100,100);]
$caption(Mybox)[font-size:90%;color:white;text-align:center;]{An example of a generic Box}
$content[font-size:120%;color:white;]{This box has a grey background with white colored text. The caption has a 90% with respect the slide content font-size, whereas the box contents itself has a 120% font-size.}
$endbox

Note that the themes of box environments can be defined, as all other theme elements, once for all into the preamble in order to not have to repeat the styling options for each box. The syntax for defining the boxes styles is commented into the theming section in the following. 

$note
$content{
Note that the caption of the example as  *Mybox 4*: the numeration is automatic, in fact I have used other 3 boxes for the titlepage of this talk: this happens for all the box-like envs where the numeration is automatically handled by MaTiSSe.py.
}
$endnote

### Note environment
The *note* environment is a subclass of box one that is specialized for rendering notes. The syntax is the following:
```md
$note
$style[style_options]
$caption[caption_options]{caption}
$content[content_options]{content}
$endnote
```
where the elements are the same of box environment, but:

+ the `content_type` and `caption_type` are automatically set to `note` and `Note` respectively; anyhow they can be still specified inside the <code>$note/$endnote</code> environment;
+ no matter the order of `$caption`/`$content` statements, the caption is always placed above the content.

You have seen this env on many preceding slides. Consider the following code:
```md
$note
$content{
As all other box subclass, the themes of note environments can be defined once for all into the preamble in order to not have to repeat the styling options for each note.
}
$endnote
```
becomes
$note
$content{
As all other box subclass, the themes of note environments can be defined once for all into the preamble in order to not have to repeat the styling options for each note.
}
$endnote

### Figure environment
The *figure* environment is a subclass of box one that is specialized for rendering figures. The syntax is the following:
```md
$figure
$style[style_options]
$caption[caption_options]{caption}
$content[content_options]{content}
$endfigure
```
where the elements are the same of box environment, but:

+ the `content_type` and `caption_type` are automatically set to `figure` and `Figure` respectively; anyhow they can be still specified inside the <code>$figure/$endfigure</code> environment;
+ the `content` must be the (relative to the root) path of an external figure file;
+ no matter the order of `$caption`/`$content` statements, the caption is always placed below the content.

You have seen this env on some preceding slides. Consider the following code:
```md
$figure
$content[padding:1% 5%;width:90%;box-shadow: 7px 7px 5px rgba(200,200,200,0.3);border-radius:25px]{images/matisse-universe-no_bg.png}
$caption(none){MaTiSSe.py **Universe**}
$endfigure
```
becomes => ...

### Figure environment (continued)
$figure
$content[padding:1% 5%;width:90%;box-shadow: 7px 7px 5px rgba(200,200,200,0.3);border-radius:25px]{images/matisse-universe-no_bg.png}
$caption(none){MaTiSSe.py **Universe**}
$endfigure

Note that, as all other box subclass, the themes of figure environments can be defined once for all into the preamble in order to not have to repeat the styling options for each figure.
 
### Titlepage
Titlepage is indeed a special slide rather than a special environment. It is designed to be a special slide where is extremely easy to have a plain slide theme in order to build a special slide. Indeed all slide are easily customizable, as you seen in the following, but a titlepage starts from a plain theme rather than the default one. To define a titlepage the syntax is:

```md
#titlepage[plain]
```
where `[plain]` is optional and if defined set the titlepage slide theme to the default plain, while if it is not defined the titlepage slide adopts the same theme as you have defined for other slides. The slide title of a titlepage is automatically set to a null string thus it has no sense to use the corresponding metadata. On the contrary all other metadata can be used within a titlepage. 

The titlepage of this presentation has been made with a code similar to the following:

```md
#titlepage[plain]
$box
$style[width:100%;height:35%;background:#4788B3;font-family:'Comic Sans MS', cursive, sans-serif;]
$content[color:white;text-align:center;]{
$title[font-size:200%;padding-top:2%;]
$subtitle[font-size:120%;padding-top:2%;] 
$logo[height:50px;] 
}
$endbox
...
```

### Including external files
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

$note
$content{
The `$include` statements are parsed one time at the beginning of the MaTiSSe.py execution, therefore no recursive inclusions are admitted.
}
$endnote
 
Now it is time to talk about theme customization... 

Do you are interested to learn how complex was to set the theme of this presentation? Continue to read!

# Customize the Themes

## MaTiSSe.py Universe

### MaTiSSe.py Universe (again)
I known, you have just seen the universe of MaTiSSe.py, this is just a recall... The customizable theme elements are:

* **presentation** with its own options, having:
    + one **canvas** with its own options over wich the slides are rendered:
    + N **slide**(s) with their own options; each slide has: 
        * $N_H$ **headers**, with $N_H \in [0,\infty]$; 
        * $N_F$ **footers**, with $N_F \in [0,\infty]$; 
        * $N_L$ left **sidebars**, with $N_L \in [0,\infty]$; 
        * $N_R$ right **sidebars**, with $N_R \in [0,\infty]$; 
        * 1 main **content**.

$figure
$content[padding:1% 5%;width:64%;box-shadow: 7px 7px 5px rgba(200,200,200,0.3);border-radius:25px]{images/matisse-universe-no_bg.png}
$caption(none){MaTiSSe.py **Universe**}
$endfigure

In the following subsections we will see how to customize each element.

## Presentation-level Theme

### Canvas container, available options and their setting

Presently, the **canvas** container has only one default option:

+ `background`, default `radial-gradient(rgb(240, 240, 240), rgb(190, 190, 190))`.

$note
$content{The canvas options are applied to the **body** html element. As a consequence it can be customized only at the beginning of the presentation for all slides: an eventual slide overriding theme cannot change the canvas options!}
$endnote

You can define other css options, however the background seems to be only with a sense for a canvas container.

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

### Headings and Custom Selector Themes

Besides the main presentation theme, you can set the default theme of headings (h1,h2,...,h6) and you can specify the theme of **custom selectors** for customizing special elements of the presentation that are not part of the main theme, e.g. the blocks of code. 

$note
$content{Both headings and custom selectors can be re-defined by the slide overriding theme, read the following.}
$endnote

### Headings, available options

The **headings** themes, that are 6, have the following default _user_ options:

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

The **custom** selector has the following default _user_ options:

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

### Custom Selector, setting options (continued)
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

### TOC Theme
Table of Contents, TOC, is a particular metadata and its handling is very different from any other metatada. Consequently TOC has its own special theme that can be customized by the following syntax:

```lua
 ---theme_toc
option_name1 = option_value1
option_name2 = option_value2
...
---endtheme_toc
```

As common for MaTiSSe.py the `option_name = option_value` pairs are valid css style options. Into the TOC it is possible to emphasize the current section/subsection/slide as it has been done for this presentation. The syntax to define an emphasized current position into the TOC is:

```lua
---theme_section_emph_toc
option_name1 = option_value1
...
---endtheme_section_emph_toc

---theme_subsection_emph_toc
option_name1 = option_value1
...
---endtheme_subsection_emph_toc

---theme_slide_emph_toc
option_name1 = option_value1
...
---endtheme_slide_emph_toc
```
### Box-like environments themes
To customize a *box-like* environments the syntax is the following

```lua
---theme_box
style   = style_options
caption = caption_options
content = content_options
---endtheme_box
```
where `style/caption/content_options` are valid css style.

$note
$content{Such a theme data can placed anywhere inside your markdown source, however it has sense to place it at the beginning, inside the presentation _preamble_, that is just a convention rather than a physical part of the markdown document.}
$endnote

For example the above note uses the following theme:

```lua
---theme_note
style   = display:inline-block;font-variant:small-caps;box-shadow: 7px 7px 5px rgba(200,200,200,0.3);border-radius:20px
caption = padding:0 2%;color:#4788B3;border-bottom:1px solid #4788B3;display:inline-block;
content = padding:0 2%;font-size:120%;
---endtheme_note 
```
 
### Presentation-level Theme, an example

This presentation uses:

```lua
---theme_canvas
background = radial-gradient(rgb(240, 240, 240), rgb(110, 110, 110))
---endtheme_canvas

---theme_toc
font-variant = small-caps
---endtheme_toc

---theme_section_emph_toc
border        = 1px solid #4788B3
border-radius = 5px
---endtheme_section_emph_toc

---theme_subsection_emph_toc
border        = 1px solid #4788B3
border-radius = 5px
---endtheme_subsection_emph_toc 
---theme_figure
style   = font-variant:small-caps;text-align:center;
caption = font-size:80%;color:#4788B3;
---endtheme_figure

---theme_note
style   = display:inline-block;font-variant:small-caps;box-shadow: 7px 7px 5px rgba(200,200,200,0.3);border-radius:20px
caption = padding:0 2%;color:#4788B3;border-bottom:1px solid #4788B3;display:inline-block;
content = padding:0 2%;font-size:120%;
---endtheme_note 
```

## Slide-level Theme

### Slide container, available options

The **slide** container has the following default _user_ options:

+ `width           `, default `900px`;
+ `height          `, default `700px`;
+ `background      `, default `white`;
+ `border          `, default `0`;
+ `border-radius   `, default `0 0 0 0`;
+ `color           `, default `black`;
+ `font            `;
+ `font-size       `, default `100%`;
+ `font-family     `, default `Open Sans, Arial, sans-serif`;
+ `slide-transition`, default `horizontal`;
+ `data-scale      `, default `1`;
+ `data-rotate     `, default `0`;
+ `data-rotate-x   `, default `0`;
+ `data-rotate-y   `, default `0`;
+ `data-rotate-z   `, default `0`;
+ `data-x          `, default `0`;
+ `data-y          `, default `0`;
+ `data-z          `, default `0`.
+ `data-offset     `, default `1`.

The most part of options are standard `CSS` options. However some exceptions are present. Before read about them, we discuss how set the slide options.

$note
$content{
For all the slide containers the user can set any valid css style options, not only the default ones.
}
$endnote

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
To be written...

### Slide Header container, available options

The *header* element is designed to render data in a _single row_ above the main content rather than wrap the content into multi-lines.

Header element has the following default _user_ options:

+ `display      `, default `block`;
+ `width        `, default `100%`;
+ `height       `, default `100%`, preferably expressed in percent _of the slide height_;
+ `padding      `, default `0`;
+ `font-size    `, default `100%`;
+ `font-family  `, default `Open Sans, Arial, sans-serif`;
+ `overflow     `, default `hidden`.
+ `metadata     `, a list of objects to be inserted, e.g. slide-title, presentation-title, presentation-logo,etc...;
+ `active       `, default `True`.

The most part of options are standard `CSS` options. The special thing is the `metadata` option... but let it to the following!

Note that the `width` is automatically set to `100%` and should not be customized from users.

### Slide Header container, setting options

To customize the options of header n. _N_ the syntax is the following
```lua
---theme_slide_header_N
option_name1 = option_value1
option_name2 = option_value2
...
---endtheme_slide_header_N
```
where `option_name` is one of the previously cited options, e.g. `height`, `display`, etc..., while `option_value` is its value. Each header is indicated by its own number: the numeration can be not strictly consecutive, e.g. you can start with header 2 instead of header 1. However, the insertion follows the number order, thus header 1, if present, is inserted **before** header 2. 

The header of the slide you are reading is made by
```lua
---theme_slide_header_1
height        = 6%
background    = #4788B3
color         = white
border-radius = 10px 10px 0 0
padding       = 1%
metadata      = [['slidetitle','font-variant:small-caps;font-size:180%;padding:2%'],&&
                 ['logo','float:right;height:90%;']]
---endtheme_slide_header_1
```
### Slide Footer container, available options

The *footer* element is designed to render data in a _single row_ below the main content rather than wrap the content into multi-lines.

Footer element has the following default _user_ options:

+ `display      `, default `block`;
+ `width        `, default `100%`;
+ `height       `, default `100%`, preferably expressed in percent _of the slide height_;
+ `padding      `, default `0`;
+ `font-size    `, default `100%`;
+ `font-family  `, default `Open Sans, Arial, sans-serif`;
+ `overflow     `, default `hidden`.
+ `metadata     `, a list of objects to be inserted, e.g. slide-title, presentation-title, presentation-logo,etc...;
+ `active       `, default `True`.

The most part of options are standard `CSS` options. The special thing is the `metadata` option... but let it to the following!

Note that the `width` is automatically set to `100%` and should not be customized from users.

### Slide Footer container, setting options

To customize the options of footer n. _N_ the syntax is the following
```lua
---theme_slide_footer_N
option_name1 = option_value1
option_name2 = option_value2
...
---endtheme_slide_footer_N
```
where `option_name` is one of the previously cited options, e.g. `height`, `display`, etc..., while `option_value` is its value. Each footer is indicated by its own number: the numeration can be not strictly consecutive, e.g. you can start with footer 2 instead of footer 1. However, the insertion follows the number order, thus footer 1, if present, is inserted **before** footer 2. 

The footer of the slide you are reading is made by
```lua
---theme_slide_footer_1
height     = 6%
padding    = 1% 2%
background = #86B2CF
color      = white
metadata   = [['timer','controls;font-size:70%;font-variant:small-caps;float:right'],&&
              ['total_slides_number','float:right;padding:0 1%;'],                   &&
              ['|custom| of ','float:right;'],                                       &&
              ['slidenumber','float:right;padding:0 1%;'],                           &&
              ['|custom|slide ','float:right;']]
---endtheme_slide_footer_1
```

### Slide Sidebar container, available options

The *sidebar* element is designed to render data in a _single column_ aside, left or right, the main content.

Sidebar element has the following default _user_ options:


+ `display      `, default `block`;
+ `width        `, default `100%`, preferably expressed in percent _of the slide height_;
+ `height       `, default `100%`;
+ `padding      `, default `0`;
+ `font-size    `, default `100%`;
+ `font-family  `, default `Open Sans, Arial, sans-serif`;
+ `overflow     `, default `hidden`.
+ `metadata     `, a list of objects to be inserted, e.g. slide-title, presentation-title, presentation-logo,etc...;
+ `active       `, default `True`.

The most part of options are standard `CSS` options. The special thing is the `metadata` option... but let it to the following!

Note that the `height` is automatically set to `100%` and should not be customized from users.

### Slide Sidebar container, setting options

To customize the options of sidebar n. _N_ the syntax is the following
```lua
---theme_slide_sidebar_N
option_name1 = option_value1
option_name2 = option_value2
...
---endtheme_slide_sidebar_N
```
where `option_name` is one of the previously cited options, e.g. `width`, `display`, etc..., while `option_value` is its value. Each sidebar is indicated by its own number: the numeration can be not strictly consecutive, e.g. you can start with sidebar 2 instead of sidebar 1. However, the insertion follows the number order and the left to right order, thus left sidebars are inserted before right one and sidebar 1, if present, is inserted **before** sidebar 2. 

The sidebar of the slide you are reading is made by
```lua
---theme_slide_sidebar_1
position      = R
width         = 20%
padding       = 1% 2%
background    = linear-gradient(#4788B3,#86B2CF)
color         = white
border-radius = 0
metadata      = [['title','font-weight:bold;font-variant:small-caps;font-size:105%;display:inline-block'],                                          &&
                 ['authors','font-variant:small-caps;font-size:90%;display:inline-block'],                                                          &&
                 ['affiliations','margin-top:4%;margin-bottom:10%;font-variant:small-caps;font-size:70%;white-space:pre-wrap;display:inline-block'],&&
                 ['toc','font-size:70%;',2]] 
---endtheme_slide_sidebar_1
```

### Slide Content container, available options

The *content* element is designed to render the main slide contents.

Content element has the following default _user_ options:

+ `display      `, default `block`;
+ `width        `, default `100%`;
+ `height       `, default `100%`;
+ `padding      `, default `0`;
+ `font-size    `, default `100%`;
+ `font-family  `, default `Open Sans, Arial, sans-serif`;
+ `overflow     `, default `hidden`.

All are are standard `CSS` options.

Note that the `height` and `width` are automatically computed by MaTiSSe.py accordingly to the dimensions of headers, footers and sidebars, thus it has no sense for the user to set them.

### Slide Content container, setting options

To customize the options of content the syntax is the following
```lua
---theme_slide_content
option_name1 = option_value1
option_name2 = option_value2
...
---endtheme_slide_content
```
where `option_name` is one of the previously cited options, e.g. `display`, `padding`, etc..., while `option_value` is its value.

The content of the slide you are reading is made by
```lua
---theme_slide_content
background    = white
color         = rgb(102,102,102)
padding       = 1%
---endtheme_slide_content
```
 
### Slide-level Theme, an example

This presentation uses:

```lua
---theme_slide_global
width            = 900px
height           = 700px
border-radius    = 10px
background       = green
color            = rgb(102,102,102)
font-size        = 100%
slide-transition = horizontal
data-offset      = 200
---endtheme_slide_global

---theme_slide_content
background    = white
color         = rgb(102,102,102)
padding       = 1%
---endtheme_slide_content

---theme_slide_header_1
height        = 6%
padding       = 1% 2%
background    = #4788B3
color         = white
border-radius = 10px 10px 0 0
metadata      = [['slidetitle','font-variant:small-caps;font-size:150%;'],&&
                 ['logo','float:right;height:100%;']]
---endtheme_slide_header_1
```

### Slide-level Theme, an example (continued)
```lua
---theme_slide_footer_1
height     = 6%
padding    = 1% 2%
background = #86B2CF
color      = white
metadata   = [['timer','controls;font-size:70%;font-variant:small-caps;float:right'],&&
              ['total_slides_number','float:right;padding:0 1%;'],                   &&
              ['|custom| of ','float:right;'],                                       &&
              ['slidenumber','float:right;padding:0 1%;'],                           &&
              ['|custom|slide ','float:right;']]
---endtheme_slide_footer_1

---theme_slide_sidebar_1
position      = R
width         = 20%
padding       = 1% 2%
background    = linear-gradient(#4788B3,#86B2CF)
color         = white
border-radius = 0
metadata      = [['title','font-weight:bold;font-variant:small-caps;font-size:105%;display:inline-block'],                                          &&
                 ['authors','font-variant:small-caps;font-size:90%;display:inline-block'],                                                          &&
                 ['affiliations','margin-top:4%;margin-bottom:10%;font-variant:small-caps;font-size:70%;white-space:pre-wrap;display:inline-block'],&&
                 ['toc','font-size:70%;',2]]
---endtheme_slide_sidebar_1
```

### Metadata option

In the previous slides we learn that `metadata` can be used inside the theme definition. Considering a generic theme element, the syntax is the following:

```lua
metadata = [list_of_metadata]
```
where the *list_of_metadata* is the list of the metadata used into the theme element. Each metadata can be styled or it can inherit the style from its element container. For example:

```lua
metadata = ['slidetile', &&
           ['logo','float:right;']]
```
defines 2 metadata:

1. `'slidetitle'` that ha no special style;
2. `['logo','float:right;']` that has its own special style, i.e. `float:right`.

$note
$content{
To define a styled metadata use a list where the second element is the css style.
}
$endnote

The `toc` metadata is a special case. If styled it can accept a third optional value:

```lua
metadata = [ ['toc','float:right;','2'] ]
```
This third optional value, `2`, indicates the TOC depth.

## Slide-Overriding theme 

### Changing the Slide Theme on-the-fly
A very nice MaTiSSe.py feature is the possibility to define a theme locally to each slide, the so called *slide overtheme*, and change the theme **on-the-fly**. The syntax is the following:

```lua
### Slide Title
---slide
any valid slide-level theme
---endslide 
```
just put the slide themes into a <code>---slide/---endslide</code> environment after the slide title and the slide will be rendered with its own theme. 

If you do not believe me, look the following slide!

### Changing the Slide Theme on-the-fly (continued)
---slide
---theme_slide_global
slide-transition = diagonal
data-z           = -2000
data-scale       = 2
data-rotate      = 90
data-rotate-y    = 30
---endtheme_slide_global

---theme_slide_content
font-family = 'Comic Sans MS', cursive, sans-serif
---endtheme_slide_content

---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1
---endslide 

##### Where is the right sidebar?
##### Why the font family is comic-like?
##### Why the slide has been rotated, scaled...?

Because this slide has the following overtheme:

```lua
---slide

---theme_slide_global
slide-transition = diagonal
data-z           = -2000
data-scale       = 2
data-rotate      = 90
data-rotate-y    = 30
---endtheme_slide_global

---theme_slide_content
font-family = 'Comic Sans MS', cursive, sans-serif
---endtheme_slide_content

---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1 

---endslide 
``` 

# Theme Example

## Sapienza, University of Rome, theme

### Sapienza Theme
---slide
---theme_slide_global
data-offset = 200
background  = white
---endtheme_slide_global

---theme_slide_header_1
background = white
color      = #822433
metadata   = [['slidetitle','font-variant:small-caps;font-size:150%;']]
---endtheme_slide_header_1

---theme_slide_footer_1
height     = 3%
width      = 90%
float      = right
background = #822433
metadata   = []
---endtheme_slide_footer_1

---theme_slide_footer_2
height     = 6%
padding    = 1% 2%
background = #822433
color      = white
metadata   = [['title','padding:0 1%;'],                           &&
              ['date','padding:0 1%;'],                            &&
              ['total_slides_number','float:right;padding:0 1%;'], &&
              ['|custom| of ','float:right;'],                     &&
              ['slidenumber','float:right;padding:0 1%;'],         &&
              ['|custom|slide ','float:right;']]
---endtheme_slide_footer_2
 
---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1
---endslide 
 
Slide Overtheme definition: 

```lua
---slide 
---theme_slide_global
data-offset = 200
background  = white
---endtheme_slide_global

---theme_slide_header_1
background = white
color      = #822433
metadata   = [['slidetitle','font-variant:small-caps;font-size:150%;']]
---endtheme_slide_header_1

---theme_slide_footer_1
height     = 3%
width      = 90%
float      = right
background = #822433
metadata   = []
---endtheme_slide_footer_1

```

### Sapienza Theme (continued)
---slide
---theme_slide_global
data-offset = 200
background  = white
---endtheme_slide_global

---theme_slide_header_1
background = white
color      = #822433
metadata   = [['slidetitle','font-variant:small-caps;font-size:150%;']]
---endtheme_slide_header_1

---theme_slide_footer_1
height     = 3%
width      = 90%
float      = right
background = #822433
metadata   = []
---endtheme_slide_footer_1

---theme_slide_footer_2
height     = 6%
padding    = 1% 2%
background = #822433
color      = white
metadata   = [['title','padding:0 1%;'],                           &&
              ['date','padding:0 1%;'],                            &&
              ['total_slides_number','float:right;padding:0 1%;'], &&
              ['|custom| of ','float:right;'],                     &&
              ['slidenumber','float:right;padding:0 1%;'],         &&
              ['|custom|slide ','float:right;']]
---endtheme_slide_footer_2
 
---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1
---endslide 
 
```lua
---theme_slide_footer_2
height     = 6%
padding    = 1% 2%
background = #822433
color      = white
metadata   = [['title','padding:0 1%;'],                           &&
              ['date','padding:0 1%;'],                            &&
              ['total_slides_number','float:right;padding:0 1%;'], &&
              ['|custom| of ','float:right;'],                     &&
              ['slidenumber','float:right;padding:0 1%;'],         &&
              ['|custom|slide ','float:right;']]
---endtheme_slide_footer_2
 
---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1 
---endslide 
```

## Beamer Themes

### Beamer Themes

MaTiSSe.py has been greatly inspired by LaTeX-Beamer class. 

###### MaTiSSe.py author has used LaTeX-Beamer for many years and truly loves it. 

LaTeX-Beamer is widely used in the scientific community. Therefore MaTiSSe.py *should* offer support for LaTeX-Beamer community. In particular the reproduction of LaTeX-Beamer themes should be as easy as possible. 

In the following slide we try to reproduce some of the most used LaTeX-Beamer theme.

For each theme the **overtheme** definition is reported as code listings.

$note
$content{
Into each listing the tags <code>---slide</code>/<code>---endslide</code> are omitted because it is implicitly assumed that the listing can be referred to both *main* and *over* slide theme.
}
$endnote

### Bergen
---slide

---theme_slide_header_1
width         = 75%
height        = 10%
background    = white
color         = black
float         = right
border-radius = 0
metadata      = [['slidetitle','font-size:150%;']]
---endtheme_slide_header_1 
 
---theme_slide_footer_1
active = False
---endtheme_slide_footer_1 
 
---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1 
 
---theme_slide_sidebar_2
position   = L
width      = 25%
background = #272586
color      = white
min-height = 100%
metadata   = [['toc','font-size:120%;text-align:right;line-height:500%;padding:30% 5%;float:right',1]]
---endtheme_slide_sidebar_2 

---endslide

Theme definition:
```lua
---theme_slide_header_1
width         = 75%
height        = 10%
background    = white
color         = black
float         = right
metadata      = [['slidetitle','font-size:150%;']]
---endtheme_slide_header_1 
 
---theme_slide_sidebar_1
position   = L
width      = 25%
background = #272586
color      = white
min-height = 100%
metadata   = [['toc','font-size:120%;text-align:right;line-height:500%;padding:30% 5%;float:right',1]]
---endtheme_slide_sidebar_1 
```

### Madrid
---slide

---theme_slide_header_1
height        = 10%
background    = #3333B3
metadata      = [['slidetitle','font-size:150%;']]
---endtheme_slide_header_1 

---theme_slide_footer_1
height     = 6%
background = #3333B3
padding    = 0
metadata   = [['authors_short','float:left;height:100%;width:20%;padding:1% 2%;background: #191959;'],       &&
              ['title','float:left;font-size:80%;height:100%;width:35%;padding:1% 2%;background: #262686;'], &&
              ['date','float:left;font-size:80%;height:100%;width:35%;padding:1% 2%;background: #3333B3;'],  &&
              ['total_slides_number','float:right;padding:0 1%;'],                                           &&
              ['|custom| / ','float:right;'],                                                                &&
              ['slidenumber','float:right;padding:0 1%;']]
---endtheme_slide_footer_1 
 
---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1  

---endslide

Theme definition:
```lua
---theme_slide_header_1
height        = 10%
background    = #3333B3
metadata      = [['slidetitle','font-size:150%;']]
---endtheme_slide_header_1 

---theme_slide_footer_1
height     = 6%
background = #3333B3
padding    = 0
metadata   = [['authors_short','float:left;height:100%;width:20%;padding:1% 2%;background: #191959;'],       &&
              ['title','float:left;font-size:80%;height:100%;width:35%;padding:1% 2%;background: #262686;'], &&
              ['date','float:left;font-size:80%;height:100%;width:35%;padding:1% 2%;background: #3333B3;'],  &&
              ['total_slides_number','float:right;padding:0 1%;'],                                           &&
              ['|custom| / ','float:right;'],                                                                &&
              ['slidenumber','float:right;padding:0 1%;']]
---endtheme_slide_footer_1  
```
 
### Antibes
---slide

---theme_slide_header_1
height        = 4%
background    = black
color         = white
padding       = 1% 2%
metadata      = [['title','font-size:90%;']]
---endtheme_slide_header_1 

 ---theme_slide_header_2
height        = 4%
background    = #191959
color         = white
padding       = 1% 4%
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['sectiontitle','font-size:90%;']]
---endtheme_slide_header_2

 ---theme_slide_header_3
height        = 4%
background    = #262686
color         = white
padding       = 1% 6%
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['subsectiontitle','font-size:90%;']]
---endtheme_slide_header_3

---theme_slide_header_4
height        = 6%
background    = #3333B2
color         = white
padding       = 1% 2%
metadata      = [['slidetitle','font-size:160%;']]
---endtheme_slide_header_4

---theme_slide_footer_1
active = False
---endtheme_slide_footer_1 
 
---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1

---endslide

Theme definition:
```lua
---theme_slide_header_1
height        = 3%
background    = black
color         = white
padding       = 1% 2%
metadata      = [['title','font-size:90%;']]
---endtheme_slide_header_1 

 ---theme_slide_header_2
height        = 3%
background    = #191959
color         = white
padding       = 1% 4%
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['sectiontitle','font-size:90%;']]
---endtheme_slide_header_2

```
### Antibes (continued)
---slide

---theme_slide_header_1
height        = 4%
background    = black
color         = white
padding       = 1% 2%
metadata      = [['title','font-size:90%;']]
---endtheme_slide_header_1 

---theme_slide_header_2
height        = 4%
background    = #191959
color         = white
padding       = 1% 4%
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['sectiontitle','font-size:90%;']]
---endtheme_slide_header_2

---theme_slide_header_3
height        = 4%
background    = #262686
color         = white
padding       = 1% 6%
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['subsectiontitle','font-size:90%;']]
---endtheme_slide_header_3

---theme_slide_header_4
height        = 6%
background    = #3333B2
color         = white
padding       = 1% 2%
metadata      = [['slidetitle','font-size:160%;']]
---endtheme_slide_header_4

---theme_slide_footer_1
active = False
---endtheme_slide_footer_1 
 
---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1

---endslide

Theme definition:
```lua
---theme_slide_header_3
height        = 3%
background    = #262686
color         = white
padding       = 1% 6%
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['subsectiontitle','font-size:90%;']]
---endtheme_slide_header_3

 ---theme_slide_header_4
height        = 7%
background    = #3333B2
color         = white
padding       = 1% 2%
metadata      = [['slidetitle','font-size:180%;']]
---endtheme_slide_header_4
``` 

### Montpellier
---slide

---theme_slide_header_1
height        = 6%
background    = white
color         = black
padding       = 1% 2%
border-top    = 8px solid #9999D9
border-radius = 0
metadata      = [['title','font-size:90%;']]
---endtheme_slide_header_1 

---theme_slide_header_2
height        = 6%
background    = white
color         = #9999D9
padding       = 1% 4%
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['sectiontitle','font-size:90%;']]
---endtheme_slide_header_2

---theme_slide_header_3
height        = 6%
background    = white
color         = #9999D9
padding       = 1% 6%
border-bottom = 8px solid #9999D9
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['subsectiontitle','font-size:90%;']]
---endtheme_slide_header_3

---theme_slide_header_4
height        = 8%
background    = white
color         = #9999D9
padding       = 1% 2%
metadata      = [['slidetitle','font-size:160%;']]
---endtheme_slide_header_4

---theme_slide_footer_1
active = False
---endtheme_slide_footer_1 
 
---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1

---endslide

Theme definition:
```lua
---theme_slide_header_1
height        = 6%
background    = white
color         = black
padding       = 1% 2%
border-top    = 8px solid #9999D9
border-radius = 0
metadata      = [['title','font-size:90%;']]
---endtheme_slide_header_1 

---theme_slide_header_2
height        = 6%
background    = white
color         = #9999D9
padding       = 1% 4%
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['sectiontitle','font-size:90%;']]
---endtheme_slide_header_2
``` 
 
### Montpellier (continued)
---slide

---theme_slide_header_1
height        = 6%
background    = white
color         = black
padding       = 1% 2%
border-top    = 8px solid #9999D9
border-radius = 0
metadata      = [['title','font-size:90%;']]
---endtheme_slide_header_1 

---theme_slide_header_2
height        = 6%
background    = white
color         = #9999D9
padding       = 1% 4%
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['sectiontitle','font-size:90%;']]
---endtheme_slide_header_2

---theme_slide_header_3
height        = 6%
background    = white
color         = #9999D9
padding       = 1% 6%
border-bottom = 8px solid #9999D9
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['subsectiontitle','font-size:90%;']]
---endtheme_slide_header_3

---theme_slide_header_4
height        = 8%
background    = white
color         = #9999D9
padding       = 1% 2%
metadata      = [['slidetitle','font-size:160%;']]
---endtheme_slide_header_4

---theme_slide_footer_1
active = False
---endtheme_slide_footer_1 
 
---theme_slide_sidebar_1
active = False
---endtheme_slide_sidebar_1

---endslide

Theme definition:
```lua
---theme_slide_header_3
height        = 6%
background    = white
color         = #9999D9
padding       = 1% 6%
border-bottom = 8px solid #9999D9
metadata      = [['|custom|&#208;','float:left;font-size:90%'],&&
                 ['subsectiontitle','font-size:90%;']]
---endtheme_slide_header_3

---theme_slide_header_4
height        = 6%
background    = white
color         = #9999D9
padding       = 1% 2%
metadata      = [['slidetitle','font-size:160%;']]
---endtheme_slide_header_4 
``` 
 
### Berkeley
---slide

---theme_slide_header_1
height        = 10%
background    = #3333B2
color         = white
padding       = 0
metadata      = [['|custom|.','float:left;height:100%;width:20%;color:#262686;background:#262686;'],&&
                 ['slidetitle','float:left;padding:1% 2%;font-size:190%;']]
---endtheme_slide_header_1 

---theme_slide_footer_1
active = False
---endtheme_slide_footer_1 
 
---theme_slide_sidebar_1
position   = L
background = #3333B2
---endtheme_slide_sidebar_1

---endslide

Theme definition:
```lua
---theme_slide_header_1
height        = 10%
background    = #3333B2
color         = white
padding       = 0
metadata      = [['|custom|.','float:left;height:100%;width:20%;color:#262686;background:#262686;'],&&
                 ['slidetitle','float:left;padding:1% 2%;font-size:190%;']]
---endtheme_slide_header_1

---theme_slide_sidebar_1
position      = L
width         = 20%
padding       = 1% 2%
background = #3333B2
color         = white
metadata      = [['title','font-weight:bold;font-variant:small-caps;font-size:105%;display:inline-block'],                                          &&
                 ['authors','font-variant:small-caps;font-size:90%;display:inline-block'],                                                          &&
                 ['affiliations','margin-top:4%;margin-bottom:10%;font-variant:small-caps;font-size:70%;white-space:pre-wrap;display:inline-block'],&&
                 ['toc','font-size:70%;',2]]
---endtheme_slide_sidebar_1 
``` 

### $overview
---slide
---theme_slide_global
data-scale       = 10
---endtheme_slide_global
---endslide
