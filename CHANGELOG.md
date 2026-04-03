# Changelog

All notable changes to MaTiSSe.py are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased] — modernization (2026)

### Breaking changes

- **`--online-MathJax` removed** — replaced by `--offline` (inverted semantics).
  CDN is now the default; pass `--offline` to use local bundled assets.
- **Python 2 and Python < 3.9 dropped** — `python_requires = ">=3.9"`.
- **`dirsync` dependency removed** — replaced by `shutil.copytree(..., dirs_exist_ok=True)`.

### Added

- `--offline` CLI flag: use local bundled copies of impress.js, MathJax and
  highlight.js instead of CDN (useful for air-gapped environments).
- `pyproject.toml` with PEP 517/518 build system, `[tool.pytest]`,
  `[tool.coverage]` and `[tool.ruff]` sections.
- GitHub Actions CI workflow (`.github/workflows/ci.yml`) testing Python
  3.9 – 3.13 in parallel with Codecov coverage upload.
- `ruff` linter added to the `lint` CI job.
- pytest-based test suite: `conftest.py`, `test_integration.py`,
  `test_parser.py`, `test_metadata.py`, `test_theme.py` (99 tests, 2 skipped).

### Changed

- **Frontend assets — CDN by default (online mode):**
  - impress.js 0.5.3 → **2.0** (CDN: `cdn.jsdelivr.net/npm/impress.js@2`)
  - MathJax 2.5.3 → **3.x** (CDN: `cdn.jsdelivr.net/npm/mathjax@3`);
    config updated from deprecated `MathJax.Hub.Config` to the MathJax 3
    `MathJax = { tex: { … } }` object.
  - highlight.js old bundle → **11.9** (CDN: `cdnjs.cloudflare.com`);
    init call updated from `hljs.initHighlightingOnLoad()` → `hljs.highlightAll()`.
- `Theme.set_from()` simplified from 31 individual `deepcopy()` calls to a
  loop over an attribute list.
- `Slide._parse_env()` extracted from the nested closure inside `Slide.to_html()`.
- `Presentation.parse()` decomposed into `__make_toc_slide`, `__build_slides`
  and `__parse_chapters` helpers.
- `setup.py` classifiers updated to Python 3.9 – 3.13; entry point changed
  from `scripts=` to `console_scripts`.
- All f-string conversions applied throughout the codebase.
- `frosted` linter removed (unmaintained); flake8 line-length reduced 500 → 120.

### Fixed

- `dict.keys()[0]` crash on Python 3 in `Theme.copy_from()` — replaced with
  `next(iter(css.keys()))`.
- `markdown.util.etree` removal in markdown 3.0 — both markdown extensions
  updated to use `xml.etree.ElementTree`.
- `extendMarkdown(self, md, md_globals)` incompatible signature — removed
  `md_globals` parameter.
- `MathJaxInlineProcessor` migrated from legacy `Pattern` / `.add()` API to
  `InlineProcessor` / `.register()` (markdown ≥ 3.0).
- Dead CDN URL `cdn.mathjax.org` (shut down 2017) — replaced with
  `cdn.jsdelivr.net/npm/mathjax@3`.
- Duplicate accumulation in `__get_highlight_styles` and `__get_themes` class
  lists — lists now cleared before repopulating.
- All `from __future__ import` compatibility shims removed.
- Trailing bare `return` statements removed from void methods.
- Quadruple-quote `""""` syntax error in `slide.py`.
- All docstring typos fixed.

---

## [1.3.3] — 2018-10-09

Last release before the 2026 modernization effort.

---

## [1.3.2] — 2018-10-08

---

## [1.3.1] — 2018-09-27

---

## [1.3.0] — 2018-09-27

---

## [1.2.x] — 2017

---

## [1.1.x] — 2017

---

## [1.0.x] — 2016 – 2017

---

## [0.x] — 2015 – 2016

Initial public releases.

---

[Unreleased]: https://github.com/szaghi/MaTiSSe/compare/v1.3.3...HEAD
[1.3.3]: https://github.com/szaghi/MaTiSSe/releases/tag/v1.3.3
