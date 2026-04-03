# Command-Line Options

```
MaTiSSe.py [options]
```

## Core options

| Option | Default | Description |
|---|---|---|
| `-i FILE`, `--input FILE` | — | Input Markdown source file *(required)* |
| `-o DIR`, `--output DIR` | — | Output directory *(required)* |
| `--offline` | off | Copy JS/CSS bundles into the output directory instead of loading from CDN |
| `--pdf` | off | Generate PDF-friendly output (no impress.js, plain scrollable HTML) |

## Informational options

| Option | Description |
|---|---|
| `--sample FILE` | Write a fully annotated sample presentation to FILE and exit |
| `--print-themes` | Print all available built-in theme names and exit |
| `--print-highlight-styles` | Print all available highlight.js style names and exit |
| `-v`, `--version` | Print version and exit |
| `-h`, `--help` | Print help and exit |

## Examples

```bash
# Minimal build
MaTiSSe.py -i talk.md -o talk/

# Bundle all assets locally (for offline use or air-gapped deployment)
MaTiSSe.py -i talk.md -o talk/ --offline

# PDF-friendly output (no slide animations)
MaTiSSe.py -i talk.md -o talk/ --pdf

# Start from a sample
MaTiSSe.py --sample mytalk.md
MaTiSSe.py -i mytalk.md -o mytalk/
```
