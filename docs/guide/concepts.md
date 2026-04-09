# Core Concepts

This page explains how MaTiSSe maps Markdown source to a presentation.
Understanding this mental model makes every other part of the documentation
fall into place.

---

## The document hierarchy

MaTiSSe organises a presentation as a four-level tree:

```
Presentation
├── Chapter          (#  heading)
│   ├── Section      (## heading)
│   │   ├── Subsection  (### heading)
│   │   │   ├── Slide   (#### heading)
│   │   │   └── Slide   (#### heading)
│   │   └── Subsection
│   └── Section
└── Chapter
```

```markdown
# Chapter one           ← Chapter
## Introduction         ← Section
### Motivation          ← Subsection
#### Why MaTiSSe?       ← Slide (starts a new slide frame)

Content of the slide goes here.

#### Key features       ← Another slide
```

Chapters, sections, and subsections are **structural** — they do not produce
visible slide content on their own.  They influence:

- The automatically generated table of contents (`$toc`)
- The auto-numbered metadata variables (`$chapternumber`, `$sectionnumber`, etc.)
- The currently active TOC entry highlighted in sidebars

Only `####` headings start slide frames containing visible content.

> **Content headings inside a slide:** Use `#####` and `######` for subsection
> headings *within* slide content, or raw HTML `<h1>`–`<h3>` for presentation
> headings that don't create hierarchy nodes.

---

## Slide anatomy

Each slide frame is composed of several regions:

```
Infinite Canvas
┌────────────────────────────────────┐
│         header-1                   │
├────────────────────────────────────┤
│         header-2                   │
├────────────────────────────────────┤
│         ...                        │
├────────────────────────────────────┤
│         header-N                   │
├─┬─┬─┬──┬───────────────────┬─┬─┬─┬─┤
│s│s│.│s │                   │s│s│.│s│
│i│i│.│i │                   │i│i│.│i│
│d│d│.│d │                   │d│d│.│d│
│e│e│ │e │   content area    │e│e│ │e│
│b│b│ │b │   (Markdown body) │b│b│ │b│
│a│a│ │a │                   │a│a│ │a│
│r│r│ │r │                   │r│r│ │r│
│L│L│ │L │                   │R│R│ │R│
│1│2│ │N │                   │1│2│ │N│
├─┴─┴─┴──┴───────────────────┴─┴─┴─┴─┤
│         footer-1                   │
├────────────────────────────────────┤
│         footer-2                   │
├────────────────────────────────────┤
│         ...                        │
├────────────────────────────────────┤
│         footer-N                   │
└────────────────────────────────────┘
```

- **Headers and footers** — horizontal bands stacking above and below the content, optional
- **Sidebars** — vertical bands on the left or right edge, optional
- **Content area** — the remaining rectangle where slide Markdown is rendered

All of these are defined in the [theme YAML](/reference/themes).  Each band can
display [metadata placeholders](/reference/themes#metadata-placeholders) such as
`slidetitle`, `slidenumber`, `sectiontitle`, `toc`, and `logo`.

---

## Theme system

A **theme** is a YAML block that controls every visual aspect of the presentation
outside the slide content itself.

```yaml
---
theme:
  palette:    # named colour variables ($accent, $bg, …)
  canvas:     # body background behind all slides
  lists:      # bullet and number list styling
  toc:        # table of contents styling
  layout:     # slide dimensions, headers, footers, sidebars, content
  entities:   # $box, $note, $figure, $table, $video environments
  code:       # fenced code block appearance and Pygments style
---
```

Themes are applied globally.  Any individual slide can override any theme section
using an **overtheme** block placed immediately after its `####` heading:

```markdown
#### My title slide
---
overtheme:
  copy-from-theme: true
  layout:
    header-1:
      active: 'no'
    content:
      background: 'black'
      color: 'white'
---
```

`copy-from-theme: true` inherits the full global theme before applying the
overrides.  Without it, the slide starts from bare defaults.

---

## Metadata system

Presentation metadata is defined in the first YAML block of the source file.
It drives two things:

1. **Decorator placeholders** — `$slidetitle`, `$authors`, `$toc`, etc. inside
   theme header/footer/sidebar definitions
2. **Content interpolation** — `$key[CSS]` syntax inside slide body text

```yaml
---
title:    My Conference Talk
authors:  ['Alice Smith', 'Bob Jones']
date:     April 2026
logo:     images/logo.png
max_time: 25
dirs_to_copy: ['images']
---
```

Auto-generated metadata (computed at build time, not settable by you):

| Key | Content |
|---|---|
| `slidenumber` | Current slide number |
| `total_slides_number` | Total slide count |
| `sectiontitle` / `sectionnumber` | Active section |
| `subsectiontitle` / `subsectionnumber` | Active subsection |
| `chaptertitle` / `chapternumber` | Active chapter |
| `slidetitle` | Active slide title |
| `toc` | Full TOC as HTML |
| `timer` | Countdown from `max_time` |

---

## Special slides

### Title page

`$titlepage` generates a slide pre-filled with metadata.  Place it at the start
of your source, typically with an overtheme that removes decorators:

```markdown
#### $titlepage
---
overtheme:
  copy-from-theme: true
  layout:
    header-1:
      active: 'no'
    footer-1:
      active: 'no'
---
```

Use `$box`/`$endbox` environments inside the title page body to compose a
structured layout from metadata values:

```markdown
#### $titlepage

$box
$style[width:100%;background:#4788B3;]
$content[color:white;text-align:center;]{
$title[font-size:200%;]
$subtitle[font-size:120%;]
}
$endbox
```

`$titlepage[plain]` generates the same slide but without any inherited theme —
useful when the built-in theme's title page layout is completely custom.

---

## File inclusion

`$include(path/to/file)` substitutes the contents of an external file before
parsing begins.  Use it to split large presentations or share a common theme:

```markdown
$include(theme.yaml)
$include(metadata.yaml)

# Chapter 1

#### Slide one
…
```

Inclusion is resolved in a single pass — there is no recursive inclusion.

---

## Output structure

Running `matisse -i talk.md -o talk/` produces:

```
talk/
├── index.html          # self-contained presentation
├── css/
│   ├── matisse.css     # generated from theme YAML
│   └── pygments.css    # generated from code.style setting
├── js/
│   └── countdown.js    # presentation timer utility
└── images/             # copied from dirs_to_copy
```

With `--offline`, `js/` also contains impress.js and MathJax bundles.
Syntax highlighting CSS is always local regardless of offline mode.

---

## Rendering backends

MaTiSSe supports two output backends, selected with `--backend`:

| Backend | Default | Strengths |
|---|---|---|
| `impress` | ✓ | 3D canvas, spatial transitions, Substep plugin |
| `reveal` | — | Speaker notes, overview mode, PDF export via browser |

Both backends use the same Markdown source and theme YAML.  Some features
(e.g. `$substep`, 3D positioning) are impress.js only; others (speaker notes,
`{.fragment}`) are reveal.js only.

---

## Dive deeper

- [Usage](/guide/usage) — full walkthrough with annotated examples for every feature
- [Theme YAML reference](/reference/themes) — every key in the theme schema
- [Metadata reference](/reference/metadata) — all metadata keys and interpolation syntax
- [Feature Matrix](/reference/feature-matrix) — every feature at a glance, with backend support
- [Themes In Depth](/advanced/themes) — real-world theme recipes and advanced layout patterns
- [Callouts, Theorems, Diagrams](/advanced/) — advanced scientific content environments
