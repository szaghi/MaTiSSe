# Offline Mode

By default MaTiSSe.py generates presentations that load their JavaScript and CSS from CDN:

| Asset | CDN source |
|---|---|
| impress.js 2 | jsDelivr |
| MathJax 3 | cdn.jsdelivr.net |
| highlight.js 11 | cdnjs.cloudflare.com |

This keeps the output directory small and always uses the pinned versions.

## Enabling offline mode

Pass `--offline` to copy all three bundles into the output directory:

```bash
MaTiSSe.py -i talk.md -o talk/ --offline
```

The output `js/` subdirectory will contain local copies of impress.js, MathJax, and highlight.js. The generated `index.html` references these local paths instead of CDN URLs.

## When to use offline mode

- Presenting in a venue with no internet access
- Archiving a self-contained presentation
- Distributing a talk as a zip file

## Output size

Bundling all three libraries adds roughly 10–15 MB to the output directory (dominated by MathJax). For CDN mode the `js/` directory contains only `countdown.js` (a small presentation timer utility).
