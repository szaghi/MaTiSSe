# Columns

MaTiSSe.py supports multi-column layouts within a slide using the columns environment.

## Syntax

```markdown
$columns

$column[width:50%]
Left column content — text, math, code, figures.

$column[width:50%]
Right column content.

$endcolumns
```

Each `$column[...]` starts a new column. The width is specified as a CSS value.

## Example — side-by-side code and figure

```markdown
#### Implementation

$columns

$column[width:55%]

```python
def solve(A, b):
    return np.linalg.solve(A, b)
```

$column[width:45%]

$figure
$style[width:90%]
$content[convergence.png]
$caption[Convergence history]
$endfigure

$endcolumns
```

## Tips

- Column widths should sum to 100% (or less, leaving a gutter)
- Any MaTiSSe content — math, figures, boxes — works inside columns
- Columns are rendered as CSS flexbox containers
