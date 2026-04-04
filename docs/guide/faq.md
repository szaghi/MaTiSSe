# FAQ

## General

**What is MaTiSSe?**

MaTiSSe is a command-line tool that converts Markdown (extended) sources into HTML presentations. It is NOT WYSIWYG — it uses the same approach as LaTeX typesetting.

**Is it WYSIWYG?**

No. You write Markdown, and MaTiSSe compiles it to HTML.

**Can I use it offline?**

Yes. By default MaTiSSe uses a local offline copy of MathJax for equation rendering. Pass `--offline` to also bundle impress.js and highlight.js locally.

**Do I need to know HTML/CSS?**

Basic knowledge is helpful but not required. The YAML theme system lets you control layout without writing HTML.

**What browsers does it work with?**

Any modern browser supporting HTML5/CSS3. Tested with Chrome/Chromium.

**Is MaTiSSe free?**

Yes — released under the [GNU GPL v3](http://www.gnu.org/licenses/gpl-3.0.html).

## Technical

**How does LaTeX equation rendering work?**

MaTiSSe embeds MathJax 3 (from CDN by default). Use `--offline` for a fully local bundle.

**What do `#`, `##`, `###`, `####` headings mean?**

- `#` — Chapter
- `##` — Section
- `###` — Subsection
- `####` — Slide title (starts a new slide)

The first three levels define structure, not content. For content headings use `####` through `######`, or raw HTML (`<h1>`, `<h2>`, `<h3>`).

**Can I use images?**

Yes — standard Markdown image syntax `![alt](image.png)` works, or use the `$figure...$endfigure` environment for captions and layout control.

**What are the special environments?**

`$box`, `$figure`, `$note`, `$table`, `$video` — see the [Advanced](/advanced/) section for each.

**Can I customize the theme?**

Yes. MaTiSSe has an extensive YAML theme system: canvas, headers, footers, sidebars, fonts, colours, per-slide overrides. See the [Theme reference](/reference/themes).

## Installation

**Error: module not found after installation?**

Check your Python version (`python --version` — requires 3.9+) and ensure the virtual environment (if any) is activated.

**MaTiSSe command not found?**

If you installed with `pip install --user`, make sure `~/.local/bin` is in your `PATH`. With `pipx install MaTiSSe.py` the binary is wired up automatically.

**How do I contribute?**

See [Contributing](/guide/contributing).
