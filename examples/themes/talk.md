---
metadata:
  - title:       "Scientific Presentations with MaTiSSe"
  - subtitle:    "A tour of the built-in themes"
  - authors:
    - Jane Smith
    - John Doe
  - authors_short:
    - J. Smith
    - J. Doe
  - emails:
    - jane.smith@example.edu
    - john.doe@example.edu
  - affiliations:
    - Department of Computer Science, Example University
    - Institute for Scientific Computing, Example Institute
  - affiliations_short:
    - CS Dept., Example University
    - ISC, Example Institute
  - date:             "2026"
  - conference:       "MaTiSSe Theme Gallery"
  - conference_short: "MTG 2026"
  - session:          "Built-in themes showcase"
  - max_time:         25
  - toc_depth:        2
---

# Introduction

## What is MaTiSSe?

### Overview

#### $titlepage

$box
$style[width:90%;margin:2% auto;padding:4%;text-align:center;border-radius:10px;]
$content{
$title[display:block;font-size:200%;font-weight:bold;padding-bottom:2%]
$subtitle[display:block;font-size:120%;padding-bottom:4%]
$authors[display:block;font-size:110%]
$affiliations[display:block;font-size:90%;padding-top:1%]
$conference[display:block;font-size:90%;padding-top:3%]
$date[display:block;font-size:85%;]
}
$endbox

#### Definition

**MaTiSSe** (_Markdown To Impressive Scientific Slides_) is a CLI tool that
compiles plain Markdown source into self-contained HTML presentations.

Key properties:

+ Write in **Markdown** — no HTML boilerplate, no LaTeX preamble
+ **LaTeX equations** rendered by MathJax 3
+ **Syntax-highlighted** code via highlight.js 11
+ Rich **scientific environments**: `$figure`, `$box`, `$note`, `$table`, `$columns`
+ **Two backends**: impress.js (3D canvas) and reveal.js (speaker notes, PDF export)
+ **Seven built-in themes** — this presentation demonstrates all of them

```bash
# Build this presentation with any built-in theme
matisse build -i talk.md -o out/ --theme <theme-name>
```

## Built-in Themes

### Theme Gallery

#### Theme overview

$table
$caption{MaTiSSe built-in themes}
$content{
| Theme            | Layout                     | Palette                  |
|------------------|----------------------------|--------------------------|
| beamer-antibes   | Triple header              | Navy / white             |
| beamer-berkely   | Left sidebar + header      | Blue / white             |
| beamer-berlin    | Triple header + footer     | Navy / white             |
| beamer-madrid    | Header + rich footer       | Blue / white             |
| matisse          | Right sidebar + header + footer | Sky-blue / white   |
| sapienza         | Header + footer            | Crimson / white          |
| solarized-dark   | Left sidebar + header + footer | Solarized dark       |
}
$endtable

$note
$caption{How to switch themes}
$content{
Pass `--theme <name>` to `matisse build`. The theme is applied on top of
the source — no changes to the Markdown file are needed.
}
$endnote

# Core Features

## Scientific Content

### Mathematical Typesetting

#### LaTeX Equations

MaTiSSe renders LaTeX via **MathJax 3** — inline `$…$` and display `$$…$$`.

The **quadratic formula**:

$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$

**Euler's identity** — often cited as the most beautiful equation in mathematics:

$$e^{i\pi} + 1 = 0$$

**Maxwell's equations** (differential form, SI units):

$$\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}, \qquad
  \nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0\varepsilon_0\,\frac{\partial \mathbf{E}}{\partial t}$$

### Code and Environments

#### Syntax-highlighted Code

highlight.js 11 colours code blocks for dozens of languages:

```python
import math

def newton_sqrt(x: float, tol: float = 1e-10) -> float:
    """Compute sqrt(x) via Newton-Raphson iteration."""
    if x < 0:
        raise ValueError("x must be non-negative")
    guess = x / 2.0
    while abs(guess * guess - x) > tol:
        guess = (guess + x / guess) / 2.0
    return guess

print(f"sqrt(2) ≈ {newton_sqrt(2):.15f}")
print(f"error   = {abs(newton_sqrt(2) - math.sqrt(2)):.2e}")
```

#### Environments: Box and Columns

$box
$caption{Mean Value Theorem}
$content[padding:0.5em]{
Let $f : [a, b] \to \mathbb{R}$ be continuous on $[a,b]$ and differentiable
on $(a,b)$.  Then there exists $c \in (a, b)$ such that

$$f'(c) = \frac{f(b) - f(a)}{b - a}.$$
}
$endbox

$columns
$column[width:48%]
**Ordered list**

1. First item
2. Second item
3. Third item — with inline math $\sigma(x) = \frac{1}{1+e^{-x}}$
$column[width:48%]
**Unordered list**

+ Markdown-first workflow
+ Version control friendly
+ Self-contained HTML output
+ Works offline with `--offline`
$endcolumns

## Performance and Deployment

### Output Modes

#### Deployment Options

$columns
$column[width:48%]
**Online mode (default)**

Assets loaded from CDN:

- impress.js 2 from jsDelivr
- MathJax 3 from jsDelivr
- highlight.js 11 from cdnjs

Minimal output directory size.
$column[width:48%]
**Offline mode** (`--offline`)

All assets bundled locally:

- Works in air-gapped environments
- No internet connection required at display time
- Larger output directory
$endcolumns

$note
$caption{PDF output}
$content{
Pass `--pdf` to disable impress.js animations — the resulting presentation
prints cleanly to PDF from the browser.
}
$endnote

# Conclusions

## Summary

### Key Takeaways

#### What we covered

$box
$caption{Summary}
$content[padding:0.5em]{
1. **MaTiSSe** compiles Markdown to self-contained HTML presentations
2. **Seven built-in themes** — each tailored for a different look
3. **LaTeX math** via MathJax 3, **code highlighting** via highlight.js 11
4. **Scientific environments**: `$box`, `$note`, `$table`, `$columns`, `$figure`
5. **Two backends**: impress.js (3D) and reveal.js (speaker notes, PDF)
6. **Offline** and **PDF** modes for deployment flexibility
}
$endbox

#### Get started

```bash
# Install
pip install MaTiSSe.py

# Generate a sample and build it
matisse build --sample mytalk.md --theme beamer-madrid
matisse build -i mytalk.md -o mytalk/
```

Full documentation: **[szaghi.github.io/MaTiSSe](https://szaghi.github.io/MaTiSSe/)**

Thank you — questions?
