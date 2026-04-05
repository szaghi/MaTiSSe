# Themes In Depth

This page is a comprehensive walkthrough of every theme section. Read
[Guide: Themes](/guide/themes) first for an overview.

---

## Palette — named colour variables

The `palette` section lets you define named variables and reference them anywhere in the
theme with `$varname`. This avoids repeating hex codes throughout the file.

```yaml
theme:
  palette:
    background: '#282a36'
    foreground: '#f8f8f2'
    accent:     '#50fa7b'
    muted:      '#6272a4'
  canvas:
    background: '$background'
  layout:
    content:
      color: '$foreground'
    header-1:
      background: '$accent'
```

**Rules:**
- Variable names: letters, digits, underscores, hyphens.
- Resolution is single-pass (no chaining: `$x: '$y'` with `$y: 'red'` does **not** work).
- Undefined references emit a warning and are left unchanged in the output.

---

## Canvas — the viewport background

`canvas` styles the HTML `<body>` element — the infinite surface behind all slides.

```yaml
theme:
  canvas:
    background: 'radial-gradient(rgb(68,71,90), rgb(30,31,43))'
```

Any CSS property valid on `body` is accepted. The canvas cannot be overridden per-slide.

---

## Lists

`lists` has four optional sub-keys that style ordered and unordered list markers and
their containers.

```yaml
theme:
  lists:
    ordered:           # <ol li>  — the item row
      margin-top: '0.5em'
    ordered-items:     # <ol li:before>  — the counter marker
      content: 'counter(item, upper-roman)'
      color: '$accent'
      padding-left: '1%'
    unordered:         # <ul li>  — the item row
      margin-top: '0.5em'
    unordered-items:   # <ul li:before>  — the bullet symbol
      color: '$accent'
      content: "'\\25A0'"   # Unicode BLACK SQUARE ■
```

The `content` property of `*-items` accepts any CSS `content` expression: named counters,
quoted strings, Unicode glyphs (prefixed with `\\`), or `counter(item)` for decimals.

---

## TOC

`toc` styles the `.toc` element wherever it is injected (typically inside a sidebar
metadata placeholder). Base properties apply to the whole block; the four `*-emph`
sub-keys style the *currently active* entry at each hierarchy level.

```yaml
theme:
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
    subsection-emph:
      color: '$muted'
    slide-emph:
      color: '$foreground'
```

---

## Layout — slide structure

`layout` is the most important section. It defines the slide container, the content area,
and any number of headers, footers, and sidebars.

### The slide container

```yaml
theme:
  layout:
    slide:
      width: '900px'
      height: '700px'
      font-size: '100%'
      border-radius: '10px'
      border: '1px solid $muted'
      background: 'transparent'
      transition: 'horizontal'
      data-offset: '20'
```

**Non-CSS options** (passed to impress.js as `data-*` attributes):

| Key | Default | Description |
|---|---|---|
| `transition` | `horizontal` | Slide placement algorithm on the canvas. See table below. |
| `data-offset` | `0` | Pixel gap inserted between consecutive slides. |
| `data-scale` | `1` | impress.js zoom factor. |
| `data-rotate` | `0` | 2D rotation in degrees. |
| `data-rotate-x/y/z` | `0` | 3D rotation around each axis. |
| `data-x`, `data-y`, `data-z` | — | Absolute position (used with `transition: absolute`). |

**Transition values:**

| Value | Direction |
|---|---|
| `horizontal` | Left → right (default) |
| `-horizontal` | Right → left |
| `vertical` | Top → bottom |
| `-vertical` | Bottom → top |
| `diagonal` | Diagonal (x and y together) |
| `-diagonal` | Reverse diagonal |
| `diagonal-x` | Diagonal, x-axis only |
| `diagonal-y` | Diagonal, y-axis only |
| `absolute` | Use explicit `data-x/y/z` from overtheme |

### The content area

The content area is what fills the slide after headers, footers, and sidebars have taken
their share. **Do not set `width` or `height` here** — they are computed automatically.

```yaml
theme:
  layout:
    content:
      background: 'white'
      color: 'rgb(102,102,102)'
      padding: '2%'
      font-family: 'Georgia, serif'
```

### Headers

Headers are numbered horizontal bands that stack **above** the content area.
The numbering is arbitrary — `header-1` is inserted before `header-2`.

```yaml
theme:
  layout:
    header-1:
      height: '10%'
      background: '$accent'
      color: 'white'
      padding: '0'
      active: 'yes'          # 'yes' (default) or 'no' to suppress
      metadata:
        slidetitle:
          float: 'left'
          font-size: '180%'
          font-variant: 'small-caps'
        logo:
          float: 'right'
          height: '100%'
```

