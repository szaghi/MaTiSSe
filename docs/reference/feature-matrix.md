# Feature Matrix

Quick reference mapping every MaTiSSe feature to its activation mechanism and
backend support.  Columns:

- **CLI flag** — command-line option
- **YAML key** — metadata or theme YAML key
- **Markdown directive** — source-level syntax
- **impress** — supported by the default impress.js backend
- **reveal** — supported by the reveal.js backend (`--backend reveal`)

---

## Document structure

| Feature | Markdown directive | impress | reveal |
|---|---|---|---|
| Chapter | `# heading` | ✓ | ✓ |
| Section | `## heading` | ✓ | ✓ |
| Subsection | `### heading` | ✓ | ✓ |
| Slide | `#### heading` | ✓ | ✓ |
| Title page | `$titlepage` / `$titlepage[plain]` | ✓ | ✓ |
| File inclusion | `$include(path)` | ✓ | ✓ |

---

## CLI options

| Feature | Flag | impress | reveal |
|---|---|---|---|
| Input file | `-i FILE` | ✓ | ✓ |
| Output directory | `-o DIR` | ✓ | ✓ |
| Backend selection | `--backend {impress\|reveal}` | ✓ | ✓ |
| Generate sample | `--sample FILE` | ✓ | ✓ |
| Apply built-in theme | `--theme NAME` | ✓ | ✓ |
| Offline bundling | `--offline` | ✓ | ✗ |
| PDF-friendly output | `--pdf` | ✓ | ✗ (use `?print-pdf` URL) |
| Code highlight style | `--code-style STYLE` | ✓ | ✓ |
| TOC at chapter start | `--toc-at-chap-beginning DEPTH` | ✓ | ✓ |
| TOC at section start | `--toc-at-sec-beginning DEPTH` | ✓ | ✓ |
| TOC at subsection start | `--toc-at-subsec-beginning DEPTH` | ✓ | ✓ |
| List built-in themes | `--print-themes` | ✓ | ✓ |
| List code styles | `--print-code-styles` | ✓ | ✓ |
| Verbose build output | `--verbose` | ✓ | ✓ |
| Print expanded source | `--print-parsed-source` | ✓ | ✓ |
| Install shell completion | `--install-completion {bash\|zsh\|fish}` | ✓ | ✓ |

---

## Metadata keys

| Key | Type | Description | impress | reveal |
|---|---|---|---|---|
| `title` | string | Presentation title | ✓ | ✓ |
| `subtitle` | string | Subtitle | ✓ | ✓ |
| `authors` | list | Full author names | ✓ | ✓ |
| `authors_short` | list | Abbreviated authors | ✓ | ✓ |
| `emails` | list | Author emails | ✓ | ✓ |
| `affiliations` | list | Full affiliations | ✓ | ✓ |
| `affiliations_short` | list | Abbreviated affiliations | ✓ | ✓ |
| `date` | string | Presentation date | ✓ | ✓ |
| `conference` | string | Conference name | ✓ | ✓ |
| `conference_short` | string | Abbreviated conference | ✓ | ✓ |
| `session` | string | Session name | ✓ | ✓ |
| `session_short` | string | Abbreviated session | ✓ | ✓ |
| `location` | string | Venue location | ✓ | ✓ |
| `location_short` | string | Abbreviated location | ✓ | ✓ |
| `logo` | string | Logo image path | ✓ | ✓ |
| `max_time` | integer | Timer duration (minutes) | ✓ | ✓ |
| `dirs_to_copy` | list | Asset directories to copy | ✓ | ✓ |
| `css_overtheme` | list | Custom CSS files | ✓ | ✓ |

---

## Theme sections

| Section | YAML key | Description |
|---|---|---|
| Colour variables | `theme.palette` | Named variables referenced as `$varname` |
| Viewport background | `theme.canvas` | Body background behind all slides |
| List styling | `theme.lists` | Bullets, counters, markers |
| TOC styling | `theme.toc` | Active entry emphasis per hierarchy level |
| Slide container | `theme.layout.slide` | Dimensions, transitions, impress.js data-* |
| Content area | `theme.layout.content` | Font, colour, padding of the text region |
| Header bands | `theme.layout.header-N` | Full-width bands above content |
| Footer bands | `theme.layout.footer-N` | Full-width bands below content |
| Sidebar bands | `theme.layout.sidebar-N` | Vertical bands left/right of content |
| Environment defaults | `theme.entities` | box, note, table, figure, video |
| Code blocks | `theme.code` | Pygments style + code container CSS |
| Per-slide override | `overtheme:` | Same schema as theme + `copy-from-theme` |

