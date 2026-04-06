---
metadata:
  - title:    "Advanced reveal.js Theming with MaTiSSe"
  - subtitle: "Full reference for RevealTheme options"
  - authors:
    - Your Name
  - affiliations:
    - Your Institution
  - date: "2026"
  - max_time: 30
  - toc_depth: 2
---

---
reveal:
  # --- Built-in CDN theme ---
  theme: moon               # black|white|league|beige|sky|night|moon|serif|simple|solarized|blood|dracula

  # --- Transitions ---
  transition: slide         # none|fade|slide|convex|concave|zoom
  transition_speed: default # default|fast|slow
  background_transition: fade

  # --- Navigation chrome ---
  controls: true
  controls_layout: bottom-right  # bottom-right|edges
  progress: true
  slide_number: "c/t"       # false|true|c|c/t|h/v|h.v

  # --- Playback behaviour ---
  loop: false
  center: true
  auto_slide: 0             # ms between auto-advances; 0 = off

  # --- Canvas size ---
  width: 1280
  height: 720
  margin: 0.04
  min_scale: 0.2
  max_scale: 2.0

  # --- Accessibility ---
  keyboard: true
  touch: true

  # --- Slide layout ---
  layout: linear            # linear|vertical  (vertical = chapters as 2D groups)

  # --- Plugins (loaded from CDN) ---
  plugins:
    - notes    # RevealNotes  — speaker notes; press S in browser
    - zoom     # RevealZoom   — click-to-zoom on slide elements
    - math     # RevealMath.MathJax3 — replaces standalone MathJax script

  # --- Code highlight style (Pygments) ---
  code_style: monokai

  # --- Inline custom CSS ---
  custom_css: |
    /* tighten up slide content padding */
    .reveal .slide-content { padding: 0.5em 1em; }
    /* make box captions pop */
    .reveal .box-caption { font-variant: small-caps; letter-spacing: 0.05em; }
---

---
# Slide decorators — header, footer, and sidebar
# Uses the same theme.layout schema as the impress backend.
# Remove or comment out this block to disable all decorators.
theme:
  layout:
    header-1:
      height: 7%
      background: "#0d1117"
      color: "#58a6ff"
      border-bottom: "1px solid #30363d"
      metadata:
        slidetitle:
          float: left
          font-size: 0.85em
          padding-left: 1em
          line-height: "7vh"
        slidenumber:
          float: right
          font-size: 0.75em
          padding-right: 1em
          line-height: "7vh"
    footer-1:
      height: 4%
      background: "#0d1117"
      color: "#8b949e"
      metadata:
        authors:
          float: left
          font-size: 0.65em
          padding-left: 1em
          line-height: "4vh"
        conference:
          float: right
          font-size: 0.65em
          padding-right: 1em
          line-height: "4vh"
---

# Introduction

## About this example

### What you are looking at

#### Title Slide

