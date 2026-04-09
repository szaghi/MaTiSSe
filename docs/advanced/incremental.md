# Incremental Reveals

Incremental reveals let you unveil slide content step by step as you advance
through the presentation, keeping the audience focused on one point at a time.

MaTiSSe provides three mechanisms:

| Mechanism | Syntax | Backend support |
|---|---|---|
| Incremental list | `::: {.incremental}` | impress.js + reveal.js |
| Pause token | `. . .` | impress.js + reveal.js |
| Substep block | `$substep … $endsubstep` | impress.js only |

---

## Incremental lists

Wrap a bullet list in a `{.incremental}` fenced div to reveal each item
individually:

```markdown
::: {.incremental}
- First claim — shown alone
- Second claim — appears next
- Third claim — appears last
:::
```

Each `<li>` receives `class="substep"` (impress.js) or `class="fragment"`
(reveal.js) so the respective framework hides and reveals them on forward
navigation.

### Mixing with regular lists

Only the items inside the `{.incremental}` block are revealed incrementally.
Regular lists elsewhere on the same slide appear all at once:

```markdown
These points appear immediately:

- Background assumption 1
- Background assumption 2

These are revealed one by one:

::: {.incremental}
- Novel contribution A
- Novel contribution B
- Novel contribution C
:::
```

---

## Pause token

Insert `. . .` (three dots separated by spaces) on its own line to split slide
content at that point.  Everything **before** the pause is shown first;
subsequent content is revealed on the next forward press.

```markdown
#### Algorithmic idea

We start from a feasible point $x_0$.

. . .

At each step we compute the gradient $\nabla f(x_k)$.

. . .

We then set $x_{k+1} = x_k - \alpha \nabla f(x_k)$ and repeat.
```

The pause token works anywhere inside slide content — between paragraphs,
after a list, before a figure, etc.

---

## Substep blocks (impress.js)

For finer control over what is hidden and when, use explicit `$substep` /
`$endsubstep` blocks.  Each block wraps arbitrary content in a `<div
class="substep">` element, which the impress.js Substep plugin hides initially
and reveals on forward navigation.

```markdown
$substep
This paragraph is revealed at step 1.
$endsubstep

$substep
This equation is revealed at step 2.

$$E = mc^2$$
$endsubstep
```

### Grouped substeps

Use the `order:N` option to reveal multiple blocks simultaneously:

```markdown
$substep[order:1]
Left column content — appears together with the right column.
$endsubstep

$substep[order:1]
Right column content — same reveal step as left column.
$endsubstep

$substep[order:2]
This appears next, after both columns are visible.
$endsubstep
```

> **Substeps are impress.js only.**  The reveal.js backend does not support
> `$substep` / `$endsubstep`.  Use `::: {.incremental}` or `. . .` for
> cross-backend compatible reveals.

---

## Backend differences

| Feature | impress.js | reveal.js |
|---|---|---|
| `{.incremental}` class | `substep` | `fragment` |
| `. . .` pause | Substep split | Fragment split |
| `$substep` blocks | ✓ supported | ✗ not supported |
| Reveal order | Sequential | Sequential |

---

## See also

- [reveal.js backend](/advanced/reveal) — overview mode, speaker notes, fragments
- [Columns](/advanced/columns) — multi-column layouts (combine with incremental)
- [Callout Blocks](/advanced/callouts) — emphasis boxes (can appear as substeps)
