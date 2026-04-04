# Markdown Syntax

MaTiSSe processes standard Markdown with several extensions for presentation structure and scientific content.

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

### Ordering rule

If the source defines at least one section (`#`), any subsections or slides that appear *before* the first section are silently omitted. The same applies to subsections relative to slides. Use `--verbose` to surface these warnings during the build.

### Unstructured presentations

Sections and subsections are optional. A flat sequence of slide headings is valid:

```markdown
#### First slide

Content here.

#### Second slide

More content.
```

## Special slides

### Title page

```markdown
$titlepage
```

Inserts a title page slide whose content is rendered from the presentation metadata (title, authors, affiliations, date). The optional `[plain]` modifier starts the title page from a bare theme instead of inheriting the global slide theme:

```markdown
$titlepage[plain]
```

The title page slide title is automatically set to an empty string; all other metadata keys are available and can be used inside `$box` environments placed after `$titlepage`. See [Metadata](/reference/metadata) for a full composition example.

## File inclusion

```markdown
$include(path/to/file.md)
```

Includes another Markdown file at parse time. Useful for splitting a large talk into per-section files or keeping metadata/theme definitions in separate files:

```markdown
$include(metadata.dat)
$include(theme.dat)

# First section

## Overview

#### Introduction
```

::: warning No recursive inclusion
`$include` statements are resolved once at the beginning of the build. Including a file that itself contains `$include` statements will not work.
:::

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
| `$columns...$endcolumns` | Multi-column layout |

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

They can also appear directly in slide content with optional CSS styling:

```markdown
$authors[font-size:150%;color:#003366]
```

See [Metadata](/reference/metadata) for the full list of keys including auto-generated ones (`toc`, `slidenumber`, `sectiontitle`, etc.).