$box
$style[width:100%;background:linear-gradient(135deg,#0d1117,#161b22);border-radius:12px;padding:5%]
$content[color:#c9d1d9;text-align:center;]{
$title[display:block;font-size:175%;font-weight:700;padding-bottom:2%]
$subtitle[display:block;font-size:110%;opacity:0.8;padding-bottom:4%]
$authors[display:block;font-size:100%]
$affiliations[display:block;font-size:85%;opacity:0.65;padding-top:1%]
$date[display:block;font-size:80%;opacity:0.5;padding-top:3%]
}
$endbox

$note
$content{
Welcome to the advanced reveal.js example for MaTiSSe.

This talk demonstrates every configurable option in RevealTheme.

Press S to toggle presenter view.  Press O for overview.  Press F for full-screen.
}
$endnote

#### What this example covers

$columns
$column[width:48%]
**Presentation-level options**

- Built-in themes
- Transitions & speed
- Navigation chrome (controls, progress, slide numbers)
- Canvas size and margins
- Plugins (notes, zoom, math)
$column[width:48%]
**Per-slide overrides**

- Background colours
- Background images
- Per-slide transition
- Auto-animate between slides

All options live in a single `reveal:` YAML block.
$endcolumns

$note
$content{
These two categories map to the presentation-level YAML block and to
per-slide overtheme.reveal blocks respectively.
}
$endnote

# Presentation-Level Options

## Theme and Transitions

### Global styling

#### Choosing a built-in theme

The `theme` key selects one of reveal.js's twelve CDN-delivered themes:

$table
$caption{Available reveal.js themes}
$content{
| Name | Style |
|---|---|
| `black` | Dark grey background, white text (default) |
| `white` | Clean white |
| `moon` | Dark blue, used in this example |
| `sky` | Light blue |
| `beige` | Warm beige |
| `night` | Dark, high contrast |
| `serif` | Classic serif typography |
| `solarized` | Solarized palette |
| `dracula` | Dracula colour scheme |
| `blood` | Dark red accents |
| `league` | Grey scale |
| `simple` | Minimal |
}
$endtable

```yaml
---
reveal:
  theme: dracula
---
```

$note
$content{
All themes are loaded from cdn.jsdelivr.net — no local files needed.
}
$endnote

#### Transition options

Six transition styles plus a speed control:

```yaml
---
reveal:
  transition: slide         # none|fade|slide|convex|concave|zoom
  transition_speed: default # default|fast|slow
  background_transition: fade
---
```

$box
$caption[color:#58a6ff]{Tip}
$content[padding:0.8em]{
Use `transition: none` for a clean academic presentation where spatial
movement would be distracting.  Use `convex` or `zoom` for demos where
movement helps guide the eye.
}
$endbox

## Navigation and Progress

### Chrome options

#### Controls and progress bar

```yaml
---
reveal:
  controls: true            # show navigation arrows
  controls_layout: bottom-right  # or edges
  progress: true            # bottom progress strip
  slide_number: "c/t"       # current/total; false to hide
---
```

`slide_number` accepts:

| Value | Display |
|---|---|
| `false` | Hidden |
| `true` | Shows slide number |
| `"c"` | Current slide |
| `"c/t"` | Current / Total |
| `"h/v"` | Horizontal.Vertical |
| `"h.v"` | Horizontal.Vertical (dot) |

$note
$content{
For conference talks, c/t is the most useful — it tells both you and
the audience how far through you are.
}
$endnote

#### Canvas size and zoom

```yaml
---
reveal:
  width: 1280        # pixels (or "100%")
  height: 720        # pixels
  margin: 0.04       # fraction of viewport left as border
  min_scale: 0.2     # minimum browser zoom
  max_scale: 2.0     # maximum browser zoom
---
```

Reveal.js scales the presentation to fit the browser window.
`min_scale` and `max_scale` clamp how far it will zoom.

## Plugins

### Available plugins

#### Notes plugin (speaker view)

```yaml
---
reveal:
  plugins:
    - notes
---
```

Press **S** in the browser to open the presenter view.  `$note` environments
are automatically mapped to `<aside class="notes">` when using the reveal backend.

```markdown
#### My Slide

Audience-visible content here.

$note
$content{Only visible in the presenter view.}
$endnote
```

$note
$content{
You are reading this in the presenter view right now!  The notes plugin
was declared in the YAML block at the top of this file.
}
$endnote

#### Math plugin (MathJax 3)

```yaml
---
reveal:
  plugins:
    - math
---
```

When the `math` plugin is active, MaTiSSe loads `RevealMath.MathJax3`
from the reveal.js CDN instead of a standalone MathJax script.

Inline: $\nabla \cdot \mathbf{E} = \rho/\varepsilon_0$

Display:

$$
\oint_{\partial\Sigma} \mathbf{B} \cdot d\boldsymbol{\ell}
  = \mu_0 \left( I_{\rm enc} + \varepsilon_0 \frac{d\Phi_E}{dt} \right)
$$

#### Zoom plugin

```yaml
---
reveal:
  plugins:
    - zoom
---
```

Hold **Alt** (or **Option** on Mac) and click any element to zoom in on it.
Click again to zoom out.  Useful for zooming into code or figures during a live demo.

# Per-Slide Overrides

## Background and Transition

### Slide-level customisation

#### Default slide (no overrides)

This slide uses the global presentation theme — no per-slide YAML block.

The global transition (`slide`) and background (from the `moon` theme) apply.

#### Slide with a background colour
---
overtheme:
  reveal:
    background_color: "#1a1a2e"
    transition: fade
---

This slide has `data-background-color="#1a1a2e"` (deep navy) set via the
per-slide overtheme block, and overrides the global transition to `fade`.

```markdown
#### Slide with a background colour
---
overtheme:
  reveal:
    background_color: "#1a1a2e"
    transition: fade
---

Slide content here.
```

$note
$content{
Per-slide overrides go into the slide's overtheme YAML block under an
`overtheme.reveal` key.  They map directly to HTML data-* attributes on
the <section> element.
}
$endnote

#### Slide with background image
---
overtheme:
  reveal:
    background_color: "#000000"
    background_size: cover
    background_position: center
---

This slide declares `background_size: cover` and `background_position: center`.
Swap in `background_image: img/your_photo.jpg` to place an actual image.

```yaml
overtheme:
  reveal:
    background_image: img/banner.jpg
    background_size: cover
    background_position: center
```

$note
$content{
Images are loaded relative to the output directory, not the source file.
Copy your images to the output directory or use dirs_to_copy in metadata.
}
$endnote

## Auto-Animate

### Smooth transitions between slides

#### List — before
---
overtheme:
  reveal:
    auto_animate: true
---

When `auto_animate: true` is set on **consecutive** slides, reveal.js
smoothly animates matching elements between them:

- Foundation
- Setup

#### List — after
---
overtheme:
  reveal:
    auto_animate: true
---

The list grows and any unchanged items stay in place:

- Foundation
- Setup
- **New item animated in**

$note
$content{
Auto-animate matches elements by their text content or an explicit
data-id attribute.  It works best for lists, headings, and code blocks.
}
$endnote

# Vertical Layout

## 2D Navigation

### Chapter grouping

#### What is vertical layout?

Set `layout: vertical` to map chapters to horizontal steps and their
slides to vertical stacks:

```yaml
---
reveal:
  layout: vertical
---
```

Navigation:
- **→ / ←** moves between chapters (horizontal)
- **↓ / ↑** moves between slides within a chapter (vertical)
- **Space** follows the standard reading order (down then right)

This is ideal for talks with clear chapters that the audience may want
to navigate non-linearly (e.g. backup slides at the end of each chapter).

$note
$content{
With layout: vertical, pressing Space still advances through ALL slides
in reading order.  The 2D structure only matters if the audience/presenter
wants to navigate manually with arrow keys.
}
$endnote

# Slide Decorators

## Headers, Footers, Sidebars

### Decorator schema

#### Header and Footer

Decorators are defined in a `theme.layout` YAML block — the same schema used
by the impress backend:

```yaml
---
theme:
  layout:
    header-1:
      height: 7%
      background: "#0d1117"
      color: "#58a6ff"
      metadata:
        slidetitle:
          float: left
          font-size: 0.85em
        slidenumber:
          float: right
    footer-1:
      height: 4%
      background: "#0d1117"
      metadata:
        authors:
          float: left
---
```

The `metadata:` sub-block maps metadata placeholders to their inline CSS.

$note
$content{
Decorator CSS uses flex layout: the section becomes a flex column, headers
and footers shrink to their declared height, and the slide content fills the
rest.  Use custom_css to fine-tune padding or font sizes.
}
$endnote

#### Sidebar

Add a sidebar with a `sidebar-*` key; set `position: L` (left) or `R`
(right, default):

```yaml
---
theme:
  layout:
    sidebar-1:
      position: L
      width: 18%
      background: "#161b22"
      metadata:
        toc:
          depth: "1"
---
```

When any sidebar is active, the content area is wrapped in a `slide-body`
flex row:

```
section.matisse-decorated
  .slide-header-*
  .slide-body  (flex row)
    .slide-sidebar-*   (left)
    .slide-content     (fill)
    .slide-sidebar-*   (right)
  .slide-footer-*
```

#### Per-slide decorator override

Override any decorator for a single slide using `overtheme.layout`:

```yaml
#### Special Slide
---
overtheme:
  layout:
    header-1:
      height: 5%
      background: "#e74c3c"
      active: yes
      metadata:
        slidetitle:
          float: left
---
Slide with a red header override.
```

Set `active: no` to hide a decorator on a specific slide.

$note
$content{
Per-slide overrides replace the matching decorator by name.  Decorators
not present in the override list remain unchanged.
}
$endnote

# Wrapping Up

## Summary

### What we covered

#### All RevealTheme options at a glance

$box
$caption[color:#58a6ff]{Presentation-level (reveal: block)}
$content[padding:0.8em]{
`theme` · `transition` · `transition_speed` · `background_transition`
· `controls` · `controls_layout` · `progress` · `slide_number`
· `loop` · `center` · `auto_slide`
· `width` · `height` · `margin` · `min_scale` · `max_scale`
· `keyboard` · `touch` · `layout`
· `plugins` · `code_style` · `custom_css`
}
$endbox

$box
$caption[color:#3fb950]{Per-slide (overtheme.reveal: block)}
$content[padding:0.8em]{
`transition` · `background_color` · `background_image`
· `background_size` · `background_position` · `background_video`
· `auto_animate`
}
$endbox

$box
$caption[color:#f0883e]{Slide decorators (theme.layout block)}
$content[padding:0.8em]{
`header-N` · `footer-N` · `sidebar-N` (same schema as impress backend)

Per-slide overrides via `overtheme.layout`.
}
$endbox

Press **O** for the overview mode — every slide at once.

$note
$content{
That covers the complete RevealTheme surface area.

Questions?
}
$endnote
