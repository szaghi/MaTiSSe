---
layout: home

hero:
  name: MaTiSSe
  text: Markdown To Impressive Scientific Slides
  image:
    light: /logo.svg
    dark: /logo-dark.svg
    alt: MaTiSSe, a torii on an unrolled scroll
  tagline: Write scientific presentations in plain Markdown — LaTeX math, syntax highlighting, rich layouts, and your choice of impress.js or reveal.js.
  actions:
    - theme: brand
      text: Quick Start
      link: /guide/quickstart
    - theme: alt
      text: Guide
      link: /guide/
    - theme: alt
      text: View on GitHub
      link: https://github.com/szaghi/MaTiSSe

features:
  - icon:
      light: /icons/markdown.svg
      dark: /icons/markdown-dark.svg
      width: 48
      height: 48
    title: Markdown-first authoring
    details: Write your entire presentation in plain Markdown. MaTiSSe handles heading-to-slide conversion, TOC generation, and multi-level structure (chapters, sections, subsections) automatically.
    link: /guide/quickstart
    linkText: Quick start
  - icon:
      light: /icons/math.svg
      dark: /icons/math-dark.svg
      width: 48
      height: 48
    title: LaTeX math with MathJax 3
    details: Inline and display math via standard `$...$` and `$$...$$` delimiters. MathJax 3 is loaded from CDN by default — zero configuration for scientific content.
    link: /advanced/math
    linkText: Math & LaTeX
  - icon:
      light: /icons/themes.svg
      dark: /icons/themes-dark.svg
      width: 48
      height: 48
    title: YAML theme system
    details: Define every visual detail in YAML theme blocks embedded in the source. Control canvas, headers, footers, sidebars, fonts, and colours. Themes support inheritance with `copy-from-theme` and per-slide overrides.
    link: /reference/themes
    linkText: Theme reference
  - icon:
      light: /icons/highlighting.svg
      dark: /icons/highlighting-dark.svg
      width: 48
      height: 48
    title: Syntax highlighting
    details: Code blocks are highlighted server-side by Pygments with support for 50+ languages and 48 colour schemes. No JavaScript dependency — highlighting CSS is always generated locally.
    link: /advanced/code
    linkText: Code highlighting
  - icon:
      light: /icons/backends.svg
      dark: /icons/backends-dark.svg
      width: 48
      height: 48
    title: Two rendering backends
    details: "`--backend impress` (default) gives full impress.js 3D canvas effects and spatial transitions. `--backend reveal` switches to reveal.js: speaker notes, overview mode, and built-in PDF export — same Markdown source, one flag."
    link: /advanced/reveal
    linkText: reveal.js guide
  - icon:
      light: /icons/callouts.svg
      dark: /icons/callouts-dark.svg
      width: 48
      height: 48
    title: Callouts & semantic blocks
    details: "Draw attention with five callout types: note, tip, warning, caution, important. Each has a coloured border, icon, and optional title."
    link: /advanced/callouts
    linkText: Callout blocks
  - icon:
      light: /icons/theorems.svg
      dark: /icons/theorems-dark.svg
      width: 48
      height: 48
    title: Theorems & proofs
    details: Number theorems, lemmas, corollaries, definitions, examples, and more with auto-incrementing counters. Cross-reference any block with `@PREFIX-id` syntax.
    link: /advanced/theorems
    linkText: Theorems & proofs
  - icon:
      light: /icons/diagrams.svg
      dark: /icons/diagrams-dark.svg
      width: 48
      height: 48
    title: Diagrams
    details: Embed Mermaid flowcharts, sequence diagrams, Gantt charts, and Graphviz dot graphs directly in slide source. CDN scripts are injected automatically.
    link: /advanced/diagrams
    linkText: Diagrams
  - icon:
      light: /icons/open-source.svg
      dark: /icons/open-source-dark.svg
      width: 48
      height: 48
    title: Free and open source
    details: Released under the GNU GPL v3 license. Free to use, study, modify, and distribute. Contributions welcome.
---

## Why MaTiSSe?

Scientific presentations demand more than a typical slide tool offers — inline equations, code listings, figures with captions, precise layouts, and reproducible output that lives in version control alongside the paper.

**MaTiSSe bridges that gap.** Write your talk in Markdown, embed LaTeX equations and code blocks as you would in a paper, and let MaTiSSe generate a fully self-contained HTML presentation — powered by **impress.js** (3D canvas, spatial transitions) or **reveal.js** (speaker notes, overview mode, PDF export), selectable with a single flag.

```bash
# Install
pipx install MaTiSSe.py

# Generate a sample presentation to start from
matisse build --sample mytalk.md

# Build
matisse build -i mytalk.md -o mytalk/
```

A minimal slide source:

```markdown
---
title:   My Talk
authors: Stefano Zaghi
date:    April 2026
---

---
theme:
  layout:
    slide:
      width: '900px'
      height: '600px'
---

# Introduction

## Overview

#### First Slide

Content goes here. Use $title to reference metadata, $math with $E = mc^2$.
```

## Author

**[Stefano Zaghi](https://github.com/szaghi)** · stefano.zaghi@gmail.com
> *Chief Yak Shaver & Accidental Research Scientist, HPC farmer* at CNR-IAC, National Research Council of Italy

## Copyrights

MaTiSSe is an open source project distributed under the [GPL v3](http://www.gnu.org/licenses/gpl-3.0.html) license.

© [Stefano Zaghi](https://github.com/szaghi)
