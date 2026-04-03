# Boxes & Notes

## Box environment

The `$box...$endbox` environment wraps content in a styled box — useful for definitions, theorems, or highlighted remarks.

```markdown
$box
$style[background:#e8f4fd;border-left:4px solid #2196F3;padding:12px]
$caption(Definition)[Convergence]
$content
A sequence $\{x_n\}$ **converges** to $L$ if for every $\varepsilon > 0$
there exists $N$ such that $|x_n - L| < \varepsilon$ for all $n > N$.
$endbox
```

### Box options

| Tag | Description |
|---|---|
| `$style[...]` | CSS style for the box container |
| `$caption(type)[title]` | Box header — `type` is the label (e.g. Definition, Theorem), `title` is the name |
| `$content` | Marks the start of the box body |

## Note environment

The `$note...$endnote` environment is a lighter callout, typically used for asides or warnings.

```markdown
$note
$style[background:#fff9c4;padding:10px]
$caption(Note)[Numerical stability]
$content
Use double precision (`float64`) to avoid catastrophic cancellation
when subtracting nearly equal values.
$endnote
```

Notes follow the same tag structure as boxes.
