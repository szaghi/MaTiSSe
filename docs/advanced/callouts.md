# Callout Blocks

Callout blocks draw the reader's attention to important information — warnings,
tips, notes, and similar asides. MaTiSSe renders them as styled containers with a
coloured left border and a type icon.

---

## Syntax

```markdown
::: {.callout-TYPE}
Body content (full Markdown supported).
:::
```

Replace `TYPE` with one of the five supported kinds:

| Type | Icon | Border colour | Default title |
|---|---|---|---|
| `note` | ℹ | Blue `#0070c0` | Note |
| `tip` | 💡 | Green `#2e8b57` | Tip |
| `warning` | ⚠ | Amber `#e69500` | Warning |
| `caution` | 🔴 | Red `#cc0000` | Caution |
| `important` | ❗ | Purple `#7b2d8b` | Important |

---

## Title options

### Default title

If you supply no title, the block uses the type name (capitalised):

```markdown
::: {.callout-tip}
Use `--offline` when you present without internet access.
:::
```

### Inline title attribute

Add `title="…"` inside the attribute string:

```markdown
::: {.callout-warning title="Data will be overwritten"}
Running with `--output` points to an existing directory.
All files inside it will be replaced.
:::
```

### Heading inside the block

A `## heading` as the first line of the block body is promoted to the title and
stripped from the body:

```markdown
::: {.callout-note}
## Reproducibility tip
Commit your `.md` source alongside the generated HTML so reviewers
can rebuild the presentation from source.
:::
```

Both `title="…"` and `## heading` can be used; the inline attribute takes
precedence if both are present.

---

## All five types

### Note

```markdown
::: {.callout-note}
## About MathJax
MathJax 3 is loaded from CDN by default. Pass `--offline` to bundle it
locally for air-gapped venues.
:::
```

### Tip

```markdown
::: {.callout-tip title="Workflow tip"}
Keep your theme in a separate `theme.yaml` and include it with
`$include(theme.yaml)` — this lets you reuse the same visual style
across multiple talks.
:::
```

### Warning

```markdown
::: {.callout-warning}
## Breaking change in v1.6
The theme YAML format changed completely.  If you are upgrading from
v1.5 read the [migration guide](/reference/themes#migration-guide-v15--v16).
:::
```

### Caution

```markdown
::: {.callout-caution title="Destructive operation"}
`dirs_to_copy` copies directories **into** the output directory.
Any existing files with the same name are silently overwritten.
:::
```

### Important

```markdown
::: {.callout-important}
The `$include` directive is resolved in a **single pass** before
parsing begins.  Circular includes are not detected and will loop
indefinitely.
:::
```

---

## Markdown inside callouts

The body of a callout is full Markdown — you can use lists, code blocks,
math, and inline formatting:

```markdown
::: {.callout-note title="Supported math syntax"}
Use `$...$` for inline math and `$$...$$` for display math:

$$E = mc^2$$

- Inline: $\alpha + \beta = \gamma$
- Display is centred automatically.
:::
```

---

## HTML output and CSS customisation

Each callout renders as:

```html
<div class="callout callout-note" id="callout-1"
     style="border-left: 4px solid #0070c0;">
  <div class="callout-title">
    <span class="callout-icon">ℹ</span> Note
  </div>
  <div class="callout-body">
    <!-- rendered Markdown -->
  </div>
</div>
```

To override the default appearance, add custom CSS via the `css_overtheme`
metadata key (applied globally) or a per-slide overtheme's CSS.  For example,
to add a light background tint for all notes:

```css
/* custom.css */
.callout-note  { background: rgba(0, 112, 192, 0.05); }
.callout-tip   { background: rgba(46, 139, 87,  0.05); }
```

```yaml
---
css_overtheme: ['custom.css']
---
```

---

## See also

- [Theorems & Proofs](/advanced/theorems) — numbered theorem-like environments
- [Boxes & Notes](/advanced/boxes) — simpler `$box`/`$note` environments
- [Inline Formatting](/advanced/inline-formatting) — superscript, subscript, spans
