# Figures

The `$figure...$endfigure` environment is a specialised box for captioned images.

## Syntax

```markdown
$figure
$style[style_options]
$content[content_options]{path/to/image.png}
$caption[caption_options]{caption text}
$endfigure
```

| Tag | Required | Description |
|---|---|---|
| `$style[...]` | No | CSS applied to the figure container |
| `$content[opts]{path}` | **Yes** | Path to the image file (relative to the source `.md` file). `[opts]` is CSS for the image element. |
| `$caption[opts]{text}` | No | Caption text. `[opts]` is CSS for the caption. Caption text supports Markdown formatting. |

**Key behaviours:**

- `content_type` is automatically set to `figure`; `caption_type` is automatically set to `Figure`
- **The caption is always placed below the image**, regardless of the order `$caption` and `$content` appear in the source
- Suppress the `Figure` prefix with `$caption(none){...}`

## Example

```markdown
$figure
$style[width:60%;margin:auto;text-align:center;]
$content[box-shadow:7px 7px 5px rgba(200,200,200,0.3);border-radius:25px;]{images/results.png}
$caption(none){Pressure field at $t = 1.0$ s — **CFD simulation**}
$endfigure
```

The caption text supports both inline math (`$...$`) and standard Markdown formatting (bold, italic, etc.).

## Reusing figure styles

Define a default figure style in the theme preamble to avoid repeating `$style[...]` on every figure:

```yaml
---
theme_figure:
  width: 60%
  margin: auto
  text-align: center
---
```

Then individual `$figure` environments can omit `$style` and inherit the preamble style automatically.
