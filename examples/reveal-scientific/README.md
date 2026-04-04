# reveal-scientific

A realistic scientific conference talk built with the **reveal.js** backend.

The example demonstrates a computational fluid dynamics (CFD) talk with:

- Title page with full author/affiliation metadata
- Multi-chapter structure (Motivation → Methods → Results → Conclusions)
- Heavy LaTeX mathematics (PDEs, algorithms, convergence analysis)
- Code listings (Python, Fortran)
- Scientific environments: `$box` (theorem/remark), `$table`, `$columns`
- Speaker notes on every slide
- `$note` mapped to `<aside class="notes">` in the presenter view

## Build

```bash
# from the repo root
matisse build -i examples/reveal-scientific/talk.md \
              -o examples/reveal-scientific/out/ \
              --backend reveal

# open in browser
xdg-open examples/reveal-scientific/out/index.html   # Linux
open     examples/reveal-scientific/out/index.html   # macOS
```

## Presenter view

Press **S** to open the presenter view — speaker notes and slide previews appear.

## Try different themes

The reveal.js built-in theme can be set in the `reveal:` YAML block at the top of
`talk.md`.  Available names:

```
beige  black  blood  dracula  league  moon  night  serif  simple  sky  solarized  white
```

> **Note:** reveal-specific YAML settings (`theme`, `transition`) are parsed but
> require a future release to take full effect.  Default: theme `black`, transition `slide`.

## Source structure

```
reveal-scientific/
├── README.md       ← this file
├── metadata.yaml   ← metadata reference (embedded in talk.md)
└── talk.md         ← self-contained source (metadata embedded)
```

> `metadata.yaml` is provided as a readable reference; the metadata is
> already embedded as a YAML block at the top of `talk.md` so the example
> builds correctly from the repo root without `$include` path issues.
