# Code Highlighting

MaTiSSe uses [Pygments](https://pygments.org/) for **server-side** syntax highlighting.
Code blocks are highlighted at build time — the output HTML contains pre-highlighted markup
with no JavaScript dependency.  Highlighting works identically in online mode, offline mode,
and PDF output.

---

## Fenced code blocks

Use standard Markdown fenced blocks with a language identifier:

````markdown
```python
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```
````

````markdown
```fortran
program hello
  implicit none
  print *, "Hello, World!"
end program hello
```
````

Language identifiers are case-insensitive. Without a language tag, the block is rendered as
plain preformatted text with no colour.

> **Indented code blocks** (4-space indent) are **not** syntax-highlighted by MaTiSSe.
> Always use fenced blocks (`` ``` ``).

---

## Supported languages

Pygments supports over 500 languages. A selection relevant to scientific presentations:

| Domain | Languages |
|---|---|
| General | `python`, `ruby`, `java`, `c`, `cpp`, `rust`, `go` |
| Scientific | `matlab`, `r`, `julia`, `fortran`, `gnuplot` |
| Shell & config | `bash`, `zsh`, `fish`, `powershell`, `ini`, `toml`, `yaml`, `json` |
| Markup | `latex`, `html`, `xml`, `markdown`, `rst` |
| Data & query | `sql`, `sparql` |
| Diff | `diff` |

---

## Selecting a style

### Via the CLI flag

```bash
matisse build -i talk.md -o talk/ --code-style monokai
```

List every available style name:

```bash
matisse build --print-code-styles
```

### Via the theme `code:` section

```yaml
---
theme:
  code:
    style: 'monokai'
---
```

**Precedence:** `theme: code: style:` always overrides the CLI flag.  If neither is set,
the `default` Pygments style is used.

### Disabling highlighting

```bash
matisse build -i talk.md --code-style disable
```

Or in theme YAML (note: this disables `css/pygments.css` generation entirely):

```yaml
---
theme:
  code:
    style: 'disable'
---
```

---

## Available styles

Pygments 2.x ships 48 built-in styles.  A curated selection:

**Dark themes**

| Name | Character |
|---|---|
| `monokai` | Classic dark — green/orange/pink on near-black |
| `dracula` | Purple-tinted dark — well-balanced contrast |
| `github-dark` | GitHub dark mode palette |
| `one-dark` | Atom One Dark |
| `nord` | Arctic cool-blue tones |
| `nord-darker` | Nord with deeper background |
| `gruvbox-dark` | Warm retro dark |
| `material` | Material Design dark |
| `native` | High-contrast dark |
| `inkpot` | Vim inkpot |
| `vim` | Classic Vim dark |
| `zenburn` | Low-contrast muted dark |
| `fruity` | High-chroma dark |

**Light themes**

| Name | Character |
|---|---|
| `default` | Standard Pygments light |
| `friendly` | Readable light |
| `github-light` (via `pastie`) | GitHub light tones |
| `vs` | Visual Studio light |
| `xcode` | Xcode light |
| `solarized-light` | Solarized light |
| `gruvbox-light` | Warm retro light |
| `tango` | GNOME Tango |
| `lovelace` | Elegant light |
| `autumn` | Warm autumn tones |

---

## Customising the code block container

The `code:` theme section accepts any CSS property alongside `style:`.
These are emitted as rules on `.highlight pre` — the preformatted block that
wraps the highlighted tokens.

```yaml
---
theme:
  code:
    style: 'monokai'
    font-size: '85%'
    font-family: '"JetBrains Mono", "Fira Code", monospace'
    border-radius: '6px'
    padding: '0.8em 1.2em'
    border: '1px solid #44475a'
    line-height: '1.5'
---
```

All standard CSS properties are valid here.  Use this section to control:

| Property | Effect |
|---|---|
| `font-size` | Shrink/grow the code relative to body text |
| `font-family` | Monospace font stack |
| `line-height` | Vertical spacing between code lines |
| `padding` | Inner whitespace around the code |
| `border-radius` | Rounded corners on the block |
| `border` | Decorative border |
| `max-height` + `overflow-y: auto` | Scrollable block for long listings |

---

## Overriding individual token colours

Pygments emits a `css/pygments.css` file in the output directory.  It assigns
CSS classes to every token type.  You can override any token colour by injecting
additional CSS rules — the cleanest way is via a `custom_css` field in the theme
(reveal backend) or by appending rules to the `canvas:` or a decorator section
that applies globally.

### Token CSS classes

The most common classes emitted by Pygments:

| Class | Token type |
|---|---|
| `.highlight` | Wrapper `<div>` around the whole block |
| `.highlight pre` | The `<pre>` tag — targeted by `code:` section |
| `.k` | Keyword |
| `.kd` | Keyword.Declaration (`def`, `class`, `int`) |
| `.kn` | Keyword.Namespace (`import`, `use`, `include`) |
| `.kc` | Keyword.Constant (`True`, `None`, `null`) |
| `.n` | Name (generic identifier) |
| `.nf` | Name.Function |
| `.nc` | Name.Class |
| `.nb` | Name.Builtin (`print`, `len`, `range`) |
| `.nn` | Name.Namespace |
| `.s`, `.s1`, `.s2` | String (single/double quoted) |
| `.sd` | String.Doc (docstrings) |
| `.si` | String.Interpol (f-string `{…}` parts) |
| `.c`, `.c1`, `.cm` | Comment (single-line / multi-line) |
| `.m`, `.mi`, `.mf` | Number (integer / float) |
| `.o` | Operator |
| `.ow` | Operator.Word (`and`, `or`, `in`, `not`) |
| `.p` | Punctuation |
| `.err` | Error token |
| `.gd` | Generic.Deleted (diff `−` lines) |
| `.gi` | Generic.Inserted (diff `+` lines) |

### Injecting overrides with a custom CSS file

Add an extra CSS file alongside your source and include it in your metadata:

```yaml
---
metadata:
  - css_overtheme:
    - css/my_overrides.css
---
```

`css/my_overrides.css` (relative to your source file):

```css
/* Make keywords bold and use your accent colour */
.highlight .k,
.highlight .kd,
.highlight .kn { color: #cba6f7; font-weight: bold; }

/* Italicise comments */
.highlight .c,
.highlight .c1,
.highlight .cm { color: #6c7086; font-style: italic; }

/* Override string colour */
.highlight .s,
.highlight .s1,
.highlight .s2 { color: #a6e3a1; }

/* Remove Pygments background so the slide background shows through */
.highlight { background: transparent !important; }
```

The `css_overtheme` metadata key accepts a list of stylesheet paths that are linked
**after** the theme stylesheet, so their specificity naturally overrides Pygments defaults.

### Removing the Pygments background

By default every Pygments style sets a background colour on `.highlight`.  If your slide
background should show through the code block, add:

```css
.highlight { background: transparent !important; }
.highlight pre { background: transparent !important; }
```

---

## Per-slide code block styling

You can change the code appearance for a single slide using an overtheme block:

```markdown
#### Algorithm Listing
---
overtheme:
  code:
    style: 'github-dark'
    font-size: '78%'
    border: '1px solid #30363d'
    border-radius: '6px'
---

```python
def solve(n: int) -> list[int]:
    return list(range(n))
```
```

::: warning One style per presentation
`code: style:` in an overtheme changes `css/pygments.css` only if it differs from the
global style. Currently MaTiSSe generates a single `pygments.css` for the whole
presentation — per-slide style selection affects only the **last** overtheme that sets
one.  For per-slide colour changes, use custom CSS overrides scoped to the slide id
(`#slide-N .highlight { … }`) instead.
:::

---

## How it works — the build pipeline

1. `markdown2html()` converts fenced blocks using Python-Markdown's `codehilite` extension
   with `noclasses=False` (class-based output, not inline styles).
2. The result is a `<div class="highlight"><pre>…</pre></div>` fragment with `<span
   class="…">` tokens — fully static HTML, no JS.
3. `make_output_tree()` calls `get_pygments_css(style)` and writes `css/pygments.css`
   to the output directory.  This stylesheet colours the token classes.
4. If the theme's `code: style:` key differs from the CLI default, `presentation.save()`
   regenerates `css/pygments.css` with the theme-selected style.
5. The renderer links `css/pygments.css` in `<head>` — always a local path, independent
   of online/offline mode.

The `css/pygments.css` file is the **only** place where colours come from.  Overriding
tokens is simply a matter of adding higher-specificity CSS rules after it.

---

## Inline code

Backtick inline code is **not** syntax-highlighted:

```markdown
Call the `fibonacci` function with a positive integer.
```

This is intentional — inline fragments are too short for meaningful tokenisation.
Style them with the `code` CSS selector in a custom stylesheet if needed.
