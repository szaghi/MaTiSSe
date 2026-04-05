# Theme YAML Reference

Quick lookup for every key accepted by the `theme:` and `overtheme:` YAML blocks.
For a conceptual introduction see [Guide: Themes](/guide/themes);
for comprehensive examples see [Advanced: Themes](/advanced/themes).

All theme configuration lives under a top-level `theme:` mapping.
Every section is optional — include only what you need.

## Schema overview

```yaml
---
theme:
  palette:    # named color variables — reference with $varname
  canvas:     # viewport / body background
  lists:      # ordered and unordered list styling
  toc:        # table of contents styling
  layout:     # slide structure: dimensions, decorators (headers/footers/sidebars), content area
  entities:   # content environments: box, note, table, figure, video
  code:       # fenced code block styling and Pygments style selection
---
```

---

## `palette`

Define named color (or value) variables here. Reference them anywhere below with `$varname`.
Unknown references emit a warning and are left as-is.

```yaml
palette:
  background: '#282a36'
  foreground: '#f8f8f2'
  accent:     '#50fa7b'
  highlight:  '#ffb86c'
```

Variable names may contain letters, digits, underscores, and hyphens.
Palette values are resolved **once** before CSS generation — single-pass, no chaining.

---

## `canvas`

The full-viewport background behind all slides.

```yaml
canvas:
  background: 'radial-gradient(rgb(40,40,60), rgb(10,10,20))'
```

Any CSS property valid on `body` is accepted.

---

## `lists`

Styling for ordered and unordered lists. All four sub-keys are optional.

```yaml
lists:
  ordered:          # <ol li> — the list item container
    margin-top: '0.5em'
  ordered-items:    # <ol li:before> — the item marker (counter)
    content: 'counter(item)'
    color: '$accent'
    padding-left: '1%'
  unordered:        # <ul li> — the list item container
    margin-top: '0.5em'
  unordered-items:  # <ul li:before> — the bullet symbol
    color: '$accent'
    content: "'\\25A0'"
```

---

## `toc`

Table of contents styling. Base properties apply to `.toc`; the four `*-emph` sub-keys
style the highlighted entry at each hierarchy level (chapter, section, subsection, slide).

```yaml
toc:
  display: 'inline-block'
  font-size: '90%'
  font-variant: 'small-caps'
  color: '$foreground'
  chapter-emph:
    border: '1px solid $accent'
    color: '$accent'
  section-emph:
    border: '1px solid $accent'
    font-weight: 'bold'
    color: '$accent'
  subsection-emph:
    color: '$highlight'
  slide-emph:
    color: '$foreground'
```

---

## `layout`

Defines the structural shell of every slide.

### `layout.slide` — global slide container

Controls slide dimensions, borders, background, font size, and impress.js transition data.

```yaml
layout:
  slide:
    transition: 'horizontal'   # horizontal | vertical | absolute
    width: '900px'
    height: '700px'
    font-size: '120%'
    data-offset: '20'          # pixel gap between slides
    scale: '1'
    border-radius: '10px'
    border-style: 'solid'
    border-width: '1px'
    border-color: '$accent'
    background: 'transparent'
    # impress.js positioning (for overtheme / absolute transition):
    data-x: '0'
    data-y: '0'
    data-z: '0'
    data-rotate-x: '0'
    data-rotate-y: '0'
    data-rotate-z: '0'
```

### `layout.content` — content area

The main text region inside the slide, after headers/footers/sidebars have taken their space.

```yaml
layout:
  content:
    background: '$background'
    color: '$foreground'
    padding: '2%'
```

### `layout.header-N`, `layout.footer-N` — horizontal bands

Named bands that stack above (headers) or below (footers) the content area.
Use any suffix — `header-1`, `header-2`, `footer-0`, `footer-1`, etc.

```yaml
layout:
  header-1:
    height: '10%'
    background: '$accent'
    color: 'white'
    padding: '0'
    active: 'yes'            # 'yes' (default) or 'no' to disable
    metadata:                # metadata placeholders rendered inside the band
      slidetitle:
        float: 'left'
        font-size: '180%'
        font-variant: 'small-caps'
      logo:
        float: 'right'
        height: '100%'
      custom-1:              # literal text snippet
        value: ' | '
        float: 'left'
        color: 'grey'
  footer-1:
    height: '6%'
    background: '$accent'
    metadata:
      slidenumber:
        float: 'right'
        padding: '0 1%'
      total_slides_number:
        float: 'right'
        padding: '0 1%'
```

**Available metadata placeholders:** `title`, `subtitle`, `authors`, `authors_short`,
`affiliations`, `affiliations_short`, `emails`, `date`, `conference`, `conference_short`,
`session`, `location`, `slidenumber`, `total_slides_number`, `sectiontitle`,
`sectionnumber`, `subsectiontitle`, `subsectionnumber`, `slidetitle`, `chaptertitle`,
`chapternumber`, `logo`, `timer`, `toc`, `custom-N` (arbitrary literal text via `value:`).

