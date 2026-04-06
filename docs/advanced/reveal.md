# reveal.js Backend

MaTiSSe supports **reveal.js** as an alternative rendering backend alongside the
default impress.js engine.  Switch to it with a single flag:

```bash
matisse build -i talk.md -o talk/ --backend reveal
```

The same Markdown source, metadata, and environments (`$figure`, `$box`, `$columns`,
…) work with both backends — only the HTML assembly and theme layers differ.

## Why reveal.js?

| Feature | impress.js | reveal.js |
|---|---|---|
| Spatial 3D canvas | ✅ | ❌ |
| Presenter view / speaker notes | ❌ | ✅ |
| Overview mode | ❌ | ✅ |
| Fragment (step) animations | limited | ✅ |
| Built-in PDF export | manual | ✅ (Chromium `?print-pdf`) |
| Plugin ecosystem | small | large |
| Active development | slow | active |

Use impress when you need Prezi-style 3D effects; use reveal for everything else.

## Quick start

```bash
# Generate a sample and build it with reveal.js
matisse build --sample mytalk.md
matisse build -i mytalk.md -o mytalk/ --backend reveal
# Open mytalk/index.html in your browser
```

## YAML configuration reference

All reveal-specific settings live under a `reveal:` key in any YAML block
in your presentation source.

```yaml
---
reveal:
  # Built-in CDN theme (default: black)
  theme: moon

  # Slide transition (default: slide)
  transition: slide          # none|fade|slide|convex|concave|zoom

  # Transition speed (default: default)
  transition_speed: default  # default|fast|slow

  # Navigation arrows (default: true)
  controls: true
  controls_layout: bottom-right  # bottom-right|edges

  # Progress bar (default: true)
  progress: true

  # Slide number display (default: false)
  slide_number: "c/t"        # false|true|c|c/t|h/v|h.v

  # Loop the deck (default: false)
  loop: false

  # Vertically centre slide content (default: true)
  center: true

  # Auto-advance in ms, 0 = disabled (default: 0)
  auto_slide: 0

  # Slide canvas size (default: 960 × 700)
  width: 1280
  height: 720

  # Viewport margin as a fraction (default: 0.04)
  margin: 0.04

  # Zoom limits (default: 0.2 – 2.0)
  min_scale: 0.2
  max_scale: 2.0

  # Background transition style (default: fade)
  background_transition: fade  # same values as transition

  # Keyboard and touch navigation (default: true each)
  keyboard: true
  touch: true

  # Slide layout mode (default: linear)
  layout: linear             # linear|vertical

  # Plugins loaded from CDN (default: none)
  plugins:
    - notes    # speaker notes — press S in browser
    - zoom     # click-to-zoom
    - search   # in-deck text search
    - math     # RevealMath.MathJax3 (replaces standalone MathJax)

  # Pygments code-highlight style (overrides --code-style CLI flag)
  code_style: monokai

  # Raw CSS injected into <head> as an inline <style> block
  custom_css: |
    .reveal h1 { font-variant: small-caps; }
---
```

## Built-in themes

reveal.js ships twelve CSS themes.  List them:

```bash
matisse build --backend reveal --print-themes
```

| Name | Style |
|---|---|
| `black` | Dark grey background (default) |
| `white` | Clean white |
| `moon` | Dark blue |
| `sky` | Light blue |
| `beige` | Warm beige |
| `night` | High contrast dark |
| `serif` | Serif typography |
| `solarized` | Solarized palette |
| `dracula` | Dracula colours |
| `blood` | Dark red accents |
| `league` | Greyscale |
| `simple` | Minimal |

## Transitions

`transition` and `background_transition` share the same set of values:

| Value | Effect |
|---|---|
| `none` | Instant cut |
| `fade` | Cross-fade |
| `slide` | Horizontal slide (default for `transition`) |
| `convex` | Convex curve |
| `concave` | Concave curve |
| `zoom` | Zoom in/out |

Combine with `transition_speed: fast` or `slow` for fine control.

## Slide numbers

`slide_number` accepts a boolean or a format string:

| Value | Display |
|---|---|
| `false` | Hidden (default) |
| `true` | Reveal default format |
| `"c"` | Current slide number |
| `"c/t"` | Current / Total |
| `"h/v"` | Horizontal.Vertical |
| `"h.v"` | Horizontal.Vertical (dot) |

## Slide layout: linear vs vertical

The default `layout: linear` maps every MaTiSSe slide to a flat sequence
of `<section>` elements — pure left/right navigation.

With `layout: vertical`, chapters become horizontal groups and their slides
stack vertically inside each group:

- **→ / ←** moves between chapters
- **↓ / ↑** moves between slides within a chapter
- **Space** follows the natural reading order (down then right)

```yaml
---
reveal:
  layout: vertical
---
```

## Plugins

Plugins are loaded from the reveal.js 5 CDN.  Add them to the `plugins` list:

```yaml
---
reveal:
  plugins:
    - notes
    - zoom
    - search
    - math
---
```

### `notes` — speaker view

Enables the presenter view.  Press **S** in the browser to open it.

`$note` environments automatically render as `<aside class="notes">` when
using the reveal backend — they are invisible to the audience:

```markdown
#### My Slide

Audience-visible content.

$note
$content{Only visible in the presenter view (press S).}
$endnote
```

> Under the impress backend, `$note` still renders as a visible note box.

### `zoom` — click-to-zoom

Hold **Alt** (or **Option** on Mac) and click any element to zoom into it.
Click again to reset.

### `search` — in-deck search

Press **Ctrl+Shift+F** to open a search box that finds text across all slides.

### `math` — MathJax 3 via reveal plugin

