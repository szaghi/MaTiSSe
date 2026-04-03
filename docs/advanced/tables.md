# Tables

The `$table...$endtable` environment wraps a Markdown table with a caption and styling.

## Syntax

```markdown
$table
$style[width:80%;margin:auto]
$caption[Table 1: Solver comparison.]
$content
| Solver  | Order | CFL   | Wall time (s) |
|---------|-------|-------|---------------|
| Euler   | 1     | 0.5   | 12.4          |
| RK4     | 4     | 0.8   | 48.1          |
| Adams   | 3     | 0.6   | 31.7          |
$endtable
```

## Options

| Tag | Description |
|---|---|
| `$style[...]` | CSS style for the table container |
| `$caption[...]` | Caption rendered above or below the table |
| `$content` | Marks the start of the Markdown table |

The table body is standard GitHub-Flavored Markdown table syntax.
