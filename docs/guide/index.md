# About MaTiSSe.py

**MaTiSSe.py** (*Markdown To Impressive Scientific Slides*) is a command-line tool that converts Markdown source files into high-quality HTML/CSS presentations.

## Goals

Scientific speakers need:

- **Equations** — inline and display math, correctly rendered
- **Code listings** — syntax-highlighted, copy-friendly
- **Structured layouts** — multi-column, sidebars, headers, footers
- **Reproducibility** — source in version control, output fully deterministic
- **Portability** — a single output directory that runs in any browser

MaTiSSe.py addresses all of these from a single Markdown file.

## How it works

A MaTiSSe source file is standard Markdown with a few extensions:

| Construct | Meaning |
|---|---|
| `# Heading` | Chapter |
| `## Heading` | Section |
| `### Heading` | Subsection |
| `#### Heading` | Slide title |
| `$titlepage` | Title slide |
| `---` YAML `---` | Metadata or theme block |
| `$figure...$endfigure` | Figure environment |
| `$box...$endbox` | Box environment |
| `$note...$endnote` | Note environment |
| `$table...$endtable` | Table environment |
| `$video...$endvideo` | Video environment |

MaTiSSe parses the source, applies the theme, and generates a self-contained output directory containing `index.html`, `css/`, and `js/`.

## Output

The output is powered by [impress.js](https://impress.js.org/) for slide transitions and positioning, [MathJax 3](https://www.mathjax.org/) for equation rendering, and [highlight.js 11](https://highlightjs.org/) for code highlighting. By default all three are loaded from CDN; pass `--offline` to bundle them locally.

## Architecture

```
Chapter (# heading)
└── Section (## heading)
    └── Subsection (### heading)
        └── Slide (#### heading)
```

Each level contributes to the automatically generated table of contents and to theme inheritance.
