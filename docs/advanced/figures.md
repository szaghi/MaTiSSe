# Figures

The `$figure...$endfigure` environment inserts a captioned image into a slide.

## Syntax

```markdown
$figure
$style[width:60%;margin:auto]
$content[figure.png]
$caption[Figure 1: A captioned image.]
$endfigure
```

## Options

| Tag | Description |
|---|---|
| `$style[...]` | CSS style applied to the figure container |
| `$content[...]` | Path to the image file (relative to the source file) |
| `$caption[...]` | Caption text (rendered below the image) |

## Example

```markdown
#### Results

$figure
$style[width:70%;margin:auto;text-align:center]
$content[results/pressure_field.png]
$caption[Figure 2: Pressure field at $t = 1.0$ s.]
$endfigure
```

Math can be used inside the caption via the usual `$...$` delimiters.
