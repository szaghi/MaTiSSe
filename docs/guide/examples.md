# Examples

## Full examples (repository)

The repository ships three ready-to-build example presentations under the
`examples/` directory.  Clone the repo, install MaTiSSe, then run the
commands below from the **repository root**.

```bash
git clone https://github.com/szaghi/MaTiSSe.git
cd MaTiSSe
pip install -e .
```

### getting-started (impress.js)

A comprehensive feature tour of MaTiSSe — the same presentation that was
used to write the original documentation.  Demonstrates the full impress.js
theme system: canvas, headers, footers, sidebars, overtheme overrides, TOC
slides, figures, boxes, tables, notes, columns, video, and code listings.

```bash
matisse build \
  -i examples/getting-started/getting_started.md \
  -o examples/getting-started/out/ \
  --toc-at-subsec-beginning 2
```

Open `examples/getting-started/out/index.html` in a browser.
Navigate with arrow keys or spacebar; use the mouse to pan the 3D canvas.

> **Note:** this example uses `$include()` internally (for `metadata.yaml`
> and `theme.yaml`).  The paths are relative to the working directory, so
> the command must be run from the **repo root** as shown above.

### reveal-quickstart (reveal.js)

A minimal, heavily annotated introduction to the reveal.js backend.
Covers slide structure, LaTeX math, syntax-highlighted code, the `$box`
and `$columns` environments, and speaker notes via `$note`.

```bash
matisse build \
  -i examples/reveal-quickstart/quickstart.md \
  -o examples/reveal-quickstart/out/ \
  --backend reveal
```

Open `examples/reveal-quickstart/out/index.html` in a browser.

| Key | Action |
|-----|--------|
| `Space` / `→` | Next slide |
| `←` | Previous slide |
| `O` | Overview mode |
| `S` | Presenter view (speaker notes) |
| `F` | Full screen |

> Press **S** to open the presenter view and read the speaker notes — each
> `$note` block is rendered as a `<aside class="notes">` element.

### reveal-scientific (reveal.js)

A realistic 14-slide computational fluid dynamics conference talk.
Demonstrates: full metadata, multi-chapter structure, heavy LaTeX (PDEs,
algorithms), Python and Fortran code listings, `$table` convergence and
scaling tables, `$box` theorem blocks, `$columns` side-by-side layouts,
and speaker notes on every slide.

```bash
matisse build \
  -i examples/reveal-scientific/talk.md \
  -o examples/reveal-scientific/out/ \
  --backend reveal
```

Open `examples/reveal-scientific/out/index.html` in a browser.

### Build all examples at once

```bash
# impress.js — getting-started
matisse build \
  -i examples/getting-started/getting_started.md \
  -o examples/getting-started/out/ \
  --toc-at-subsec-beginning 2

# reveal.js — quickstart
matisse build \
  -i examples/reveal-quickstart/quickstart.md \
  -o examples/reveal-quickstart/out/ \
  --backend reveal

# reveal.js — scientific talk
matisse build \
  -i examples/reveal-scientific/talk.md \
  -o examples/reveal-scientific/out/ \
  --backend reveal
```

---

## Inline snippets

Quick copy-paste examples to get started with MaTiSSe.

Build any snippet by saving it to a `.md` file and running:

```bash
matisse build -i source.md -o output/
```

Then open `output/index.html` in a browser.

## Minimal presentation

```markdown
---
title: Hello World
author: Your Name
---
---
theme_slide_global:
  width:  900px
  height: 600px
---

$titlepage

# Introduction

## Overview

#### First Slide

This is a simple presentation using matisse.

Inline math: $E = mc^2$

Display math:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
```

Output preview:

![Screenshot of a minimal MaTiSSe presentation](/images/first_talk.png)

## Scientific talk

```markdown
---
title:       Scientific Presentation
subtitle:    Example of LaTeX Support
authors:     Your Name
affiliation: Department of Physics, University of Example
date:        Today
---

# Scientific Computing with Python

## Motivation

Why use scientific computing?

$$
E = mc^2
$$

## Method

1. Load data
2. Process
3. Analyse
4. Visualise

#### Results

![Results plot](results.png)

#### Conclusion

Summary of findings.
```

Output preview:

![Screenshot of a structured MaTiSSe presentation with sections](/images/second_talk.png)

## Two-column layout

```markdown
#### Comparison

$box
style: width:48%;float:left;
## Approach A
- Fast convergence
- Low memory
$endbox

$box
style: width:48%;float:right;
## Approach B
- Higher accuracy
- More complex
$endbox
```

## Mathematical physics

```markdown
---
title: Quantum Mechanics
---

# Wave Functions

## Schrödinger Equation

$$i\hbar \frac{\partial}{\partial t}\Psi = \hat{H}\Psi$$

## Harmonic Oscillator

Energy eigenvalues:

$$E_n = \hbar\omega\left(n + \frac{1}{2}\right)$$

#### Wavefunctions

$$\psi_n(x) = \left(\frac{m\omega}{\pi\hbar}\right)^{1/4}
              \frac{1}{\sqrt{2^n n!}} H_n(\xi)\, e^{-\xi^2/2}$$

where $\xi = \sqrt{\dfrac{m\omega}{\hbar}}\,x$.
```

## Code documentation talk

```markdown
---
title: Code Documentation Example
---

# Function Reference

#### hello_world()

```python
def hello_world(name: str) -> None:
    """Print a greeting."""
    print(f"Hello, {name}!")
```

Usage:

```python
hello_world("World")   # Hello, World!
```
```

## Conference talk with acknowledgements

```markdown
---
title:       Machine Learning with Physics
subtitle:    A Tutorial
authors:     Your Name
affiliation: Department of Theoretical Physics
date:        Today
---

$titlepage

# Motivation

#### Why ML?

Deep learning has transformed scientific computing.

## Methods

#### Neural Networks

$$\mathcal{L} = -\sum_i \log(\sigma(z_i))$$

#### Optimisation

Gradient descent:

$$\theta_{t+1} = \theta_t - \alpha \nabla \mathcal{L}$$

## Results

![Results](results.png)

## Conclusion

Summary.
```

## Common pitfalls

| Pitfall | Fix |
|---|---|
| Using `#`, `##`, `###` for content | Use `####` through `######` for slide content headings |
| Forgetting `####` slide titles | Every `####` starts a new slide |
| Display math not rendering | Use `$$...$$`, not single `$...$` |
| Images missing after build | Use paths relative to the source `.md` file |
| Slow MathJax loading | Use `--offline` to bundle MathJax locally |