### `layout.sidebar-N` — vertical bands

```yaml
layout:
  sidebar-1:
    position: 'L'            # 'L' (left) or 'R' (right, default)
    width: '20%'
    background: '$background'
    color: '$foreground'
    padding: '1% 2%'
    border-radius: '10px 0 0 0'
    metadata:
      title:
        font-weight: 'bold'
        font-variant: 'small-caps'
        color: '$accent'
      toc:
        depth: '1'           # TOC depth level to show
        font-size: '80%'
```

---

## `entities`

Styling for content environments. Each environment has optional `caption:` and `content:`
sub-dicts; remaining keys style the outer container.

```yaml
entities:
  box:
    display: 'inline-block'
    border-radius: '10px'
    caption:
      color: '$accent'
      border-bottom: '1px solid $accent'
      display: 'inline-block'
      padding: '0 2%'
    content:
      padding: '0 2%'
      font-size: '120%'
  note:
    display: 'inline-block'
    caption:
      background: '$accent'
      color: 'white'
    content:
      padding: '0 1em'
  table:
    display: 'inline-block'
    caption:
      color: '$accent'
      font-size: '120%'
  figure:
    text-align: 'center'
    font-variant: 'small-caps'
    caption:
      font-size: '80%'
      color: '$accent'
    content:
      padding: '1% 5%'
  video:
    text-align: 'center'
    caption:
      color: '$accent'
    content:
      controls: ''           # presence of 'controls' enables video controls
      autoplay: ''
      padding: '1% 1%'
```

---

## Per-slide overrides (`overtheme`)

Schema is identical to `theme:`, plus one extra key at the top level:

| Key | Type | Description |
|---|---|---|
| `copy-from-theme` | bool | If `true`, start from the full global theme before applying overrides. Default: `false` (start from scratch). |

Place the block immediately after the `####` heading of the target slide:

```markdown
#### My special slide
---
overtheme:
  copy-from-theme: true
  layout:
    slide:
      border-radius: '50%'
    content:
      padding: '15% 20%'
      font-size: '180%'
    footer-1:
      active: 'no'
---
```

---

## `code`

Controls the appearance of fenced code blocks and selects the [Pygments](https://pygments.org/)
syntax highlighting style.

```yaml
theme:
  code:
    style: 'monokai'      # Pygments style name (default: 'default')
    font-size: '85%'      # any CSS property applies to the .highlight pre selector
    border-radius: '4px'
    padding: '0.5em 1em'
```

The `style` key is special — it selects the Pygments colour scheme and triggers regeneration
of `css/pygments.css` in the output directory.  All other keys are emitted as plain CSS on
the `.highlight pre` selector, letting you override font size, padding, border, etc.

List all available Pygments styles:

```bash
matisse build --print-code-styles
```

---

## Built-in themes

```bash
matisse build --print-themes          # list all names
matisse build -i talk.md --theme dracula
```

| Name | Structure | Colours |
|---|---|---|
| `matisse` | Right sidebar + header + footer | Blue gradient |
| `sapienza` | Header + footer | Sapienza red |
| `dracula` | Left sidebar + header + footer | Dracula dark |
| `solarized-dark` | Left sidebar + header + footer | Solarized dark |
| `beamer-antibes` | Three stacked headers | Beamer blue |
| `beamer-berkely` | Left sidebar + header | Beamer blue |
| `beamer-berlin` | Three stacked headers + two footers | Beamer dark blue |
| `beamer-madrid` | Header + footer | Beamer blue |

---

## Migration guide (v1.5 → v1.6)

The theme YAML format changed completely in v1.6. The table below shows the most
common patterns:

| Old (v1.5) | New (v1.6) |
|---|---|
| `theme: - canvas: - background: 'X'` | `theme:\n  canvas:\n    background: 'X'` |
| `theme: - slide: - width: '900px'` | `theme:\n  layout:\n    slide:\n      width: '900px'` |
| `theme: - slide: - content: - bg: 'X'` | `theme:\n  layout:\n    content:\n      background: 'X'` |
| `theme: - slide: - header-1: ...` | `theme:\n  layout:\n    header-1: ...` |
| `theme: - box: - display: 'block'` | `theme:\n  entities:\n    box:\n      display: 'block'` |
| `overtheme: - copy-from-theme: True` | `overtheme:\n  copy-from-theme: true` |

**Key structural changes:**
- All CSS values are now plain YAML dicts (`prop: value`) instead of lists of single-key dicts (`- prop: value`).
- `canvas:`, `lists:`, `toc:`, `layout:`, `entities:`, `code:` are top-level sections under `theme:`.
- Slide sub-elements (`content:`, `header-N`, `footer-N`, `sidebar-N`) move from under `slide:` to directly under `layout:`.
- The new `palette:` section lets you define named colors and reference them with `$varname`.
- `copy-from-theme:` moves to the top level of `overtheme:` (not inside a theme element list).
