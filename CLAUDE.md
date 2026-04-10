# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MaTiSSe.py** (Markdown To Impressive Scientific Slides) is a CLI tool that converts Markdown source files into high-quality HTML/CSS presentations with strong support for scientific content (LaTeX equations, figures, tables, code listings). It supports two rendering backends: **impress.js** (default) and **reveal.js**. MathJax renders equations.

Current version: **1.7.3**

## Commands

### Install (development)
```bash
pip install -e ".[dev]"   # editable install with dev dependencies
make dev                  # same, via Makefile
```

### Run
```bash
MaTiSSe.py -i source.md -o output_dir        # Convert markdown to presentation (impress.js)
MaTiSSe.py -i source.md -o output --reveal   # Use reveal.js backend
MaTiSSe.py --sample mytalk.md                # Generate a sample presentation
MaTiSSe.py --print-themes                    # List builtin themes
MaTiSSe.py --print-highlight-styles          # List code highlight styles
MaTiSSe.py -i source.md -o output --pdf      # Generate PDF-friendly output (no impress.js)
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

### Source Layout
```
matisse/                    # Main package (flat layout — importable directly)
  __init__.py               # Package version (__version__ = "1.7.3")
  matisse.py                # CLI shim — delegates to matisse_config.py; keeps console-script working
  __main__.py               # python -m matisse
  presentation.py           # Presentation class — top-level HTML orchestrator
  parser.py                 # Regex-based markdown tokenization
  matisse_config.py         # Configuration, output tree setup, asset copying
  metadata.py               # Presentation metadata (YAML front matter)
  chapter.py                # Chapter model
  section.py                # Section model
  subsection.py             # Subsection model
  slide.py                  # Slide model + HTML generation
  position.py               # Slide positioning (top-level shim)
  theme.py                  # Backward-compat shim → backends.impress.theme.ImpressTheme
  figure.py                 # Figure environment
  figure_group.py           # Subfigure layout environment
  box.py                    # Box environment
  note.py                   # Note environment
  table.py                  # Table environment
  video.py                  # Video environment
  columns.py                # Columns layout
  callout.py                # Callout block environments
  diagram.py                # Mermaid and Graphviz diagram environments
  incremental.py            # Incremental list environment
  substep.py                # Substep environment (impress.js Substep plugin)
  theorem.py                # Theorem, lemma, and proof environments
  labels.py                 # Label registry and cross-reference support
  markdown_utils.py         # Markdown processing utilities
  mdx_mathjax.py            # MathJax markdown extension (InlineProcessor API)
  mdx_custom_span_class.py  # Custom span class markdown extension
  mdx_quarto_span.py        # Quarto-style inline span extension ([text]{attrs})
  mdx_strikethrough.py      # Strikethrough extension (~~text~~ → <del>)
  mdx_sup_sub.py            # Superscript/subscript extension
  backends/                 # Rendering backends subpackage
    base.py                 # Abstract base classes and shared utilities
    impress/                # impress.js backend
      renderer.py           # HTML renderer for impress.js
      theme.py              # ImpressTheme — CSS generation from YAML
      position.py           # Slide positioning for impress.js
    reveal/                 # reveal.js backend
      renderer.py           # HTML renderer for reveal.js
      theme.py              # RevealTheme — CSS generation for reveal.js
  utils/                    # Static assets (CSS, JS, themes) — omitted from coverage
tests/
  conftest.py               # Session fixtures (MatisseConfig, compare_dirs)
  create.py                 # Test fixture creation helpers
  suite_tests.py            # Test suite utilities
  test_integration.py       # End-to-end rendering tests against compare/ fixtures
  test_parser.py            # Unit tests for parser.py
  test_metadata.py          # Unit tests for metadata.py
  test_theme.py             # Unit tests for theme.py
  test_cli.py               # CLI argument parsing tests
  test_code_highlighting.py # Code block highlighting tests
  test_impress_features.py  # impress.js-specific feature tests
  test_inline_extensions.py # Inline markdown extension tests
  test_base_decorators.py   # Base class decorator tests
  test_phase62_features.py  # Phase 6.2 feature tests (callout, diagram, theorem, etc.)
  test_reveal_backend.py    # reveal.js backend unit tests
  test_reveal_integration.py # reveal.js end-to-end tests
  test_reveal_theme.py      # reveal.js theme tests
  compare/                  # Test fixture directories (each contains test.md)
pyproject.toml              # Build, pytest, coverage, ruff config
Makefile                    # dev / test / lint / fmt / clean
.github/workflows/ci.yml    # CI: test on Python 3.9–3.13 + lint
```

### Key Architectural Patterns

**Hierarchical document model**: Presentations are structured as `Chapter > Section > Subsection > Slide`. Each level is parsed from Markdown headings (`#`, `##`, `###`, `####`).

**Backend architecture**: HTML generation is delegated to swappable backends (`backends/impress/`, `backends/reveal/`). Each backend provides its own renderer and theme. Top-level `theme.py` and `position.py` are backward-compat shims pointing at the impress backend.

**Custom Markdown syntax**: The parser (`parser.py`) uses regex to tokenize the source. Beyond standard Markdown headings, it supports:
- `$titlepage` — special slide for the title page
- `$include(file)` — include external files recursively
- YAML blocks (`---`) for metadata and theme definitions
- Custom environments: `$note...$endnote`, `$figure...$endfigure`, `$box...$endbox`, `$table...$endtable`, `$video...$endvideo`, `$callout...$endcallout`, `$theorem...$endtheorem`, `$diagram...$enddiagram`
- Inline extensions: `[text]{.class}` (Quarto-style spans), `~~strikethrough~~`, `^sup^`, `~sub~`

**Theme system**: Presentation visuals are defined via YAML theme blocks. Each `Theme` object defines CSS rules for canvas, slide layout (headers, footers, sidebars, content), boxes, figures, notes, tables, and TOC. Themes support `copy-from-theme` for inheritance and per-slide overrides ("overtheme").

**HTML generation**: Each backend's renderer assembles the final HTML. By default, JS/CSS are loaded from CDN. Pass `--offline` to copy bundles into the output directory instead. Output is a self-contained directory with `index.html`, `css/`, and `js/` subdirectories.

**Metadata templating**: Presentation metadata (title, authors, affiliations, etc.) is defined in YAML front matter and interpolated into themes using `$metadata_name` placeholders.

**CLI**: Built with `typer`. Entry point is `matisse.matisse:main` (shim) → `matisse_config.py`.

### Dependencies
- **Runtime**: `markdown`, `yattag`, `pyyaml`, `typer>=0.9.0`, `pygments>=2.14`
- **Dev**: `pytest`, `pytest-cov`, `ruff`

### Python Version
Supports Python 3.9+. CI tests on 3.9, 3.10, 3.11, 3.12, 3.13.

## Release Workflow

Uses **trunk-based development** on `master`. No release branches, no develop branch.

```bash
./release.sh --major | --minor | --patch | X.Y.Z
```

The script: pre-flight checks → lint → confirm → bump `matisse/__init__.py` → generate `docs/guide/changelog.md` → run tests → commit → tag → `git push origin master --follow-tags`.

PyPI publish is triggered automatically by the tag push via CI — never publish locally.

## Important Notes

- Builtin themes are in `matisse/utils/builtin_themes/`.
- highlight.js styles are in `matisse/utils/js/highlight/styles/`.
- Version is defined in `matisse/__init__.py` and read dynamically by `pyproject.toml`.
- `matisse/utils/` is excluded from coverage (static assets only).
- The `release/` directory (if present) contains stale bundled archives — do not modify it.
