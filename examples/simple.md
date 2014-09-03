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

---theme_canvas
background = radial-gradient(rgb(240, 240, 240), rgb(110, 110, 110))
---endtheme_canvas

---theme_selector_code
font-family = Courier, monospace
background  = rgba(0,0,0,0.05)
---endtheme_selector_code

---theme_selector_pre-code
display        = block 
margin         = 1%
padding        = 1%
white-space    = pre-wrap 
background     = rgba(0,0,0,0.05)
box-shadow     = 4px 4px 6px rgba(0, 0, 0, .1)
border-radius  = 10px 10px 10px 10px
---endtheme_selector_pre-code

---theme_heading_4
border-bottom   = 1px solid #4788B3
---endtheme_heading_4

---theme_slide_global
width            = 900px
height           = 700px
border-radius    = 10px
background       = green
color            = rgb(102,102,102)
font-size        = 100%
slide-transition = horizontal
---endtheme_slide_global

---theme_slide_content
background    = white
color         = rgb(102,102,102)
padding       = 2%
---endtheme_slide_content

---theme_slide_header_1
height        = 6%
background    = #4788B3
color         = white
border-radius = 10px 10px 0 0
elements      = [['slidetitle','font-variant:small-caps;font-size:180%;padding:2%'],&&
                 ['logo','float:right;height:100%']]
---endtheme_slide_header_1

---theme_slide_footer_1
height     = 6%
background = #86B2CF
color      = white
elements   = [['timer','controls;font-size:70%;font-variant:small-caps;padding:1% 1%;float:right'],&&
              ['total_slides_number','float:right;padding:1% 1%'],                                 &&
              ['|custom| of ','float:right;padding:1% 0%'],                                        &&
              ['slidenumber','float:right;padding:1% 1%'],                                         &&
              ['|custom|slide ','float:right;padding:1% 0%']]
---endtheme_slide_footer_1

---theme_slide_sidebar_1
position      = R
width         = 20%
background    = linear-gradient(#4788B3,#86B2CF)
color         = white
border-radius = 0
elements      = [['title','font-weight:bold;font-variant:small-caps;font-size:105%;padding:5%;display:inline-block'],                                          &&
                 ['authors','font-variant:small-caps;font-size:90%;padding:5%;display:inline-block'],                                                          &&
                 ['affiliations','margin-top:4%;margin-bottom:10%;font-variant:small-caps;font-size:70%;white-space:pre-wrap;padding:5%;display:inline-block'],&&
                 ['toc','font-variant:small-caps;font-size:90%;white-space:pre-wrap;padding:5%;display:inline-block']]
---endtheme_slide_sidebar_1

# Introduction

## MaTiSSe.py, what is?

### The Acronym

#### Ciao
##### Ciao Ciao
###### Ciao Ciao Ciao

_MaTiSSe.py_ means **Ma**rkdown **T**o **I**mpressive **S**cientific **S**lid**e**s

It is basically a very simple and stupid (KISS) presentation maker based on simple `markdown` syntax.

For example the markdown code of this slide is:

```
_MaTiSSe.py_ means **Ma**rkdown **T**o **I**mpressive **S**cientific **S**lid**e**s

It is basically a very simple and stupid (KISS) presentation maker based on simple `markdown` syntax.
```

All other elements (headers, footers, sidebars, etc...) are handled by MaTiSSe.py once you have setup the theme of your presentation. 

The real cool feature is that for setting up your theme (as the one of the presentation you are reading) **you do not need to be a html-css guru!**

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
font-size = 110%
color = red
slide-transition = vertical
---endslide

Scientific researchers (at least the brave ones) are used to write presentation with _latex-beamer_. 

_LaTeX_ is great and the **beamer** class quality is incredible, however some drawbacks can be highlighted:

1. the compilation of an even small presentation can be _time consuming_;
2. latex _programming_ can be very inflexible frustrating the presenter;
3. the pdf output has great quality but it behaves not so well with multimedia content; 
4. it is rather complicated to introduce _prezi_-like effects.

MaTiSSe.py is designed for scientific researchers that want retain the best of _latex-beamer_ and _prezi_ worlds together. 

## Getting started

### How it works?
You write your presentation in markdown and MaTiSSe.py creates an impressive presentation even if you are a boring scientific researcher.


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
