# Math & LaTeX

MaTiSSe.py renders equations with [MathJax 3](https://www.mathjax.org/), loaded from CDN by default.

## Inline math

Wrap an expression in single dollar signs:

```markdown
The energy-mass relation $E = mc^2$ is fundamental.
```

Renders as: The energy-mass relation $E = mc^2$ is fundamental.

## Display math

Wrap a block in double dollar signs:

```markdown
$$
\int_0^\infty e^{-x^2}\, dx = \frac{\sqrt{\pi}}{2}
$$
```

The equation is rendered directly in the slide by MathJax:

![LaTeX equation rendered in a MaTiSSe.py slide](/images/latexeq.png)

## Escaping dollar signs

To include a literal `$` that should not trigger math, escape it:

```markdown
The price is \$42.
```

## MathJax configuration

MaTiSSe configures MathJax with:

- Inline delimiters: `$...$` and `\\(...\\)`
- Display delimiters: `$$...$$` and `\\[...\\]`
- `processEscapes: true` (so `\$` is treated as a literal dollar sign)

No user configuration is needed.

## Offline use

When `--offline` is passed, the MathJax bundle is copied into the output directory and loaded from there. The equation rendering is identical.
