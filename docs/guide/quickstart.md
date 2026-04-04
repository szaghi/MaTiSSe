# Quick Start

## Generate a sample presentation

The fastest way to get started is to let MaTiSSe generate a working example:

```bash
matisse --sample mytalk.md
```

To start from a built-in theme, pass `--theme` as well:

```bash
matisse --sample mytalk.md --theme beamer-madrid
```

List all available built-in themes:

```bash
matisse --print-themes
```

This writes `mytalk.md` — a fully annotated source file showing all major features. Build it immediately:

```bash
matisse -i mytalk.md -o mytalk/
```

Open `mytalk/index.html` in a browser. Use arrow keys or spacebar to navigate slides.

## Write your own

A minimal presentation source:

```markdown
---
title:    My Talk
subtitle: A Subtitle
authors:  Stefano Zaghi
---
---
theme_slide_global:
  width:  900px
  height: 600px
  data-transition-duration: 500
---

$titlepage

# Introduction

## Overview

#### First Slide

Write slide content here.

Inline math: $E = mc^2$

Display math:

$$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$

#### Second Slide

Code listing:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```
```

Build:

```bash
matisse -i source.md -o output/
```

## Common options

| Option | Effect |
|---|---|
| `-i FILE` | Input Markdown file |
| `-o DIR` | Output directory |
| `--offline` | Bundle JS/CSS locally instead of using CDN |
| `--pdf` | PDF-friendly output (no impress.js animations) |
| `--print-themes` | List all built-in themes |
| `--print-highlight-styles` | List all highlight.js styles |
| `--sample FILE` | Write a sample source file |

## List available themes

```bash
matisse --print-themes
```

Apply a built-in theme by adding a `theme` key to your metadata block:

```yaml
---
title: My Talk
theme: dark
---
```

## Next steps

- [Markdown Syntax reference](/reference/markdown-syntax) — all MaTiSSe extensions
- [Theme YAML reference](/reference/themes) — full theme customisation
- [Math & LaTeX](/advanced/math) — equation authoring tips
- [Figures, Boxes, Tables](/advanced/figures) — rich content environments