---

## Content environments

| Environment | Syntax | impress | reveal |
|---|---|---|---|
| Box | `$box … $endbox` | ✓ | ✓ |
| Note | `$note … $endnote` | ✓ | ✓ (→ speaker note) |
| Figure | `$figure … $endfigure` | ✓ | ✓ |
| Table | `$table … $endtable` | ✓ | ✓ |
| Video | `$video … $endvideo` | ✓ | ✓ |
| Columns | `$columns … $endcolumns` | ✓ | ✓ |
| Callout | `::: {.callout-TYPE}` | ✓ | ✓ |
| Theorem / lemma / … | `::: {#PREFIX-id}` | ✓ | ✓ |
| Proof | `::: {.proof}` | ✓ | ✓ |
| Mermaid diagram | ` ```{mermaid} ` | ✓ | ✓ |
| Graphviz diagram | ` ```{dot} ` | ✓ | ✓ |

---

## Incremental reveals

| Feature | Syntax | impress | reveal |
|---|---|---|---|
| Incremental list | `::: {.incremental}` | ✓ (substep) | ✓ (fragment) |
| Pause token | `. . .` | ✓ | ✓ |
| Substep block | `$substep … $endsubstep` | ✓ | ✗ |
| Ordered substeps | `$substep[order:N]` | ✓ | ✗ |

---

## Inline formatting extensions

| Feature | Syntax | impress | reveal |
|---|---|---|---|
| Strikethrough | `~~text~~` | ✓ | ✓ |
| Superscript | `^text^` | ✓ | ✓ |
| Subscript | `~text~` | ✓ | ✓ |
| Quarto span | `[text]{.classname}` | ✓ | ✓ |
| Legacy span | `!!classname\|text!!` | ✓ | ✓ |
| Footnotes | `[^ref]` / `[^ref]: …` | ✓ | ✓ |
| Definition list | `Term\n: definition` | ✓ | ✓ |
| Image attributes | `![alt](img){width="60%"}` | ✓ | ✓ |
| Underline span | `[text]{.underline}` | ✓ | ✓ |
| Highlighted span | `[text]{.mark}` | ✓ | ✓ |
| Small caps span | `[text]{.smallcaps}` | ✓ | ✓ |

---

## Math and code

| Feature | Syntax / flag | impress | reveal |
|---|---|---|---|
| Inline math | `$...$` | ✓ | ✓ |
| Display math | `$$...$$` | ✓ | ✓ |
| Literal dollar | `\$` | ✓ | ✓ |
| Code highlighting | fenced ` ``` ` blocks | ✓ | ✓ |
| Highlight style (CLI) | `--code-style NAME` | ✓ | ✓ |
| Highlight style (theme) | `theme.code.style` | ✓ | ✓ |
| Per-slide code style | `overtheme.code.style` | ✓ | ✓ |
| GFM checklists | `- [x] item` | ✓ | ✓ |

---

## Built-in themes

### impress.js themes

| Name | Structure | Colours |
|---|---|---|
| `matisse` | Right sidebar + header + footer | Blue gradient |
| `sapienza` | Header + footer | Sapienza red |
| `dracula` | Left sidebar + header + footer | Dracula dark |
| `solarized-dark` | Left sidebar + header + footer | Solarized dark |
| `beamer-antibes` | Three stacked headers | Beamer blue |
| `beamer-berkely` | Left sidebar + header | Beamer blue |
| `beamer-berlin` | Three headers + two footers | Beamer dark blue |
| `beamer-madrid` | Header + footer | Beamer blue |

### reveal.js themes (built into reveal.js)

`black`, `white`, `moon`, `sky`, `beige`, `night`, `serif`, `solarized`,
`dracula`, `blood`, `league`, `simple`

---

## Cross-reference labels

| Prefix | Display label |
|---|---|
| `fig` | Figure |
| `tbl` | Table |
| `eq` | Equation |
| `sec` | Section |
| `dia` | Diagram |
| `thm` | Theorem |
| `lem` | Lemma |
| `cor` | Corollary |
| `prp` | Proposition |
| `def` | Definition |
| `exm` | Example |
| `exr` | Exercise |
| `rem` | Remark |

Syntax: label with `{#PREFIX-id}`, reference with `@PREFIX-id`.
See [Theorems & Proofs](/advanced/theorems#cross-references).
