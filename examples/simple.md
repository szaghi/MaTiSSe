

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

---theme
slide_width            = 900px
slide_height           = 700px
slide_border_radius    = 10px
slide_background_color = white
slide_color            = rgb(102,102,102)
slide_font_size        = 100%

slide_content_width            = 100%
slide_content_height           = 100%
slide_content_background_color = white
slide_content_color            = rgb(102,102,102)
slide_content_border_radius    = 0 0 0 0

header                        = True
slide_header_height           = 10%
slide_header_background_color = #4788B3
slide_header_color            = white
slide_header_border_radius    = 10px 10px 0 0
slide_header_elements         = ['slidetitle','logo']

footer                        = False
slide_footer_height           = 10%
slide_footer_background_color = #86B2CF
slide_footer_color            = white

sidebarL                        = False
slide_sidebarL_width            = 10%
slide_sidebarL_height           = 80%
slide_sidebarL_background_color = linear-gradient(#4788B3,#86B2CF)
slide_sidebarL_color            = white
slide_sidebarL_border_radius    = 0 0 0 0

sidebarR                        = True
slide_sidebarR_width            = 10%
slide_sidebarR_height           = 90%
slide_sidebarR_background_color = linear-gradient(#4788B3,#86B2CF)
slide_sidebarR_color            = white
slide_sidebarR_border_radius    = 0 0 10px 0
---endtheme

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