- **`width`** is automatically set to 100% — do not override it.
- **`active: 'no'`** suppresses the entire band (useful in overtheme to hide it on specific slides).
- **`metadata:`** embeds presentation values or auto-generated content inside the band. See the [metadata placeholder list](#metadata-placeholders) below.

### Footers

Footers follow the same schema as headers, stacked **below** the content area.

```yaml
theme:
  layout:
    footer-1:
      height: '6%'
      background: '$accent'
      padding: '0 2%'
      metadata:
        sectiontitle:
          float: 'left'
          font-variant: 'small-caps'
        slidenumber:
          float: 'right'
          padding: '0 1%'
        custom-1:
          value: ' / '
          float: 'right'
          color: 'grey'
        total_slides_number:
          float: 'right'
          padding: '0 1%'
        timer:
          controls: ''
          font-size: '70%'
          float: 'right'
```

`custom-N` accepts a `value:` key for arbitrary literal text snippets (separator strings,
section labels, etc.).

### Sidebars

Sidebars are vertical bands placed to the left or right of the content area.
`position: 'L'` puts it on the left; `position: 'R'` (default) on the right.

```yaml
theme:
  layout:
    sidebar-1:
      position: 'L'
      width: '20%'
      background: '$background'
      color: '$foreground'
      padding: '1% 2%'
      border-right: '1px solid $muted'
      metadata:
        title:
          font-weight: 'bold'
          font-variant: 'small-caps'
          color: '$accent'
        authors:
          font-size: '85%'
          color: '$muted'
        toc:
          depth: '1'
          font-size: '75%'
```

- **`height`** is automatically set to 100% — do not override it.
- Left sidebars are inserted before right ones; lower numbers are inserted first within each side.
- The `toc` metadata placeholder accepts a `depth:` key to control how many hierarchy levels to show.

### Metadata placeholders {#metadata-placeholders}

The following keys are valid inside any `metadata:` block (header, footer, or sidebar).
Each key maps to a CSS property dict that styles the rendered element.

| Key | Content |
|---|---|
| `title` | Presentation title |
| `subtitle` | Presentation subtitle |
| `authors` | Full author list |
| `authors_short` | Short author list |
| `affiliations` | Full affiliation list |
| `affiliations_short` | Short affiliation list |
| `emails` | Author email list |
| `date` | Presentation date |
| `conference` | Conference name |
| `conference_short` | Short conference name |
| `session` | Session name |
| `location` | Location |
| `chaptertitle` / `chapternumber` | Current chapter |
| `sectiontitle` / `sectionnumber` | Current section |
| `subsectiontitle` / `subsectionnumber` | Current subsection |
| `slidetitle` / `slidenumber` | Current slide |
| `total_slides_number` | Total slide count |
| `logo` | Logo image (from `logo:` metadata) |
| `timer` | Countdown timer (requires `max_time:` metadata) |
| `toc` | Table of contents (accepts `depth:` CSS key) |
| `custom-N` | Arbitrary literal text (requires `value:` CSS key) |

---

## Entities — content environments

`entities` sets default styles for all five content environments: `box`, `note`, `table`,
`figure`, and `video`. Each has optional `caption:` and `content:` sub-dicts; remaining
keys style the outer container.

```yaml
theme:
  entities:
    box:
      display: 'inline-block'
      border-radius: '10px'
      box-shadow: '7px 7px 5px rgba(0,0,0,0.2)'
      caption:
        color: '$accent'
        border-bottom: '1px solid $accent'
        display: 'inline-block'
        padding: '0 2%'
      content:
        padding: '0 2%'
        font-size: '110%'
    note:
      display: 'inline-block'
      border-radius: '10px'
      caption:
        background: '$accent'
        color: 'white'
        padding: '0 2%'
      content:
        padding: '0 1em'
    table:
      display: 'inline-block'
      caption:
        color: '$accent'
        font-size: '90%'
    figure:
      text-align: 'center'
      caption:
        font-size: '80%'
        font-style: 'italic'
        color: '$muted'
      content:
        padding: '1% 5%'
    video:
      text-align: 'center'
      caption:
        color: '$muted'
      content:
        controls: ''       # presence of this key enables video controls
        padding: '1% 1%'
```

Styles defined here are the default for every instance of that environment in the
presentation. Individual environments can still override with `$style[…]` inline.

---

## Code — syntax highlighting style

`code` controls the appearance of fenced code blocks. The special `style` key selects
the [Pygments](https://pygments.org/) colour scheme; all other keys are emitted as CSS
on the `.highlight pre` selector.

```yaml
theme:
  code:
    style: 'monokai'
    font-size: '85%'
    border-radius: '4px'
    padding: '0.5em 1em'
```

List available styles:

```bash
matisse build --print-code-styles
```

The selected style is always generated at build time into `css/pygments.css` — no CDN
dependency, no extra work needed for offline mode.

---

## Per-slide overtheme

Any `####` slide can carry an `overtheme:` block immediately after its heading line.
The schema is identical to `theme:`, with the addition of `copy-from-theme: true`.

### Minimal override

Only the keys you specify are changed; everything else retains the global theme value.

```markdown
#### Highlight slide
---
overtheme:
  layout:
    content:
      background: '#44475a'
      color: '#f8f8f2'
---

Content here uses a dark background just for this slide.
```

### Disabling a decorator

```markdown
#### Clean slide
---
overtheme:
  layout:
    header-1:
      active: 'no'
    footer-1:
      active: 'no'
---
```

### Full inheritance with `copy-from-theme`

Without `copy-from-theme`, the overtheme starts from scratch — the global theme's layout
is ignored for that slide. Use `copy-from-theme: true` to start from the full global
theme and patch specific values:

```markdown
#### $titlepage
---
overtheme:
  copy-from-theme: true
  layout:
    content:
      padding: '0%'
---
```

### Elliptic Prezi-style slide

```markdown
#### A round slide
---
overtheme:
  layout:
    slide:
      border-radius: '50%'
      data-offset: '200'
    content:
      border-radius: '50%'
      padding: '15% 20%'
      font-size: '180%'
---
```

### Absolute positioning

Use `transition: absolute` in the global theme and set explicit coordinates per slide:

```yaml
# global theme
theme:
  layout:
    slide:
      transition: 'absolute'
```

```markdown
#### Slide at a specific position
---
overtheme:
  layout:
    slide:
      data-x: '3000'
      data-y: '-1500'
      data-rotate-z: '90'
---
```

---

## Complete theme example

Below is a full theme definition representative of a real conference talk. Save it as
`theme.yaml` and include it with `$include(theme.yaml)`.

```yaml
theme:
  palette:
    bg:      '#1e1e2e'
    fg:      '#cdd6f4'
    accent:  '#cba6f7'
    muted:   '#6c7086'
    surface: '#313244'

  canvas:
    background: 'radial-gradient($bg, #11111b)'

  lists:
    ordered-items:
      content: 'counter(item)'
      color: '$accent'
      padding-left: '1%'
    unordered-items:
      color: '$accent'
      content: "'\\25B8'"

  toc:
    font-variant: 'small-caps'
    font-size: '85%'
    section-emph:
      color: '$accent'
      border-left: '3px solid $accent'
      padding-left: '4px'

  layout:
    slide:
      width: '900px'
      height: '700px'
      transition: 'horizontal'
      data-offset: '20'
      border-radius: '8px'
      border: '1px solid $surface'
    content:
      background: '$bg'
      color: '$fg'
      padding: '2%'
    header-1:
      height: '9%'
      background: '$surface'
      padding: '0 2%'
      metadata:
        slidetitle:
          float: 'left'
          font-size: '160%'
          font-variant: 'small-caps'
          color: '$accent'
        logo:
          float: 'right'
          height: '100%'
    footer-1:
      height: '5%'
      background: '$surface'
      padding: '0 2%'
      metadata:
        sectiontitle:
          float: 'left'
          font-size: '80%'
          font-variant: 'small-caps'
          color: '$muted'
        slidenumber:
          float: 'right'
          padding: '0 0.5%'
          font-size: '80%'
          color: '$muted'
        custom-1:
          value: ' / '
          float: 'right'
          color: '$muted'
          font-size: '80%'
        total_slides_number:
          float: 'right'
          padding: '0 0.5%'
          font-size: '80%'
          color: '$muted'
    sidebar-1:
      position: 'L'
      width: '18%'
      background: '$surface'
      padding: '2% 1%'
      metadata:
        title:
          font-weight: 'bold'
          font-variant: 'small-caps'
          font-size: '90%'
          color: '$accent'
        toc:
          depth: '1'
          font-size: '75%'

  entities:
    box:
      display: 'inline-block'
      border-radius: '8px'
      caption:
        color: '$accent'
        border-bottom: '1px solid $accent'
        padding: '0 2%'
      content:
        padding: '0 2%'
    note:
      display: 'inline-block'
      border-radius: '8px'
      caption:
        background: '$accent'
        color: '$bg'
        padding: '0 2%'
      content:
        padding: '0 1em'
    figure:
      text-align: 'center'
      caption:
        font-size: '80%'
        color: '$muted'
    table:
      display: 'inline-block'
      caption:
        color: '$accent'

  code:
    style: 'catppuccin-mocha'
    font-size: '85%'
    border-radius: '4px'
```
