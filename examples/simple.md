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
---endmetadata

---theme_slide_global
width            = 900px
height           = 700px
border_radius    = 10px
background_color = white
color            = rgb(102,102,102)
font_size        = 100%
---endtheme_slide_global

---theme_slide_content
width            = 100%
height           = 100%
background_color = white
color            = rgb(102,102,102)
border_radius    = 10px
---endtheme_slide_content

---theme_slide_header_1
height           = 10%
background_color = #4788B3
color            = white
border_radius    = 10px 10px 0 0
elements         = ['slidetitle','logo']
---endtheme_slide_header_1

---theme_slide_header_2
height           = 3%
background_color = red
color            = white
border_radius    = 0
elements         = ['slidetitle','logo']
---endtheme_slide_header_2

---theme_slide_footer_1
height           = 10%
background_color = #86B2CF
color            = white
---endtheme_slide_footer_1

---theme_slide_sidebar_1
position         = L
width            = 10%
background_color = linear-gradient(#4788B3,#86B2CF)
color            = white
border_radius    = 0 0 0 0
---endtheme_slide_sidebar_1

---theme_slide_sidebar_3
position         = L
width            = 10%
background_color = red
color            = white
border_radius    = 0
---endtheme_slide_sidebar_3

---theme_slide_sidebar_2
position         = R
width            = 10%
background_color = linear-gradient(#4788B3,#86B2CF)
color            = white
border_radius    = 0
---endtheme_slide_sidebar_2

# Introduction

## Motivation

### Why?
We love html-based slides with cool effects (by means of `impress.js`, `reveal.js` etc...) but we need more structured slides style for long, scientific presentation. Our ideal talk-makes must have:

* simple syntax as markdown;
* html slides output;
* latex equation support;
* cool effects;

### For whom?
Scientific researchers used to write presentation with beamer-latex that want to introduce the cool effects of modern html-based presentations to their high-quality scientific slides.

## Requirements

### How it works?
You write a markdown and MaTiSSe.py creates an impressive presentation even if you are a boring scientific researcher by means of nice html slides powered by:

* Python:
    + [x] `yattag` module;
    + [x] `markdown` module;
* Javascript:
    + [x] `impress.js`;
    + [ ] `jmpress.js`;
    + [ ] `reveal.js`;

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
