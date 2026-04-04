# Advanced Topics

This section covers MaTiSSe.py's rich content environments and scientific authoring features.

## Environments

- [Figures](/advanced/figures) — captioned images with positioning
- [Boxes & Notes](/advanced/boxes) — highlighted boxes, callouts, notes
- [Tables](/advanced/tables) — captioned tables
- [Columns](/advanced/columns) — multi-column layouts
- [Video](/advanced/video) — embedded video
- [Checklists](/advanced/checklists) — interactive checklist lists

## Scientific content

- [Math & LaTeX](/advanced/math) — equation authoring with MathJax 3
- [Code Highlighting](/advanced/code) — syntax highlighting with highlight.js 11

## Deployment

- [Offline Mode](/advanced/offline) — self-contained output with bundled assets

## Environment composition rules

`$columns` can contain any other environment — figures, boxes, notes, tables, and math all work inside a column.

Box-like environments (`$box`, `$note`, `$figure`, `$table`) **cannot** contain a `$columns` environment. Nest only one level deep.
