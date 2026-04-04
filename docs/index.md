---
layout: home

hero:
  name: MaTiSSe
  text: Markdown To Impressive Scientific Slides
  tagline: Write scientific presentations in plain Markdown — LaTeX math, syntax highlighting, rich layouts, and impress.js animations.
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
  - icon: 📝
    title: Markdown-first authoring
    details: Write your entire presentation in plain Markdown. MaTiSSe handles heading-to-slide conversion, TOC generation, and multi-level structure (chapters, sections, subsections) automatically.
    link: /guide/quickstart
    linkText: Quick start
  - icon: 🧮
    title: LaTeX math with MathJax 3
    details: Inline and display math via standard `$...$` and `$$...$$` delimiters. MathJax 3 is loaded from CDN by default — zero configuration for scientific content.
    link: /advanced/math
    linkText: Math & LaTeX
  - icon: 🎨
    title: YAML theme system
    details: Define every visual detail in YAML theme blocks embedded in the source. Control canvas, headers, footers, sidebars, fonts, and colours. Themes support inheritance with `copy-from-theme` and per-slide overrides.
    link: /reference/themes
    linkText: Theme reference
  - icon: 💻
    title: Syntax highlighting
    details: Code blocks are highlighted by highlight.js 11 with support for dozens of languages. Choose from all built-in highlight.js styles.
    link: /advanced/code
    linkText: Code highlighting
  - icon: 🌐
    title: CDN-by-default, offline-ready
    details: impress.js, MathJax, and highlight.js are loaded from CDN by default for minimal output size. Pass `--offline` to bundle everything locally for air-gapped environments.
    link: /advanced/offline
    linkText: Offline mode
  - icon: 🆓
    title: Free and open source
    details: Released under the GNU GPL v3 license. Free to use, study, modify, and distribute. Contributions welcome.
---

## Why MaTiSSe?

Scientific presentations demand more than a typical slide tool offers — inline equations, code listings, figures with captions, precise layouts, and reproducible output that lives in version control alongside the paper.

**MaTiSSe bridges that gap.** Write your talk in Markdown, embed LaTeX equations and code blocks as you would in a paper, and let MaTiSSe generate a fully self-contained HTML presentation powered by impress.js.

```bash
# Install
pip install matisse

# Generate a sample presentation to start from
matisse --sample mytalk.md

# Build
matisse -i mytalk.md -o mytalk/
```

A minimal slide source looks like this:

```markdown
---
title:   My Talk
authors: Stefano Zaghi
---
---
theme_slide_global:
  width:  900px
  height: 600px
---

# Introduction

## Overview

#### First Slide

Content with inline math $E = mc^2$ and a code block:

```python
print("Hello, MaTiSSe!")
```
```

## Author

**Stefano Zaghi** — [stefano.zaghi@cnr.it](mailto:stefano.zaghi@cnr.it) · [GitHub](https://github.com/szaghi)

## Copyrights

MaTiSSe is an open source project distributed under the [GPL v3](http://www.gnu.org/licenses/gpl-3.0.html) license.
