# Examples

Quick copy-paste examples to get started with MaTiSSe.py.

Build any example with:

```bash
MaTiSSe.py -i source.md -o output/
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

This is a simple presentation using MaTiSSe.py.

Inline math: $E = mc^2$

Display math:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$
```

Output preview:

![Screenshot of a minimal MaTiSSe.py presentation](/images/first_talk.png)

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

![Screenshot of a structured MaTiSSe.py presentation with sections](/images/second_talk.png)

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
