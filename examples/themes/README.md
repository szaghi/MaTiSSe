# Built-in themes showcase

This directory contains a single shared presentation source (`talk.md`) that
can be built with any of MaTiSSe's eight built-in themes.  All build commands
are run from the **repository root**.

## Themes at a glance

| Theme | Layout | Palette |
|-------|--------|---------|
| [beamer-antibes](#beamer-antibes) | Triple header (title / section / subsection) | Navy blue / white |
| [beamer-berkely](#beamer-berkely) | Left sidebar + header | Blue / white |
| [beamer-berlin](#beamer-berlin)   | Triple header + double footer | Navy blue / white |
| [beamer-madrid](#beamer-madrid)   | Header + rich multi-segment footer | Blue / white |
| [matisse](#matisse)               | Right sidebar + header + footer | Sky blue / white |
| [sapienza](#sapienza)             | Header + footer | Crimson / white |
| [solarized-dark](#solarized-dark) | Left sidebar + header + footer | Solarized dark |
| [dracula](#dracula)               | Left sidebar + header + footer | Dracula dark |

## Build all themes at once

```bash
for theme in beamer-antibes beamer-berkely beamer-berlin beamer-madrid matisse sapienza solarized-dark dracula; do
  matisse build \
    -i examples/themes/talk.md \
    -o examples/themes/${theme}/out/ \
    --theme ${theme}
done
```

Then open any of:

```
examples/themes/beamer-antibes/out/index.html
examples/themes/beamer-berkely/out/index.html
examples/themes/beamer-berlin/out/index.html
examples/themes/beamer-madrid/out/index.html
examples/themes/matisse/out/index.html
examples/themes/sapienza/out/index.html
examples/themes/solarized-dark/out/index.html
examples/themes/dracula/out/index.html
```

---

## beamer-antibes

Triple-header layout (title bar / section bar / subsection bar), inspired by
the LaTeX Beamer Antibes theme.  White slide background with navy/indigo chrome.

```bash
matisse build \
  -i examples/themes/talk.md \
  -o examples/themes/beamer-antibes/out/ \
  --theme beamer-antibes
```

---

## beamer-berkely

Left sidebar carrying title, authors, affiliations, and a depth-1 TOC.
Top header shows the current slide title.  Inspired by the LaTeX Beamer
Berkeley theme.  White slide background with blue chrome.

```bash
matisse build \
  -i examples/themes/talk.md \
  -o examples/themes/beamer-berkely/out/ \
  --theme beamer-berkely
```

---

## beamer-berlin

Three stacked headers (depth-1 TOC / subsection / slide title) and a double
footer (authors + title).  Inspired by LaTeX Beamer Berlin.  White slide
background with navy/blue chrome.  Ships with a built-in title page layout.

```bash
matisse build \
  -i examples/themes/talk.md \
  -o examples/themes/beamer-berlin/out/ \
  --theme beamer-berlin
```

---

## beamer-madrid

Bold top header with the slide title and a rich segmented footer (authors /
affiliations / title / conference / slide count).  Inspired by LaTeX Beamer
Madrid.  White slide background with blue/navy chrome.

```bash
matisse build \
  -i examples/themes/talk.md \
  -o examples/themes/beamer-madrid/out/ \
  --theme beamer-madrid
```

---

## matisse

Right sidebar (title, authors, affiliations, depth-2 TOC) + header (slide
title + logo) + footer (timer + slide count).  Coloured canvas background.
Sky-blue gradient palette.

```bash
matisse build \
  -i examples/themes/talk.md \
  -o examples/themes/matisse/out/ \
  --theme matisse
```

---

## sapienza

Header (slide title + logo) and a minimal double footer.  Coloured canvas
background.  Crimson / dark-red palette inspired by Sapienza University of Rome.

```bash
matisse build \
  -i examples/themes/talk.md \
  -o examples/themes/sapienza/out/ \
  --theme sapienza
```

---

## solarized-dark

Left sidebar (title, authors, affiliations, depth-1 TOC) + header (slide
title) + footer (section | subsection breadcrumb + slide count).  Dark canvas
with the full Solarized palette: green headings, orange accents, cream text on
a `#073642` content area.

```bash
matisse build \
  -i examples/themes/talk.md \
  -o examples/themes/solarized-dark/out/ \
  --theme solarized-dark
```

---

## dracula

Left sidebar (title, authors, affiliations, depth-1 TOC) + header (slide
title) + footer (section | subsection breadcrumb + slide count).  Dark canvas
using the official [Dracula palette](https://github.com/dracula/dracula-theme):
purple accents, green headings, orange counters, pink note borders on a
`#282a36` content area.

```bash
matisse build \
  -i examples/themes/talk.md \
  -o examples/themes/dracula/out/ \
  --theme dracula
```
