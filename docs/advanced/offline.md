# Offline Mode

By default MaTiSSe generates presentations that load their JavaScript and CSS from CDN:

| Asset | CDN source |
|---|---|
| impress.js 2 | jsDelivr |
| MathJax 3 | cdn.jsdelivr.net |

This keeps the output directory small and always uses the pinned versions.

> **Syntax highlighting is always local.**  MaTiSSe uses Pygments to highlight code blocks
> at build time and writes a `css/pygments.css` file into the output directory.  No CDN
> call is ever needed for highlighting — it works the same in online and offline mode.

## Enabling offline mode

Pass `--offline` to copy impress.js and MathJax bundles into the output directory:

```bash
matisse -i talk.md -o talk/ --offline
```

The output `js/` subdirectory will contain local copies of impress.js and MathJax. The
generated `index.html` references these local paths instead of CDN URLs.

## When to use offline mode

- Presenting in a venue with no internet access
- Archiving a self-contained presentation
- Distributing a talk as a zip file

## Output size

Bundling impress.js and MathJax adds roughly 10–15 MB to the output directory (dominated
by MathJax). For CDN mode the `js/` directory contains only `countdown.js` (a small
presentation timer utility) and `css/` contains the theme and Pygments stylesheets.
