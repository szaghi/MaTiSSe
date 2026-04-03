# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MaTiSSe.py** (Markdown To Impressive Scientific Slides) is a CLI tool that converts Markdown source files into high-quality HTML/CSS presentations with strong support for scientific content (LaTeX equations, figures, tables, code listings). It uses `impress.js` for presentation rendering and `MathJax` for equation rendering.

Current version: **1.3.3**

## Commands

### Install (development)
```bash
pip install -e ".[dev]"   # editable install with dev dependencies
make dev                  # same, via Makefile
```

### Run
```bash
MaTiSSe.py -i source.md -o output_dir    # Convert markdown to presentation
MaTiSSe.py --sample mytalk.md            # Generate a sample presentation
MaTiSSe.py --print-themes                # List builtin themes
MaTiSSe.py --print-highlight-styles      # List code highlight styles
MaTiSSe.py -i source.md -o output --pdf  # Generate PDF-friendly output (no impress.js)
MaTiSSe.py -i source.md -o output --offline  # Copy JS/CSS bundles locally instead of using CDN
```

### Tests
```bash
make test                 # Run full test suite with coverage
python -m pytest          # Same
python -m pytest tests/test_parser.py   # Run a single test module
```

Tests live in `tests/`. Fixtures are in `tests/compare/*/test.md`; generated HTML output goes into `tests/compare/*/test*/` (gitignored).

### Lint / Format
```bash
make lint                 # ruff check
make fmt                  # ruff check --fix + ruff format
```

### Clean
```bash
make clean                # remove dist/, build/, .pytest_cache, .coverage, coverage.xml
```

## Architecture

### Source Layout (flat)
```
matisse/                  # Main package (flat layout — importable directly)
  __init__.py             # Package version (__version__ = "1.3.3")
  matisse.py              # CLI entry point + main()
  __main__.py             # python -m matisse
  presentation.py         # Presentation class — top-level HTML orchestrator
  parser.py               # Regex-based markdown tokenization
  matisse_config.py       # Configuration, output tree setup, asset copying
  theme.py                # Theme parsing and CSS generation from YAML
  chapter.py              # Chapter model
  section.py              # Section model
  subsection.py           # Subsection model
  slide.py                # Slide model + HTML generation
  metadata.py             # Presentation metadata (YAML front matter)
  position.py             # Slide positioning
  figure.py               # Figure environment
  box.py                  # Box environment
  note.py                 # Note environment
  table.py                # Table environment
  video.py                # Video environment
  columns.py              # Columns layout
  mdx_mathjax.py          # MathJax markdown extension (InlineProcessor API)
  mdx_custom_span_class.py  # Custom span class markdown extension
  markdown_utils.py       # Markdown processing utilities
  utils/                  # Static assets (CSS, JS, themes) — omitted from coverage
tests/
  conftest.py             # Session fixtures (MatisseConfig, compare_dirs)
  test_integration.py     # End-to-end rendering tests against compare/ fixtures
  test_parser.py          # Unit tests for parser.py
  test_metadata.py        # Unit tests for metadata.py
  test_theme.py           # Unit tests for theme.py
  compare/                # Test fixture directories (each contains test.md)
pyproject.toml            # Build, pytest, coverage, ruff config
Makefile                  # dev / test / lint / fmt / clean
.github/workflows/ci.yml  # CI: test on Python 3.9–3.13 + lint
```

### Key Architectural Patterns

**Hierarchical document model**: Presentations are structured as `Chapter > Section > Subsection > Slide`. Each level is parsed from Markdown headings (`#`, `##`, `###`, `####`).

**Custom Markdown syntax**: The parser (`parser.py`) uses regex to tokenize the source. Beyond standard Markdown headings, it supports:
- `$titlepage` — special slide for the title page
- `$include(file)` — include external files recursively
- YAML blocks (`---`) for metadata and theme definitions
- Custom environments: `$note...$endnote`, `$figure...$endfigure`, `$box...$endbox`, `$table...$endtable`, `$video...$endvideo`

**Theme system**: Presentation visuals are defined via YAML theme blocks. Each `Theme` object defines CSS rules for canvas, slide layout (headers, footers, sidebars, content), boxes, figures, notes, tables, and TOC. Themes support `copy-from-theme` for inheritance and per-slide overrides ("overtheme").

**HTML generation**: `Presentation.to_html()` uses `yattag` to generate HTML. By default, JS/CSS (impress.js 2, MathJax 3, highlight.js 11) are loaded from CDN. Pass `--offline` to copy bundles into the output directory instead. Each slide gets impress.js data attributes for positioning/transitions. Output is a self-contained directory with `index.html`, `css/`, and `js/` subdirectories.

**Metadata templating**: Presentation metadata (title, authors, affiliations, etc.) is defined in YAML front matter and interpolated into themes using `$metadata_name` placeholders.

### Dependencies
- **Runtime**: `markdown`, `yattag`, `pyyaml`
- **Dev**: `pytest`, `pytest-cov`, `ruff`

### Python Version
Supports Python 3.9+. CI tests on 3.9, 3.10, 3.11, 3.12, 3.13.

## Important Notes

- Builtin themes are in `matisse/utils/builtin_themes/`.
- highlight.js styles are in `matisse/utils/js/highlight/styles/`.
- Version is defined in `matisse/__init__.py` and read dynamically by `pyproject.toml`.
- `matisse/utils/` is excluded from coverage (static assets only).
- The `release/` directory (if present) contains stale bundled archives — do not modify it.
