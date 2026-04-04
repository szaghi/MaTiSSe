# Boxes & Notes

## Box environment

The `$box...$endbox` environment wraps any content in a styled div — useful for definitions, theorems, highlighted remarks, or any content that needs a distinct visual treatment.

### Full syntax

```markdown
$box
$style[style_options]
$caption(caption_type)[caption_options]{caption text}
$content(content_type)[content_options]{content}
$endbox
```

| Tag | Required | Description |
|---|---|---|
| `$style[...]` | No | CSS applied to the whole box container. `[]` must be present even if empty. |
| `$caption(type)[opts]{text}` | No | Box header. `(type)` is a label prefix (e.g. `Definition`, `Theorem`). Use `(none)` to suppress the prefix. `[opts]` is CSS for the caption only. `{text}` is the caption text. |
| `$content(type)[opts]{body}` | **Yes** | Box body. `(type)` classifies the content (`figure`, `table`, `note`, `box`). `[opts]` is CSS for the content only. `{body}` is the content — can span multiple lines. |

All parenthesised and bracketed modifiers are optional individually, so these are all valid:

```markdown
$caption{Just a caption, no type or style}
$caption[font-size:90%;]{Caption with style, no type}
$caption(Note)[font-weight:bold;]{Styled note caption}

$content{Plain content}
$content[padding:8px;]{Styled content}
```

### Example

```markdown
$box
$style[background:rgb(100,100,100);]
$caption(Definition)[font-size:90%;color:white;]{Convergence}
$content[font-size:120%;color:white;]{
A sequence $\{x_n\}$ **converges** to $L$ if for every $\varepsilon > 0$
there exists $N$ such that $|x_n - L| < \varepsilon$ for all $n > N$.
}
$endbox
```

### Caption positioning

By default the caption appears **below** the content. Use `position: TOP` inside the caption options to move it above:

```markdown
$box
$style[background:#e8f4fd;border-left:4px solid #2196F3;padding:12px;]
$caption(Theorem)[color:#003366;position: TOP;]{Pythagorean theorem}
$content{For a right triangle: $a^2 + b^2 = c^2$.}
$endbox
```

The `position` keyword is **case-sensitive** and must be `TOP` or `BOTTOM`. It is stripped from the CSS before output so it does not pollute the rendered HTML. An unrecognised value silently defaults to `BOTTOM`.

### Box contents

Box content fully supports Markdown:

- bullet lists and numbered lists
- bold, italic, and other inline formatting
- headings `####` through `######`
- LaTeX equations (inline `$...$` and display `$$...$$`)

---

## Note environment

The `$note...$endnote` environment is a specialised box for asides and warnings.

### Syntax

```markdown
$note
$style[style_options]
$caption[caption_options]{caption text}
$content[content_options]{content}
$endnote
```

Differences from `$box`:

- `content_type` is automatically `note`; `caption_type` is automatically `Note`
- **The caption is always placed above the content**, regardless of declaration order

### Example

```markdown
$note
$style[background:#fff9c4;padding:10px;border-left:3px solid #f9a825;]
$caption[font-weight:bold;]{Numerical stability}
$content{
Use double precision (`float64`) to avoid catastrophic cancellation
when subtracting nearly equal values.
}
$endnote
```

Note contents support the same Markdown and LaTeX features as box contents.

---

## Reusing styles via the theme preamble

Repeating `$style[...]` on every box is tedious. Define a default box, note, or figure style once in the theme preamble and omit the `$style` tag on individual environments — MaTiSSe will apply the preamble style automatically.
