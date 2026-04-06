---
metadata:
  - title:    "Reveal.js Integration Test"
  - subtitle: "Testing all RevealTheme options"
  - authors:
    - Test Author
  - date: "2026"
  - max_time: 10
---

---
reveal:
  theme: moon
  transition: fade
  transition_speed: fast
  controls: true
  controls_layout: bottom-right
  progress: true
  slide_number: "c/t"
  loop: false
  center: true
  auto_slide: 0
  width: 1280
  height: 720
  margin: 0.05
  min_scale: 0.2
  max_scale: 2.0
  background_transition: fade
  keyboard: true
  touch: true
  layout: linear
  plugins:
    - notes
    - zoom
  code_style: monokai
  custom_css: ".reveal { font-family: sans-serif; }"
---

# Chapter One

## Section One

### Subsection One

#### $titlepage

$box
$style[width:100%;background:#1a1a2e;border-radius:8px;padding:3%]
$content[color:white;text-align:center;]{
$title[display:block;font-size:200%;font-weight:bold]
$subtitle[display:block;font-size:120%;opacity:0.8;padding-top:2%]
$authors[display:block;font-size:100%;padding-top:3%]
$date[display:block;font-size:80%;opacity:0.6;padding-top:2%]
}
$endbox

$note
$content{Speaker note on the title slide.}
$endnote

#### Slide with Per-Slide Background
---
overtheme:
  reveal:
    background_color: "#2c3e50"
    transition: zoom
---

Content on a slide with a custom background colour and per-slide transition.

$note
$content{This slide uses a dark blue background via data-background-color.}
$endnote

#### Math Equations

Inline math: $E = mc^2$.

Display math:

$$
\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}
$$

$note
$content{MathJax renders LaTeX; the notes plugin exposes these in the presenter view.}
$endnote

#### Code Block

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("world"))
```

#### Columns and Box

$columns
$column[width:48%]
**Left column**

- Point A
- Point B
- Point C with $\alpha + \beta = \gamma$
$column[width:48%]
$box
$caption[color:#e74c3c]{Key Result}
$content[padding:0.8em]{
The answer is always **42**.
}
$endbox
$endcolumns

# Chapter Two

## Section Two

### Subsection Two

#### Auto-Animate Slide (before)
---
overtheme:
  reveal:
    auto_animate: true
---

- Item one

#### Auto-Animate Slide (after)
---
overtheme:
  reveal:
    auto_animate: true
---

- Item one
- Item two (animated in)

#### Final Slide

Summary slide with no special overrides.

$note
$content{End of the test presentation. All environments rendered successfully.}
$endnote
