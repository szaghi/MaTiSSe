---
metadata:
  - title:    "Hello, reveal.js!"
  - subtitle: "A minimal MaTiSSe reveal.js presentation"
  - authors:
    - Jane Smith
  - authors_short:
    - J. Smith
  - affiliations:
    - Example University
  - date: "2026"
  - max_time: 20
  - toc_depth: 1
---

# Introduction

## What is this?

### Overview

#### $titlepage

$box
$style[width:100%;background:#1a1a2e;border-radius:12px;padding:4%]
$content[color:white;text-align:center;]{
$title[display:block;font-size:220%;font-weight:bold;padding-bottom:2%]
$subtitle[display:block;font-size:130%;opacity:0.8;padding-bottom:4%]
$authors[display:block;font-size:110%]
$affiliations[display:block;font-size:90%;opacity:0.7;padding-top:1%]
$date[display:block;font-size:85%;opacity:0.6;padding-top:3%]
}
$endbox

$note
$content{
Welcome everyone! Today I'll walk you through the basics of building
reveal.js presentations with MaTiSSe.

This is a speaker note — only visible in the presenter view (press S).
}
$endnote

#### What is MaTiSSe?

**MaTiSSe** (_Markdown To Impressive Scientific Slides_) compiles plain
Markdown into self-contained HTML presentations.

- Write in **Markdown** — no HTML boilerplate
- Full **LaTeX equations** via MathJax
- **Syntax-highlighted** code via highlight.js
- Rich **scientific environments**: figures, boxes, tables, columns
- Two rendering backends: **impress.js** (3D canvas) and **reveal.js**

```bash
# Build this presentation
matisse build -i quickstart.md -o out/ --backend reveal
```

$note
$content{
Emphasise the "same source file, one flag" pitch:
the identical .md file compiles to either backend.
}
$endnote

# Core Features

## LaTeX Math

### Equations

#### Inline and Display Math

MaTiSSe renders LaTeX via **MathJax 3**.

Inline math: the quadratic formula is $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$.

Display math renders on its own line:

$$
\int_{-\infty}^{\infty} e^{-x^2} \, dx = \sqrt{\pi}
$$

$$
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}, \qquad
\nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0\varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}
$$

$note
$content{
The Gaussian integral and Maxwell's equations make for a nice demo.
MathJax is loaded from CDN — no local setup needed.
}
$endnote

## Code

### Syntax Highlighting

#### Python Example

highlight.js 11 colours code blocks automatically.

```python
import math

def is_prime(n: int) -> bool:
    """Return True if n is prime."""
    if n < 2:
        return False
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True

primes = [x for x in range(2, 50) if is_prime(x)]
print(primes)
```

$note
$content{
Ask the audience: can anyone spot the algorithmic complexity?
It is O(sqrt(n)) thanks to math.isqrt — much better than checking all n.
}
$endnote

#### Fortran Example

```fortran
program hello
  implicit none
  integer :: i
  do i = 1, 10
    if (mod(i, 2) == 0) print *, i, 'is even'
  end do
end program hello
```

# Environments

## Boxes and Notes

### Built-in Environments

#### Box Environment

$box
$caption[color:#2c3e50;border-bottom:2px solid #2c3e50]{Key Theorem}
$content[padding:1em]{
Let $f : \mathbb{R} \to \mathbb{R}$ be a continuous function on $[a, b]$
and differentiable on $(a, b)$. Then there exists $c \in (a, b)$ such that

$$f'(c) = \frac{f(b) - f(a)}{b - a}$$
}
$endbox

This is the **Mean Value Theorem** — rendered via the `$box` environment.

$note
$content{
The box environment supports custom CSS for the caption and content areas.
Great for theorems, definitions, remarks, and warnings.
}
$endnote

#### Columns Layout

$columns
$column[width:48%]
**Left column**

+ Point A: the `$columns` environment splits the slide horizontally.
+ Point B: each column is independently styled.
+ Point C: works with any inline Markdown.
$column[width:48%]
**Right column**

1. Numbered lists work too.
2. Mix math: $e^{i\pi} + 1 = 0$
3. And **bold** or _italic_ text.
$endcolumns

$note
$content{
Columns are great for side-by-side comparisons — e.g., pseudocode on the
left and timing results on the right.
}
$endnote

# Wrapping Up

## Summary

### Conclusion

#### Key Takeaways

$box
$caption[color:#27ae60]{What we covered}
$content[padding:1em]{
1. **Slide structure** — chapters, sections, subsections, slides via `#` headings
2. **LaTeX math** — inline `$…$` and display `$$…$$`
3. **Syntax highlighting** — fenced code blocks with language tags
4. **Environments** — `$box`, `$columns`, `$note`
5. **Speaker notes** — `$note` maps to `<aside class="notes">` in reveal.js
}
$endbox

#### Build command recap

```bash
matisse build -i quickstart.md -o out/ --backend reveal
```

Press **O** for the overview, **S** for the presenter view, **F** for full screen.

$note
$content{
Thank the audience. Remind them the full documentation is at
https://szaghi.github.io/MaTiSSe/

Questions?
}
$endnote
