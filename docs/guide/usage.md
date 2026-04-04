# Usage

This page is a comprehensive walkthrough of MaTiSSe derived from the bundled
`examples/getting-started` presentation — a self-documented showcase of every major feature.

## How it works

MaTiSSe is a CLI tool. You write your presentation as a plain Markdown file and run:

```bash
matisse build -i your_presentation.md
```

This creates a directory (named after the input file without its extension) that contains
the self-contained HTML presentation. Open `index.html` in any modern browser and navigate
with arrow keys or spacebar.

Common invocations:

```bash
# Basic build
matisse build -i talk.md -o talk/

# Insert a TOC at the beginning of each section (depth 3)
matisse build -i talk.md --toc-at-sec-beginning 3

# Generate a sample skeleton with a built-in theme
matisse build --sample mytalk.md --theme beamer-madrid
```

See the [CLI reference](/reference/cli) for the full option list.

## The MaTiSSe universe

Understanding the presentation model is the key to mastering MaTiSSe.
A presentation is rendered on an **infinite canvas**. Each slide is an element placed on
that canvas; impress.js handles 2D/3D positioning and transitions between them.

Every slide is composed of:

- **canvas** — the infinite background surface (one per presentation);
- **headers** — any number of horizontal bands above the content ($N_H \in [0, \infty)$);
- **footers** — any number of horizontal bands below the content ($N_F \in [0, \infty)$);
- **left/right sidebars** — any number of vertical columns aside the content ($N_L, N_R \in [0, \infty)$);
- **content** — the single main area where slide text lives.

![MaTiSSe universe](/images/matisse-universe-no_bg.png)

Headers, footers, and sidebars are *theme containers*: their content is driven entirely by the
theme definition (metadata values, TOC, logos, …). The **content** area is what you write in
your Markdown source.

## Structuring a presentation

Use standard Markdown headings to define the hierarchy:

```markdown
# Chapter title         ← h1
## Section title        ← h2
### Subsection title    ← h3
#### Slide title        ← h4
```

Everything that follows a `####` heading up to the next heading is the slide's content.

::: warning Ordering rule
If you define at least one chapter (`#`), any sections/subsections/slides that appear
*before* the first chapter are ignored. The same rule applies to sections and subsections.
Use `--verbose` to see warnings about misplaced content.
:::

### Unstructured presentations

You can omit chapters/sections/subsections entirely and write a flat list of slides:

```markdown
#### First slide
Content here.

#### Second slide
More content.
```

### The title page

`$titlepage` is a special directive that creates a slide excluded from the TOC:

```markdown
#### $titlepage
```

To strip all headers/footers/sidebars from it, add an empty overtheme block:

```markdown
#### $titlepage
---
overtheme:
  slide:
---
```

Then fill it freely with `$box` environments, metadata placeholders, etc.

## Metadata

Presentation metadata is defined in a YAML block anywhere in the source (conventionally at
the top). The block **must** start with the `metadata:` key:

```yaml
---
metadata:
  - title: 'Your Talk Title'
  - subtitle: 'A Subtitle'
  - authors:
    - First Author
    - Second Author
  - authors_short:
    - F. Author
    - S. Author
  - emails:
    - first@example.com
    - second@example.com
  - affiliations:
    - First University, Department of Something
    - Second University, Institute of Things
  - affiliations_short:
    - First U.
    - Second U.
  - logo: 'images/logo.png'
  - date: '15th January, 2025'
  - conference: 'International Conference on Something'
  - conference_short: 'ICS 2025'
  - session: 'Session on Advanced Topics'
  - location: 'City, Country'
  - max_time: 30
  - toc_depth: 2
  - dirs_to_copy:
    - images
    - data
---
```

MaTiSSe also auto-generates these metadata values at build time:

| Key | Description |
|---|---|
| `sectiontitle` / `sectionnumber` | Current section name / number |
| `subsectiontitle` / `subsectionnumber` | Current subsection name / number |
| `slidetitle` / `slidenumber` | Current slide name / number |
| `total_slides_number` | Total number of slides |
| `toc` | Full table of contents |
| `timer` | Countdown timer (requires `max_time`) |

Use any metadata value inside slide content or theme definitions with `$key` or `$key[css]`:

```markdown
The speaker is $authors[color:#4788B3;font-weight:bold;]
```

See the full [Metadata reference](/reference/metadata) for details.

## Including external files

Split long presentations into multiple files with `$include`:

```markdown
$include(metadata.yaml)
$include(theme.yaml)

## First section

### First subsection

#### First slide
```

::: warning No recursion
`$include` is processed once at startup. Included files cannot themselves include other files.
:::

## Code listings

Use fenced code blocks exactly as in GitHub Flavored Markdown:

````markdown
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```
````

Syntax highlighting is provided by highlight.js. Use `--highlight-style` to select a style,
and `--print-highlight-styles` to list all available options.

## LaTeX equations

Inline and display math are supported natively via MathJax 3:

```markdown
Inline: $E = mc^2$

