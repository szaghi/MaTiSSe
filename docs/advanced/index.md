# Advanced Topics

This section covers MaTiSSe's rich content environments, scientific authoring
features, styling options, and rendering backends.

---

## Content environments

Classic `$environment … $endenvironment` blocks for structured slide content:

- [Figures](/advanced/figures) — captioned images with positioning
- [Boxes & Notes](/advanced/boxes) — highlighted boxes and aside callouts
- [Tables](/advanced/tables) — captioned tables with GFM syntax
- [Columns](/advanced/columns) — multi-column layouts
- [Video](/advanced/video) — embedded video files
- [Checklists](/advanced/checklists) — interactive checklist items

### Nesting rules

`$columns` can contain any other environment — figures, boxes, notes, tables,
and math all work inside a column.

Box-like environments (`$box`, `$note`, `$figure`, `$table`) **cannot** contain
a `$columns` environment. Nest only one level deep.

---

## Advanced syntax

New fenced-div environments for callouts, theorems, diagrams, and animated reveals:

- [Callout Blocks](/advanced/callouts) — warning, tip, note, caution, important
- [Theorems & Proofs](/advanced/theorems) — auto-numbered theorem-like environments and cross-references
- [Diagrams](/advanced/diagrams) — Mermaid and Graphviz/dot figures
- [Incremental Reveals](/advanced/incremental) — reveal content step by step (incremental lists, pause tokens, substep blocks)

---

## Text formatting

- [Inline Formatting](/advanced/inline-formatting) — strikethrough, superscript, subscript, footnotes, definition lists, image attributes, Quarto-style spans

---

## Scientific content

- [Math & LaTeX](/advanced/math) — equation authoring with MathJax 3
- [Code Highlighting](/advanced/code) — syntax highlighting with Pygments (50+ languages, 48 styles)

---

## Themes in depth

- [Themes In Depth](/advanced/themes) — comprehensive walkthrough and real-world recipes for every theme section

---

## Backends and deployment

- [reveal.js backend](/advanced/reveal) — speaker notes, overview mode, fragments, PDF export
- [Offline Mode](/advanced/offline) — self-contained output with bundled assets
