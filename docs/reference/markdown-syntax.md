# Markdown Syntax

MaTiSSe.py processes standard Markdown with several extensions for presentation structure and scientific content.

## Document structure

Headings map to the presentation hierarchy:

```markdown
# Chapter title
## Section title
### Subsection title
#### Slide title
```

Each `####` heading starts a new slide. Chapters, sections, and subsections are structural — they appear in the automatically generated table of contents.

::: warning Heading levels and content
`#`, `##`, and `###` are **structural** — they define chapters, sections, and subsections, not slide content. Use `####` through `######` for in-slide headings. If you need an `<h1>`–`<h3>` inside slide content, write it as raw HTML:

```html
<h2>This is a content heading, not a section</h2>
```
:::

## Special slides

```markdown
$titlepage
```

Inserts a title page slide whose content is rendered from the presentation metadata (title, authors, affiliations, date).

## File inclusion

```markdown
$include(path/to/file.md)
```

Recursively includes another Markdown file. Useful for splitting a large talk into per-section files.

## YAML blocks

Two kinds of YAML blocks are recognised at the document level:

```markdown
---
title:   My Talk
authors: Stefano Zaghi
---
```

A metadata block (first `---` block) defines presentation-level variables.

```markdown
---
theme_slide_global:
  width:  900px
  height: 600px
---
```

A theme block defines or overrides visual properties. Multiple theme blocks may appear throughout the document.

## Math

Inline math uses single dollar signs:

```markdown
The energy is $E = mc^2$.
```

Display math uses double dollar signs:

```markdown
$$
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}
$$
```

## Environments

All environments follow the same pattern:

```markdown
$environment
...content...
$endenvironment
```

Available environments:

| Environment | Description |
|---|---|
| `$figure...$endfigure` | Captioned figure |
| `$box...$endbox` | Highlighted box |
| `$note...$endnote` | Note/callout |
| `$table...$endtable` | Table with caption |
| `$video...$endvideo` | Embedded video |

See the [Advanced](/advanced/) section for full details on each environment.

## Metadata interpolation

Metadata values can be interpolated into theme text fields using `$key` placeholders:

```yaml
---
theme_slide_header_1:
  active: True
  height: 10%
  content: "$title — $authors"
---
```
