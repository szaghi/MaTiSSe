<div align="center">

# MaTiSSe.py

[![CI](https://github.com/szaghi/MaTiSSe/actions/workflows/ci.yml/badge.svg)](https://github.com/szaghi/MaTiSSe/actions/workflows/ci.yml)
[![Latest Version](https://img.shields.io/pypi/v/MaTiSSe.py.svg)](https://pypi.org/project/MaTiSSe.py/)
[![GitHub tag](https://img.shields.io/github/tag/szaghi/MaTiSSe.svg)]()
[![GitHub issues](https://img.shields.io/github/issues/szaghi/MaTiSSe.svg)](https://github.com/szaghi/MaTiSSe/issues)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org)

[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0.html)

> Markdown To Impressive Scientific Slides — a KISS CLI that compiles plain Markdown into
> high-quality, self-contained HTML presentations with full scientific-content support.

<div>
<table>
<tr>
<td><b>📝 Markdown-first authoring</b><br><sub>Write clean, readable Markdown — no HTML, no LaTeX preamble. MaTiSSe extends standard syntax with chapter/section/subsection headings, a <code>$titlepage</code> directive, and <code>$include()</code> for multi-file compositions. <a href="https://szaghi.github.io/MaTiSSe/reference/markdown-syntax">Syntax reference</a></sub></td>
<td><b>🎨 YAML theme system</b><br><sub>Define canvas, headers, footers, sidebars, and content areas entirely in YAML blocks. Apply per-slide overrides with <em>overtheme</em>. Six built-in LaTeX-Beamer-style themes ready to use out of the box. <a href="https://szaghi.github.io/MaTiSSe/reference/themes">Theme reference</a></sub></td>
</tr>
<tr>
<td><b>🔢 LaTeX equations</b><br><sub>Inline <code>$…$</code> and display <code>$$…$$</code> math rendered by MathJax 3 — no extra setup required. Works in slide content, box captions, figure captions, and headers. <a href="https://szaghi.github.io/MaTiSSe/advanced/math">Math guide</a></sub></td>
<td><b>🔬 Scientific environments</b><br><sub>First-class environments for figures, boxes, notes, tables, videos, and multi-column layouts — each fully customizable via CSS and YAML. <a href="https://szaghi.github.io/MaTiSSe/advanced/figures">Figures</a> · <a href="https://szaghi.github.io/MaTiSSe/advanced/boxes">Boxes</a> · <a href="https://szaghi.github.io/MaTiSSe/advanced/columns">Columns</a></sub></td>
</tr>
<tr>
<td><b>✨ Syntax-highlighted code</b><br><sub>Code blocks rendered by highlight.js 11 with 100+ bundled styles. Tab-completion on <code>--highlight-style</code> lets you preview styles instantly. <a href="https://szaghi.github.io/MaTiSSe/reference/cli">CLI reference</a></sub></td>
<td><b>📦 Offline &amp; PDF modes</b><br><sub><code>--offline</code> bundles all JS/CSS assets locally for air-gapped environments. <code>--pdf</code> disables impress.js animations for clean PDF printing. <a href="https://szaghi.github.io/MaTiSSe/reference/cli">CLI reference</a></sub></td>
</tr>
<tr>
<td><b>🆓 Free and open source</b><br><sub>Released under the GNU GPL v3 license. Free to use, study, modify, and distribute. Contributions welcome — see the <a href="CONTRIBUTING.md">contributing guidelines</a>.</sub></td>
<td><b>🖥️ Powered by impress.js</b><br><sub>Each slide gets full impress.js positioning and transition support — rotate, scale, translate in 3D. Or disable animations entirely with <code>--pdf</code>. <a href="https://szaghi.github.io/MaTiSSe/guide/quickstart">Quick start</a></sub></td>
</tr>
</table>
</div>

**[Full documentation](https://szaghi.github.io/MaTiSSe/)** — installation, quick start, CLI reference, theme gallery

</div>

## Why MaTiSSe.py?

LaTeX Beamer produces beautiful slides, but its compile cycle is slow and its syntax is noisy. PowerPoint and Keynote are WYSIWYG and therefore hard to version-control or script. Modern presentation frameworks like impress.js are impressive but require hand-written HTML.

MaTiSSe.py takes a different path: you write clean, readable Markdown — with optional YAML theme blocks and a handful of scientific-content environments — and MaTiSSe.py compiles it into a self-contained HTML/CSS/JS presentation.

```bash
# Generate a sample and build it immediately
MaTiSSe.py build --sample mytalk.md --theme beamer-madrid
MaTiSSe.py build -i mytalk.md -o mytalk/
```

Open `mytalk/index.html` in a browser and navigate with arrow keys or spacebar.

| **Title page** | **Figure environment** |
|:---:|:---:|
| ![Title page](screenshots/01.png) | ![Figures](screenshots/02.png) |
| **LaTeX equations** | **LaTeX-Beamer themes** |
| ![Equations](screenshots/03.png) | ![Themes](screenshots/04.png) |

## Main features

* [x] `markdown-to-html` slides builder with extended Markdown syntax;
* [x] structured presentations: chapters, sections, subsections, slides;
* [x] presentation metadata (title, authors, affiliations, …) with `$key` interpolation into themes;
* [x] automatic table of contents slides (`--toc-at-chap-beginning`, `--toc-at-sec-beginning`, …);
* [x] flexible **theme system** defined entirely in YAML:
    * [x] canvas, headings, headers, footers, sidebars, content areas;
    * [x] per-slide theme overrides (*overtheme*);
    * [x] six built-in LaTeX-Beamer-style themes (`beamer-antibes`, `beamer-berkely`, `beamer-berlin`, `beamer-madrid`, `matisse`, `sapienza`);
* [x] **LaTeX equations** via MathJax 3 (inline `$…$` and display `$$…$$`);
* [x] scientific content environments:
    * [x] `$figure…$endfigure` with captions and custom CSS;
    * [x] `$box…$endbox` fully customizable;
    * [x] `$note…$endnote`;
    * [x] `$table…$endtable`;
    * [x] `$video…$endvideo`;
    * [x] `$columns…$endcolumns` multi-column layout;
* [x] syntax-highlighted code listings via highlight.js 11 (100+ styles);
* [x] `$include(file)` for composing presentations from multiple source files;
* [x] `--offline` mode: all JS/CSS assets bundled locally (air-gapped environments);
* [x] `--pdf` mode: animations disabled for clean PDF printing;
* [x] shell tab-completion for `--theme` and `--highlight-style`;
* [x] powered by [impress.js](https://impress.js.org/) for 3D-capable slide transitions.

## Author

**Stefano Zaghi** — [stefano.zaghi@gmail.com](mailto:stefano.zaghi@gmail.com) · [GitHub](https://github.com/szaghi)

## Copyrights

MaTiSSe.py is an open source project distributed under the [GPL v3](https://www.gnu.org/licenses/gpl-3.0.html) license. Anyone interested in using, developing, or contributing to MaTiSSe.py is welcome — see the [contributing guidelines](CONTRIBUTING.md).
