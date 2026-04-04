# Command-Line Options

```
matisse [OPTIONS] COMMAND [ARGS]...
matisse build [OPTIONS]
```

The single command is `build`. It is the default, so `matisse build [OPTIONS]`
and `matisse [OPTIONS]` behave identically at the shell.

## I/O options

| Option | Short | Description |
|---|---|---|
| `--input FILE` | `-i` | Input Markdown source file to parse *(required for a build)* |
| `--output DIR` | `-o` | Output directory. Defaults to the input filename without its extension. |

## Sample options

| Option | Short | Description |
|---|---|---|
| `--sample FILE` | `-s` | Write a fully annotated sample presentation to FILE and exit |
| `--theme NAME` | `-t` | Apply a built-in theme to the presentation (see `--print-themes`) |

## Rendering options

| Option | Short | Default | Description |
|---|---|---|---|
| `--backend NAME` | `-b` | `impress` | Rendering backend: `impress` (impress.js) or `reveal` (reveal.js) |
| `--offline` | — | off | Bundle impress.js, MathJax, and highlight.js locally instead of loading from CDN (impress backend only) |
| `--pdf` | — | off | Disable impress.js animations — suitable for PDF printing (impress backend only) |
| `--highlight-style STYLE` | `-hs` | `github.css` | highlight.js CSS style. Use `"disable"` to turn off syntax highlighting. |

## TOC options

| Option | Metavar | Description |
|---|---|---|
| `--toc-at-chap-beginning` | `DEPTH` | Insert a TOC slide at each chapter beginning. `DEPTH` controls how many levels to show. |
| `--toc-at-sec-beginning` | `DEPTH` | Insert a TOC slide at each section beginning. |
| `--toc-at-subsec-beginning` | `DEPTH` | Insert a TOC slide at each subsection beginning. |

## Info options

These options print information and exit immediately — no source file is required.

| Option | Description |
|---|---|
| `--print-themes` | List all available built-in themes |
| `--print-highlight-styles` | List all available highlight.js styles |
| `--version` / `-v` | Print version and exit |
| `--help` | Print help and exit |

## Debug options

| Option | Description |
|---|---|
| `--verbose` | Print verbose build messages |
| `--print-parsed-source` | Print the fully resolved source (after `$include` expansion) and continue |

## Shell completions

MaTiSSe includes shell tab-completion for `--theme` and `--highlight-style`.
Enable it once for your shell:

```bash
# bash
matisse --install-completion bash

# zsh
matisse --install-completion zsh

# fish
matisse --install-completion fish
```

After restarting your shell (or sourcing the completion script), pressing `Tab`
after `--theme` or `--highlight-style` will list matching names.

To inspect the generated completion script without installing it:

```bash
matisse --show-completion
```

## Examples

```bash
# Minimal build (impress.js — default)
matisse build -i talk.md -o talk/

# Build with the reveal.js backend
matisse build -i talk.md -o talk/ --backend reveal

# Bundle all assets locally (offline / air-gapped — impress backend only)
matisse build -i talk.md -o talk/ --offline

# PDF-friendly output (no slide animations — impress backend only)
matisse build -i talk.md -o talk/ --pdf

# Generate a sample skeleton with a built-in theme
matisse build --sample mytalk.md --theme beamer-madrid

# List built-in themes (impress backend)
matisse build --print-themes

# List reveal.js built-in themes
matisse build --backend reveal --print-themes

# List available highlight.js styles
matisse build --print-highlight-styles
```
