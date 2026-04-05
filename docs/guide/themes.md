# Themes

A **theme** controls everything visual about a MaTiSSe presentation that is not the slide
content itself: the canvas background, slide dimensions and colours, headers, footers,
sidebars, list bullets, TOC appearance, environment styling, and code highlighting.

---

## Built-in themes

MaTiSSe ships eight ready-to-use themes. Apply one with the `--theme` flag:

```bash
matisse build -i talk.md --theme dracula
```

Or list all available names:

```bash
matisse build --print-themes
```

| Name | Layout | Colour scheme |
|---|---|---|
| `matisse` | Right sidebar + header + footer | Blue gradient |
| `sapienza` | Header + footer | Sapienza red |
| `dracula` | Left sidebar + header + footer | Dracula dark |
| `solarized-dark` | Left sidebar + header + footer | Solarized dark |
| `beamer-antibes` | Three stacked headers | Beamer blue |
| `beamer-berkely` | Left sidebar + header | Beamer blue |
| `beamer-berlin` | Three stacked headers + two footers | Beamer dark blue |
| `beamer-madrid` | Header + footer | Beamer blue |

Each built-in theme may also set default metadata (title page layout, logo placement) via
companion `metadata.yaml` and `titlepage.md` files — these are injected automatically.

---

## Writing your first custom theme

A theme block is a YAML document embedded directly in your source file:

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

Place it anywhere in the source — conventionally at the top, before any slide content.
Multiple `theme:` blocks in the same file are merged (later values override earlier ones).

All sections are optional. Include only what you want to override.

---

## The seven theme sections

A theme can contain up to seven top-level sections:

```yaml
---
theme:
  palette:    # named colour variables — reference with $varname
  canvas:     # full-viewport body background
  lists:      # ordered and unordered list styling
  toc:        # table of contents styling
  layout:     # slide structure (dimensions, headers, footers, sidebars, content)
  entities:   # box, note, table, figure, video environments
  code:       # fenced code block styling and Pygments theme
---
```

For a minimal presentation you will typically only need `canvas` and `layout`.
A typical conference talk uses all seven.

---

## Keeping themes in a separate file

For reusable or long themes, put the YAML in a separate file and include it:

```markdown
$include(theme.yaml)
$include(metadata.yaml)

# Chapter one
...
```

`theme.yaml` is a plain YAML file — no surrounding markdown, no `---` delimiters needed.
The `$include` directive is processed before parsing, so the theme is available to all slides.

---

## Per-slide overrides

Any individual slide can override the global theme using an `overtheme:` block placed
immediately after its `####` heading:

```markdown
#### My special slide
---
overtheme:
  layout:
    slide:
      border-radius: '50%'
    content:
      padding: '15% 20%'
      font-size: '180%'
---

Slide content here.
```

Use `copy-from-theme: true` to inherit the full global theme first and then patch it:

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

Without `copy-from-theme`, the overtheme starts from scratch (all layout defaults).

---

## Next steps

- **[Advanced: Themes](/advanced/themes)** — comprehensive walkthrough of every section,
  palette variables, decorator metadata, and real-world examples.
- **[Reference: Theme YAML](/reference/themes)** — complete schema specification.
