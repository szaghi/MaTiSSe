# Theorems, Lemmas, and Proofs

MaTiSSe provides numbered theorem-like environments for scientific presentations —
theorems, lemmas, corollaries, definitions, examples, exercises, remarks, and
propositions — together with an unnumbered proof environment.

All environments use the same fenced-div syntax and integrate with the
[cross-reference system](#cross-references).

---

## Theorem-like environments

### Syntax

```markdown
::: {#PREFIX-id}
## Optional title
Body content (full Markdown, including math).
:::
```

`PREFIX` determines the environment type and its display label.  `id` is a unique
identifier used for cross-referencing (see [below](#cross-references)).

### Supported prefixes

| Prefix | Display label | Example heading |
|---|---|---|
| `thm` | Theorem | **Theorem 1** |
| `lem` | Lemma | **Lemma 1** |
| `cor` | Corollary | **Corollary 1** |
| `prp` | Proposition | **Proposition 1** |
| `def` | Definition | **Definition 1** |
| `exm` | Example | **Example 1** |
| `exr` | Exercise | **Exercise 1** |
| `rem` | Remark | **Remark 1** |

Counters are **per-prefix** and sequential within the presentation.

### Examples

**Theorem without a title:**

```markdown
::: {#thm-cauchy}
$$|\langle u, v\rangle|^2 \leq \|u\|^2 \|v\|^2$$
:::
```

Renders as: **Theorem 1** followed by the equation.

**Definition with a title:**

```markdown
::: {#def-lipschitz}
## Lipschitz continuity
A function $f : \mathbb{R}^n \to \mathbb{R}^m$ is $L$-Lipschitz if for all
$x, y$:
$$\|f(x) - f(y)\| \leq L\,\|x - y\|$$
:::
```

Renders as: **Definition 1 (Lipschitz continuity)**.

**Example with inline math:**

```markdown
::: {#exm-gradient-descent}
## Gradient descent step
Starting from $x_0$, iterate:
$$x_{k+1} = x_k - \alpha \nabla f(x_k)$$
with step size $\alpha > 0$.
:::
```

---

## Proof environment

Proofs use the `.proof` class instead of a `#PREFIX-id` identifier.  They are
**unnumbered** and always end with the QED symbol ∎.

```markdown
::: {.proof}
Let $\varepsilon > 0$.  By compactness of the unit sphere there exists a
finite $\varepsilon$-net …

The bound follows by taking the supremum over all unit vectors.
:::
```

If the body already contains `∎` or `\square`, the auto-appended symbol is
suppressed to avoid duplication.

A proof can follow immediately after a theorem block:

```markdown
::: {#thm-fundamental}
## Fundamental theorem of calculus
If $f$ is continuous on $[a,b]$ then
$$\int_a^b f(x)\,dx = F(b) - F(a)$$
where $F' = f$.
:::

::: {.proof}
Define $F(x) = \int_a^x f(t)\,dt$ and differentiate under the integral sign…
:::
```

---

## Cross-references

### Labelling

Every theorem-like block carries an implicit label derived from its `#PREFIX-id`.
The label is also registered in the global label registry for use as a
cross-reference target:

```markdown
::: {#thm-main-result}
## Main result
…
:::
```

HTML id: `thm-main-result`.

### Referencing

Use `@PREFIX-id` anywhere in slide content (including inside other environments)
to insert a hyperlinked cross-reference:

```markdown
As shown in @thm-main-result, the bound is tight.
```

Renders as a link: **Theorem 1** → `<a href="#thm-main-result">Theorem 1</a>`.

If the target label is not found a `??` warning link is emitted and a message is
printed at build time.

### All supported reference prefixes

| Prefix | Display label |
|---|---|
| `fig` | Figure |
| `tbl` | Table |
| `eq` | Equation |
| `sec` | Section |
| `dia` | Diagram |
| `thm` | Theorem |
| `lem` | Lemma |
| `cor` | Corollary |
| `prp` | Proposition |
| `def` | Definition |
| `exm` | Example |
| `exr` | Exercise |
| `rem` | Remark |

---

## Complete example

```markdown
#### Key mathematical results

::: {#def-convex}
## Convex function
$f$ is convex if for all $x, y$ and $\lambda \in [0,1]$:
$$f(\lambda x + (1-\lambda)y) \leq \lambda f(x) + (1-\lambda)f(y)$$
:::

::: {#thm-jensen}
## Jensen's inequality
For a convex function $f$ and random variable $X$:
$$f(\mathbb{E}[X]) \leq \mathbb{E}[f(X)]$$
:::

::: {.proof}
Apply @def-convex repeatedly to the finite expectation sum…
:::

By @thm-jensen the empirical risk is an upper bound on the expected risk.
```

---

## HTML output and CSS customisation

```html
<!-- theorem -->
<div class="theorem theorem-thm" id="thm-cauchy">
  <div class="theorem-header"><strong>Theorem 1 (Cauchy–Schwarz)</strong></div>
  <div class="theorem-body">…</div>
</div>

<!-- proof -->
<div class="theorem theorem-proof" id="proof-1">
  <div class="theorem-header"><em>Proof.</em></div>
  <div class="theorem-body">
    …
    <span class="qed">∎</span>
  </div>
</div>
```

Useful CSS selectors for custom styling:

```css
.theorem              { border-left: 3px solid #4a90d9; padding: 0.5em 1em; }
.theorem-thm          { background: rgba(74,144,217,0.05); }
.theorem-def          { border-left-color: #2e8b57; }
.theorem-proof        { border-left-color: #888; font-style: italic; }
.theorem-header       { font-size: 110%; margin-bottom: 0.3em; }
.qed                  { float: right; }
.cross-ref            { color: #4a90d9; text-decoration: none; }
```

Apply via `css_overtheme` in your metadata block.

---

## See also

- [Callout Blocks](/advanced/callouts) — warning/tip/note callouts
- [Diagrams](/advanced/diagrams) — Mermaid and Graphviz diagrams
- [Math & LaTeX](/advanced/math) — inline and display math with MathJax 3
- [Cross-reference prefixes](#all-supported-reference-prefixes) — full label table
