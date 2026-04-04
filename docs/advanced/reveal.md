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

## Built-in themes

reveal.js ships twelve CSS themes.  List them:

```bash
matisse build --backend reveal --print-themes
```

Available names: `beige`, `black`, `blood`, `dracula`, `league`, `moon`, `night`,
`serif`, `simple`, `sky`, `solarized`, `white`.

Configure the theme in your presentation YAML:

```yaml
---
reveal:
  theme: moon
  transition: slide
---
```

## Transitions

Supported values for `transition`:

| Value | Effect |
|---|---|
| `none` | Instant cut |
| `fade` | Cross-fade |
| `slide` | Horizontal slide (default) |
| `convex` | Convex curve |
| `concave` | Concave curve |
| `zoom` | Zoom in/out |

## YAML configuration reference

All reveal-specific settings live under a `reveal:` key in any YAML block:

```yaml
---
reveal:
  theme: moon           # reveal.js built-in theme name
  transition: slide     # slide transition (see table above)
  highlight_style: monokai.css   # overrides --highlight-style CLI flag
  custom_css: |
    .slide-content { font-size: 1.2em; }
---
```

## Speaker notes

`$note` environments are mapped to reveal.js speaker notes (`<aside class="notes">`).
They are **not visible** to the audience — only to the presenter in the presenter view.

```markdown
#### My Slide

Content visible to the audience.

$note
$content{These words appear only in the presenter view.}
$endnote
```

Open the presenter view by pressing `S` in the browser.

> **Note:** Under the impress backend, `$note` still renders as a visible note box
> on the slide.  The same source produces different output depending on `--backend`.

## Document model mapping

MaTiSSe's hierarchical model maps linearly to reveal.js `<section>` elements:

| MaTiSSe | HTML |
|---|---|
| `$titlepage` | First `<section>` |
| Any slide (`####`) | `<section id="slide-N">` |
| `$note` content | `<aside class="notes">` inside the section |

> Horizontal/vertical nesting (chapters as horizontal groups, slides as vertical stacks)
> is planned for a future release.

## PDF export

reveal.js supports PDF export via Chromium's print dialog.  Append `?print-pdf` to
the URL before printing:

```
file:///path/to/talk/index.html?print-pdf
```

Then print to PDF with "Background graphics" enabled.  For best results use a
Chromium-based browser (Chrome, Edge, Brave).

## Offline mode

`--offline` is **not yet supported** for the reveal backend.  All assets (reveal.js,
MathJax, highlight.js) are loaded from CDN.  A local bundle will be added in a future
release.

## Limitations (current release)

- Reveal-specific YAML settings (`reveal:` block) use default values — YAML parsing
  from the presentation source is not yet wired up to the renderer.
- No horizontal/vertical nesting: all slides are rendered in a flat linear sequence.
- `--offline` not supported.
- `--pdf` flag has no effect (use the `?print-pdf` URL approach instead).
- Per-slide `data-background` and `data-transition` attributes are not yet exposed.
