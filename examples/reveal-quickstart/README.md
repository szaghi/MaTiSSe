# reveal-quickstart

A minimal MaTiSSe presentation built with the **reveal.js** backend.

Covers the essentials: slide structure, LaTeX math, syntax-highlighted code,
speaker notes, and the `$box` environment — all from a single Markdown file.

## Build

```bash
# from the repo root
matisse build -i examples/reveal-quickstart/quickstart.md \
              -o examples/reveal-quickstart/out/ \
              --backend reveal

# then open in your browser
xdg-open examples/reveal-quickstart/out/index.html   # Linux
open     examples/reveal-quickstart/out/index.html   # macOS
```

## Presenter view

Press **S** in the browser to open the presenter view and see speaker notes.

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| `Space` / `→` | Next slide |
| `←` | Previous slide |
| `F` | Full screen |
| `O` | Overview mode |
| `S` | Speaker / presenter view |
| `Esc` | Exit overview or full screen |
