# showcase

A real talk built with the **reveal.js** backend: *FLUME on ADAM*, compressible flows and MHD on adaptive grids. Every
equation, number and figure comes from the [FLUME verification pages](https://szaghi.github.io/adam/applications/flume/verification/);
nothing is invented. It doubles as a demonstration of a fully custom theme written in the presentation's own YAML.

What it shows:

- a title page in raw HTML over a full-bleed per-slide background (`overtheme.reveal.background_image`): the blast-front
  ensō over its refined quadtree, the mark of [similitudo.eu](https://similitudo.eu), with the seal stamped on the title
- three chapter dividers (a huge extended numeral, one word, a brush stroke), each a slide whose `overtheme` drops the
  header and footer
- slide titles over a brush stroke and the slide number as a pale extended numeral, in a **header decorator**; author
  and talk in mono with the seal, in a **footer decorator**. The reveal backend draws slide titles only through a
  decorator, so a theme without one shows untitled slides
- display math (ideal MHD with GLM cleaning) rendered by the MathJax plugin
- two-column slides (`$columns`) mixing lists, tables, figures and code; figures mounted as prints
- Markdown tables whose bold numbers turn vermilion, and fenced code with a theme-level Pygments style
  (`theme.code.style: algol_nu`)
- the sumi theme in `reveal.custom_css`: washi ground with a fibre texture and an 80 px grid, Archivo / Inter /
  IBM Plex Mono, sumi ink, one vermilion seal. The brush stroke, the seal, the paper texture and the ensō are files in
  `images/` (`brush.svg` is drawn by the brush generator of the similitudo.eu site)

## Build

From this directory (the images are copied by `dirs_to_copy`, relative to the working directory):

```bash
matisse build -i talk.md -o out --backend reveal
xdg-open out/index.html    # Linux
open     out/index.html    # macOS
```

Press **S** for the speaker view.

## Notes on `custom_css`

The block is HTML-escaped when it is written into the page, so write it without child combinators (`>`) and without
ampersands (`&`): the Google Fonts imports are one per family for that reason.