Display:
$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
```

Equations work inside slide content, box captions, figure captions, notes, and headers.
See the [Math & LaTeX guide](/advanced/math) for more details.

## Special environments

### Columns

Split slide content into side-by-side columns:

```markdown
$columns
$column[width:60%;padding-right:1%;border-right:1px solid #4788B3;]
Left column content here.

$column[width:40%;padding-left:1%;]
Right column content here.
$endcolumns
```

The `width` option is mandatory. If omitted, MaTiSSe divides the available width equally.
`display:block;float:left;` are added automatically.

See the [Columns guide](/advanced/columns).

### Box

The generic box renders any content with a customizable style:

```markdown
$box
$style[background:rgb(100,100,100);]
$caption(Mybox)[font-size:90%;color:white;]{An example of a generic Box}
$content[font-size:120%;color:white;]{Box content goes here.}
$endbox
```

- `$style[…]` — CSS for the outer box wrapper (optional)
- `$caption(type)[…]{text}` — caption with optional type prefix and CSS (optional)
- `$content(type)[…]{text}` — content with optional type and CSS (required)

### Note

```markdown
$note
$content{This is a note. The caption is always placed above the content.}
$endnote
```

The `caption_type` and `content_type` default to `Note` and `note`. Override with
`$caption(none)` to suppress the label.

### Table

```markdown
$table
$caption{My fancy Table}
$content{

|  /  | foo | bar | baz |
|-----|-----|-----|-----|
| a   | 1   |  2  |  3  |
| b   | 2   |  3  |  4  |

}
$endtable
```

The caption is always placed **above** the content.

### Figure

```markdown
$figure
$content[padding:1% 5%;width:90%;]{images/myplot.png}
$caption{Figure 1: My plot.}
$endfigure
```

The caption is always placed **below** the content. The `content` value must be a path to an
image file relative to the output directory root.

### Video

```markdown
$video
$content[width:95%;controls]{video/demo.mp4}
$caption(none){Demo video}
$endvideo
```

Add the `controls` CSS option to show play/pause controls. Use `autoplay` when controls are
omitted.

See dedicated guides: [Figures](/advanced/figures) · [Boxes & Notes](/advanced/boxes) ·
[Tables](/advanced/tables) · [Video](/advanced/video).

## Presentation-level theme

Theme blocks use a YAML `theme:` key and can appear anywhere in the source (conventionally
near the top, or in a separate file included with `$include`).

### Canvas

```yaml
---
theme:
  - canvas:
    - background: 'radial-gradient(rgb(240,240,240), rgb(110,110,110))'
---
```

The canvas maps to the HTML `<body>` and cannot be overridden per-slide.

### TOC

```yaml
---
theme:
  - toc:
    - font-variant: 'small-caps'
    - chapter-emph:
      - border: '1px solid #4788B3'
      - border-radius: '5px'
    - section-emph:
      - border: '1px solid #4788B3'
      - border-radius: '5px'
    - subsection-emph:
      - border: '1px solid #4788B3'
      - border-radius: '5px'
    - slide-emph:
      - border: '1px solid #4788B3'
      - border-radius: '3px'
---
```

`chapter-emph`, `section-emph`, `subsection-emph`, and `slide-emph` style the *currently
active* entry in a rendered TOC.

### Box-like environment themes

Define a default style for all notes, figures, tables, or generic boxes in one place:

```yaml
---
theme:
  - note:
    - display: 'inline-block'
    - font-variant: 'small-caps'
    - box-shadow: '7px 7px 5px rgba(200,200,200,0.3)'
    - border-radius: '20px'
    - caption:
      - padding: '0 2%'
      - color: '#4788B3'
      - border-bottom: '1px solid #4788B3'
      - display: 'inline-block'
    - content:
      - padding: '0 2%'
      - font-size: '120%'
  - figure:
    - text-align: 'center'
    - caption:
      - font-style: 'italic'
      - font-size: '80%'
---
```

Supported keys: `box`, `note`, `figure`, `table`, `video`.

### List customization

```yaml
---
theme:
  - unordered-list:
    - padding-bottom: '0.5em'
  - unordered-list-items:
    - color: '#4788B3'
    - content: "'\\25D5'"
  - ordered-list:
    - padding-bottom: '0.8em'
    - background: 'rgba(241,241,241,0.5)'
  - ordered-list-items:
    - content: 'counter(item, upper-roman)'
    - color: 'pink'
---
```

The `content` property accepts any CSS `list-style-type` value or a Unicode glyph code.

## Slide-level theme

The global slide theme sets dimensions, fonts, transitions, and default element styles for
*all* slides.

### Slide container

```yaml
---
theme:
  - slide:
    - width: '900px'
    - height: '700px'
    - border-radius: '10px'
    - background: 'green'
    - color: 'rgb(102,102,102)'
    - font-size: '100%'
    - transition: 'horizontal'
    - data-offset: '20'
---
```

**Special (non-CSS) options:**

| Option | Values | Description |
|---|---|---|
| `transition` | `horizontal`, `-horizontal`, `vertical`, `-vertical`, `diagonal`, `-diagonal`, `diagonal-x`, `diagonal-y`, `absolute` | Slide placement direction on the canvas |
| `data-offset` | number (px) | Gap between consecutive slides |
| `data-scale` | number | Zoom factor (useful in overtheme) |
| `data-rotate` | degrees | 2D rotation |
| `data-rotate-x/y/z` | degrees | 3D rotation around each axis |

`transition: absolute` requires explicit `data-x`, `data-y`, `data-z` per slide via overtheme.

### Headers

```yaml
---
theme:
  - slide:
    - header-1:
      - height: '6%'
      - padding: '1% 2%'
      - background: '#4788B3'
      - color: 'white'
      - border-radius: '10px 10px 0 0'
      - metadata:
        - slidetitle:
          - font-size: '150%'
          - float: 'left'
          - font-variant: 'small-caps'
        - logo:
          - height: '100%'
          - float: 'right'
---
```

Headers are numbered (non-consecutive numbers are allowed). `header-1` is inserted before
`header-2`. The `width` is automatically set to 100% — do not override it.

Use `metadata:` to embed presentation or auto-generated values. Any metadata key is valid,
plus the special `custom-N` key for literal text:

```yaml
- custom-1:
  - value: 'slide '
  - float: 'right'
```

### Footers

Footers follow the same pattern as headers, placed below the content:

```yaml
---
theme:
  - slide:
    - footer-1:
      - height: '6%'
      - padding: '1% 2%'
      - background: '#86B2CF'
      - color: 'white'
      - metadata:
        - slidenumber:
          - float: 'right'
          - padding: '0 1%'
        - custom-1:
          - value: ' of '
          - float: 'right'
        - total_slides_number:
          - float: 'right'
          - padding: '0 1%'
        - timer:
          - controls: ''
          - font-size: '70%'
          - float: 'right'
---
```

Use `active: 'no'` to suppress a footer for a specific overtheme without deleting it.

### Sidebars

```yaml
---
theme:
  - slide:
    - sidebar-1:
      - position: 'R'        # 'L' for left, 'R' for right
      - width: '20%'
      - padding: '1% 2%'
      - background: 'linear-gradient(#4788B3,#86B2CF)'
      - color: 'white'
      - metadata:
        - title:
          - font-weight: 'bold'
          - font-variant: 'small-caps'
        - toc:
          - depth: '3'
          - font-size: '70%'
---
```

The `height` is automatically set to 100%. Left sidebars are inserted before right ones.
Within each side, lower numbers are inserted first.

### Content

```yaml
---
theme:
  - slide:
    - content:
      - background: 'white'
      - color: 'rgb(102,102,102)'
      - padding: '1%'
---
```

`width` and `height` are computed automatically from the remaining space after headers,
footers, and sidebars. Do not set them manually.

## Per-slide overtheme

Any slide can override the global theme with a YAML block placed immediately after its `####`
heading:

```markdown
#### My custom slide
---
overtheme:
  - slide:
    - transition: 'diagonal'
    - content:
      - font-family: 'Comic Sans MS, cursive, sans-serif'
    - footer-1:
      - active: 'no'
---

Slide content here — rendered with the diagonal transition and comic font.
```

`copy-from-theme: True` inside an overtheme block copies all global slide settings first,
then applies the local overrides on top.

The Prezi-style elliptic slide effect is achieved entirely via overtheme:

```yaml
---
overtheme:
  - slide:
    - border-radius: '50%'
    - data-offset: '200'
    - content:
      - border-radius: '50%'
      - padding: '15% 20%'
      - font-size: '180%'
---
```

## Full example

Below is a minimal but complete source file that demonstrates the main features:

```markdown
$include(metadata.yaml)
$include(theme.yaml)

#### $titlepage
---
overtheme:
  slide:
---
$box
$style[width:100%;height:40%;background:#4788B3;]
$content[color:white;text-align:center;]{
$title[font-size:200%;padding-top:2%;]
$subtitle[font-size:120%;padding-top:2%;]
}
$endbox
$authors[font-size:110%;]

# Introduction

## Overview

### Background

#### What is MaTiSSe?

MaTiSSe means **Markdown To Impressive Scientific Slides**.

$$E = mc^2$$

#### Code example

```python
def hello(name: str) -> str:
    return f"Hello, {name}!"
\```

## Methods

### Approach

#### Algorithm

$columns
$column[width:50%;]
- Step 1
- Step 2
- Step 3

$column[width:50%;]
$figure
$content[width:90%;]{images/diagram.png}
$caption{Fig. 1: Diagram}
$endfigure
$endcolumns
```

For the `metadata.yaml` and `theme.yaml` structure see the
[Metadata reference](/reference/metadata) and [Theme YAML reference](/reference/themes).
