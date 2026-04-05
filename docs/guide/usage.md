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

Syntax highlighting is provided by Pygments at build time — no browser JS required.
Use `--code-style` to select a style and `--print-code-styles` to list all available options.
See the [Code Highlighting guide](/advanced/code) for details.

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

## Themes

Theme blocks use a YAML `theme:` key and can appear anywhere in the source (conventionally
near the top, or in a separate file included with `$include`):

```yaml
---
theme:
  canvas:
    background: 'radial-gradient(rgb(240,240,240), rgb(110,110,110))'
  layout:
    slide:
      width: '900px'
      height: '700px'
    content:
      background: 'white'
      padding: '2%'
---
```

For a full walkthrough of all theme sections (palette, canvas, layout, decorators, entities,
code, overtheme) see:

- **[Guide: Themes](/guide/themes)** — built-in themes, your first custom theme, per-slide overtheme
- **[Advanced: Themes](/advanced/themes)** — every section with complete examples
- **[Reference: Theme YAML](/reference/themes)** — schema specification

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
