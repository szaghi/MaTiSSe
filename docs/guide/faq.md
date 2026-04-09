# FAQ

## General

**What is MaTiSSe?**

MaTiSSe is a command-line tool that converts Markdown (extended) sources into HTML presentations. It is NOT WYSIWYG — it uses the same approach as LaTeX typesetting.

**Is it WYSIWYG?**

No. You write Markdown, and MaTiSSe compiles it to HTML.

**Can I use it offline?**

Yes. Syntax highlighting (Pygments) is always local — no network call needed. Pass `--offline` to also bundle impress.js and MathJax locally. Diagram engines (Mermaid, Graphviz) require a network connection even with `--offline`; see [Diagrams](/advanced/diagrams#offline-mode).

**Do I need to know HTML/CSS?**

Basic knowledge is helpful but not required. The YAML theme system lets you control layout without writing HTML. For fine-grained tweaks use the `css_overtheme` metadata key to supply a custom CSS file.

**What browsers does it work with?**

Any modern browser supporting HTML5/CSS3. Tested with Chrome/Chromium.

**Is MaTiSSe free?**

Yes — released under the [GNU GPL v3](http://www.gnu.org/licenses/gpl-3.0.html).

---

## Technical

**How does LaTeX equation rendering work?**

MaTiSSe embeds MathJax 3 (from CDN by default). Use `--offline` for a fully local bundle.

**What do `#`, `##`, `###`, `####` headings mean?**

- `#` — Chapter
- `##` — Section
- `###` — Subsection
- `####` — Slide title (starts a new slide)

The first three levels define structure, not content. For content headings inside a slide use `#####`, `######`, or raw HTML (`<h1>`, `<h2>`, `<h3>`).

See [Core Concepts](/guide/concepts) for a full explanation of the document hierarchy.

**Can I use images?**

Yes — standard Markdown image syntax `![alt](image.png)` works, or use the `$figure...$endfigure` environment for captions and layout control.

**What are the special environments?**

`$box`, `$figure`, `$note`, `$table`, `$video`, `$columns` — see the [Advanced](/advanced/) section for each. There are also fenced-div environments: [Callout Blocks](/advanced/callouts), [Theorems & Proofs](/advanced/theorems), and [Diagrams](/advanced/diagrams).

**Can I auto-number theorems, figures, and tables?**

Yes. Theorem-like blocks (`thm`, `lem`, `def`, etc.) are auto-numbered per type. Cross-reference any labelled block with `@PREFIX-id` syntax — it resolves to e.g. "Theorem 1". See [Theorems & Proofs](/advanced/theorems).

**Can I embed Mermaid or Graphviz diagrams?**

Yes. Use ` ```{mermaid} ` or ` ```{dot} ` fenced blocks. The required CDN scripts are injected into `index.html` automatically. See [Diagrams](/advanced/diagrams).

**Can I customize the theme?**

Yes. MaTiSSe has an extensive YAML theme system: canvas, headers, footers, sidebars, fonts, colours, per-slide overrides. See the [Theme reference](/reference/themes). For CSS that goes beyond what YAML supports, use `css_overtheme` in your metadata.

**Can I reveal slide content step by step?**

Yes. Use `::: {.incremental}` for bullet lists, `. . .` to pause between paragraphs, or `$substep … $endsubstep` blocks (impress.js only). See [Incremental Reveals](/advanced/incremental).

**What is the difference between `$note` and callout blocks?**

`$note...$endnote` is a classic MaTiSSe environment styled via the theme's `entities.note` section. On the reveal.js backend it becomes a speaker note. Callout blocks (`::: {.callout-*}`) are semantic, have type-specific icons and colours, and work the same on both backends. Use callouts for in-slide emphasis; use `$note` when you want the content to appear as a speaker note in reveal.js.

---

## Installation

**Error: module not found after installation?**

Check your Python version (`python --version` — requires 3.9+) and ensure the virtual environment (if any) is activated.

**MaTiSSe command not found?**

If you installed with `pip install --user`, make sure `~/.local/bin` is in your `PATH`. With `pipx install MaTiSSe.py` the binary is wired up automatically.

**How do I contribute?**

See [Contributing](/guide/contributing).
