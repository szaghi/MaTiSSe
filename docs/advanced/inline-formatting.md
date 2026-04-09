# Inline Formatting

MaTiSSe extends standard Markdown with several inline text-formatting features
commonly needed in scientific writing: strikethrough, superscript, subscript,
footnotes, definition lists, sized images, and Quarto-compatible span classes.

## Strikethrough

Wrap text with double tildes to produce `<del>` (rendered with a strikethrough line):

```markdown
The ~~old result~~ corrected value is 42.
```

Renders as: The ~~old result~~ corrected value is 42.

Useful for showing edits, deprecated items, or crossed-out hypotheses.

## Superscript

Wrap text with carets (`^`) to produce `<sup>`:

```markdown
E = mc^2^

x^n^ + y^n^ = z^n^

The speed of light is 2.998 × 10^8^ m s^-1^.
```

::: tip Math vs. superscript
`^` inside a `$...$` or `$$...$$` block is consumed by MathJax and **never** touched
by the superscript processor.  Use `^text^` for non-math contexts (units, ordinals,
footnote-style markers) and `$x^{n}$` for equations.
:::

## Subscript

Wrap text with single tildes (`~`) to produce `<sub>`:

```markdown
Water is H~2~O.

Carbon dioxide CO~2~ is a greenhouse gas.

Sulfuric acid H~2~SO~4~.
```

Renders as: Water is H~2~O.

The single-tilde subscript is processed **after** the double-tilde strikethrough,
so `~~del~~` is never mis-parsed as nested subscripts.

## Footnotes

Use the standard Markdown footnote syntax:

```markdown
The result was significant.[^1]

A second claim needs a source.[^source]

[^1]: p < 0.05, two-tailed t-test, n = 120.
[^source]: Smith et al. (2023), *Journal of Something*, 42(3), 1–12.
```

Footnote definitions can appear anywhere in the slide source; they are collected and
rendered as a small block at the bottom of the slide content area.

::: tip Inline footnotes
The inline form `^[text]` is a Pandoc/Quarto extension not supported by Python-Markdown.
Use the reference form `[^label]` / `[^label]: text` instead.
:::

## Definition Lists

Use `term\n: definition` to produce `<dl>/<dt>/<dd>` blocks:

```markdown
Accuracy
:   The closeness of a measured value to the true value.

Precision
:   The repeatability of a measurement under identical conditions.

Resolution
:   The smallest detectable change in a quantity.
```

Multiple definitions for a single term are supported:

```markdown
Entropy
:   A measure of disorder in a thermodynamic system.
:   A measure of information content in a message (Shannon entropy).
```

Definition lists are well-suited for glossary slides, notation slides, and
terminology overviews.

## Image Attributes

Add `{...}` directly after a Markdown image to set HTML attributes:

```markdown
![Circuit diagram](images/circuit.png){width="70%"}

![Result plot](images/results.png){width="400px" .figure}

![Logo](images/logo.png){#logo-img width="80px"}
```

Supported attribute forms:

| Syntax | Effect |
|---|---|
| `{width="60%"}` | Sets `width` attribute on `<img>` |
| `{height="200px"}` | Sets `height` attribute on `<img>` |
| `{.classname}` | Adds a CSS class to `<img>` |
| `{#my-id}` | Sets the `id` attribute on `<img>` |
| `{style="border:1px solid red"}` | Inline CSS on `<img>` |

::: tip Full-featured figures
For captions, complex layouts, and styling of the container, use the
[`$figure` environment](/advanced/figures) instead.  Image attributes are ideal
for quick inline sizing without a caption.
:::

## Quarto-style Span Classes

Apply a CSS class (or arbitrary HTML attributes) to any inline run of text:

```markdown
[Underlined text]{.underline}

[Highlighted passage]{.mark}

[CHAPTER TITLE]{.smallcaps}

[Custom styled word]{.my-class}
```

### Built-in span classes

Three classes ship with the default stylesheet:

| Class | Effect |
|---|---|
| `.underline` | `text-decoration: underline` |
| `.mark` | Yellow background highlight (`background-color: #ff0`) |
| `.smallcaps` | `font-variant: small-caps` |

### Custom classes

Any class name works — add the corresponding CSS rule to your theme or a custom
stylesheet:

```markdown
[emphasis]{.alert}
```

```yaml
---
theme:
  layout:
    content:
      # no built-in hook; inject raw CSS via an overtheme or custom CSS file
---
```

### Other attributes

Beyond class names, arbitrary HTML attributes are supported:

```markdown
[anchor text]{#section-ref}

[tooltip text]{title="This is a tooltip"}

[styled inline]{style="color:crimson;font-weight:bold"}
```

### Alternative legacy syntax

MaTiSSe's original custom-span syntax still works and is equivalent:

```markdown
!!classname|text!!
```

The Quarto `[text]{.class}` form is preferred for compatibility with Quarto and
Pandoc workflows.

## Combining features

All inline features compose freely:

```markdown
~~Old H~2~O formula~~ Revised: H~2~^18^O[^1] with [corrected]{.mark} yield.

[^1]: Isotopically labelled water; purity > 99.9 %.
```

Within `$box`, `$note`, `$figure` captions, and column content, all inline
formatting is processed identically to slide body text.