When active, `RevealMath.MathJax3` is loaded instead of the standalone
MathJax script block.  The inline/display math delimiters (`$…$` and `$$…$$`)
are configured automatically.

```yaml
reveal:
  plugins:
    - math
```

> **Note:** Do not use the `highlight` plugin — MaTiSSe pre-processes code
> blocks with Pygments, producing HTML that conflicts with reveal's own
> highlight.js pass.

## Slide decorators

The reveal backend supports the same `theme.layout` decorator schema as the
impress backend: persistent **headers**, **footers**, and **sidebars** that
appear on every slide and can show dynamic metadata values.

### Basic usage

Place a `theme.layout` block in any YAML section of your source file:

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
          padding-left: 1em
        slidenumber:
          float: right
          padding-right: 1em
    footer-1:
      height: 4%
      background: "#0d1117"
      color: "#8b949e"
      metadata:
        authors:
          float: left
          font-size: 0.65em
          padding-left: 1em
---
```

Each decorator key (`header-N`, `footer-N`, `sidebar-N`) accepts:

| Key | Description |
|---|---|
| `height` | Fixed height for headers/footers (CSS value, e.g. `7%`) |
| `width` | Fixed width for sidebars (CSS value, e.g. `18%`) |
| `position` | Sidebar placement: `L` (left) or `R` (right, default) |
| `active` | `yes` / `no` — whether to render this decorator (default `yes`) |
| `metadata` | Sub-dict mapping metadata names to their inline CSS |
| *any other key* | Treated as a raw CSS property (e.g. `background`, `color`) |

Multiple decorators of the same kind are supported (`header-1`, `header-2`, …)
and are rendered in alphabetical order.

### Sidebar layout

When at least one sidebar is defined the slide body is wrapped in a flex-row
container:

```
section.matisse-decorated          ← flex column
  .slide-header-*                  ← fixed height
  .slide-body                      ← flex row, fills remaining height
    .slide-sidebar-*  (left)       ← fixed width
    .slide-content                 ← fills remaining width
    .slide-sidebar-*  (right)      ← fixed width
  .slide-footer-*                  ← fixed height
```

### Metadata placeholders

The `metadata` sub-block maps any MaTiSSe metadata name to a CSS string that
controls its inline display style.  Available metadata names include
`slidetitle`, `slidenumber`, `chaptertitle`, `sectiontitle`, `authors`,
`conference`, `toc`, and all other names defined in your front matter.

```yaml
metadata:
  slidetitle:
    float: left
    font-size: 0.9em
    padding-left: 1em
```

This produces a `$slidetitle[float:left;font-size:0.9em;padding-left:1em;]`
placeholder that is resolved to the current slide title at render time.

### Per-slide decorator overrides

Use `overtheme.layout` to override any decorator for a single slide:

```markdown
#### Special Slide
---
overtheme:
  layout:
    header-1:
      height: 5%
      background: "#e74c3c"
      metadata:
        slidetitle:
          float: left
---
Slide with a red header.
```

Overrides replace the named decorator; all other decorators remain unchanged.
Set `active: no` to hide a specific decorator on one slide.

## Per-slide overrides

Individual slides can override the global theme via a YAML block placed
directly inside the slide content (between `---` markers):

```markdown
#### Slide with dark background
---
overtheme:
  reveal:
    background_color: "#1a1a2e"
    transition: zoom
---

Slide content here.
```

All per-slide keys map to HTML `data-*` attributes on the `<section>` element:

| YAML key | HTML attribute | Notes |
|---|---|---|
| `transition` | `data-transition` | overrides global transition for this slide |
| `background_color` | `data-background-color` | CSS colour value |
| `background_image` | `data-background-image` | image URL (relative to output dir) |
| `background_size` | `data-background-size` | e.g. `cover`, `contain` |
| `background_position` | `data-background-position` | e.g. `center` |
| `background_video` | `data-background-video` | video URL |
| `auto_animate` | `data-auto-animate` | set to `true` to enable between adjacent slides |

### Auto-animate example

Set `auto_animate: true` on two **consecutive** slides.  Reveal.js smoothly
animates matching elements (same text content or explicit `data-id`):

```markdown
#### Step 1
---
overtheme:
  reveal:
    auto_animate: true
---

- Item A

#### Step 2
---
overtheme:
  reveal:
    auto_animate: true
---

- Item A
- Item B (animated in)
```

## Custom CSS

`custom_css` is raw CSS injected as an inline `<style>` block in `<head>`.
Use it to fine-tune the chosen theme without creating a separate file:

```yaml
reveal:
  custom_css: |
    .reveal h1 { text-transform: none; }
    .reveal .slide-content { font-size: 0.9em; }
```

## Speaker notes

`$note` environments are mapped to reveal.js speaker notes:

```markdown
#### My Slide

Content visible to the audience.

$note
$content{These words appear only in the presenter view.}
$endnote
```

Open the presenter view by pressing **S** in the browser.
Activate the `notes` plugin to enable this feature.

## PDF export

Append `?print-pdf` to the URL and print from a Chromium-based browser
(Chrome, Edge, Brave) with **Background graphics** enabled:

```
file:///path/to/talk/index.html?print-pdf
```

For best results set the page size to match `width` × `height` in your theme.

## Offline mode

`--offline` is **not yet supported** for the reveal backend.  reveal.js and
MathJax are loaded from CDN.  Pygments syntax highlighting (Pygments CSS)
is always generated locally regardless of this flag.

## Complete example

See `examples/reveal-advanced/advanced.md` in the MaTiSSe repository for a
self-contained presentation that exercises every RevealTheme option.

```bash
matisse build -i examples/reveal-advanced/advanced.md \
              -o /tmp/reveal-advanced/ \
              --backend reveal
```
