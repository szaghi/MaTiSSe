# Columns

MaTiSSe.py supports multi-column layouts within a slide using the columns environment.

## Syntax

```markdown
$columns

$column[column_options]
column 1 content

$column[column_options]
column 2 content

...

$endcolumns
```

| Tag | Description |
|---|---|
| `$columns` / `$endcolumns` | Open and close the columns environment |
| `$column[opts]` | Start a new column. `[opts]` is CSS for that column. |

The number of columns is counted automatically — you do not declare it explicitly.

::: warning Always specify `width`
Without an explicit `width` on each `$column`, the browser may produce unpredictable layouts. Make sure the widths sum to 100% (or slightly less to leave a gutter).
:::

## Example — two columns with a vertical separator

```markdown
$columns

$column[width:60%;padding-right:1%;border-right:1px solid #4788B3;]

This is the left column — 60% wide, separated by a vertical line.

$$
\nabla^2 \phi = 0
$$

$column[width:38%;padding-left:1%;]

This is the right column — 38% wide, with a small gutter.

$figure
$content[width:90%;]{images/solution.png}
$caption{Computed solution}
$endfigure

$endcolumns
```

## Example — code beside figure

```markdown
#### Implementation

$columns

$column[width:55%;]

```python
def solve(A, b):
    return np.linalg.solve(A, b)
```

$column[width:45%;]

$figure
$style[width:90%;]
$content[width:100%;]{convergence.png}
$caption{Convergence history}
$endfigure

$endcolumns
```

## Nesting

Columns can contain any MaTiSSe environment — math, figures, boxes, notes, tables, and video. Box-like environments (`$box`, `$note`, `$figure`, `$table`) **cannot** themselves contain a `$columns` environment.
