# reveal-advanced example

Demonstrates the full reveal.js theme engine: presentation-level options,
plugin activation, per-slide backgrounds and transitions, and vertical layout.

## Build

```bash
# from the repo root
matisse build -i examples/reveal-advanced/advanced.md \
              -o /tmp/reveal-advanced/ \
              --backend reveal
# then open /tmp/reveal-advanced/index.html in a browser
```

## What it shows

| Feature | YAML key |
|---|---|
| Built-in theme | `reveal.theme` |
| Slide transition + speed | `reveal.transition`, `reveal.transition_speed` |
| Navigation controls | `reveal.controls`, `reveal.controls_layout` |
| Progress bar | `reveal.progress` |
| Slide numbers | `reveal.slide_number` |
| Canvas size | `reveal.width`, `reveal.height` |
| Margin | `reveal.margin` |
| Zoom limits | `reveal.min_scale`, `reveal.max_scale` |
| Auto-advance | `reveal.auto_slide` |
| Speaker notes plugin | `reveal.plugins: [notes]` |
| Math plugin (MathJax3) | `reveal.plugins: [math]` |
| Zoom plugin | `reveal.plugins: [zoom]` |
| Custom CSS | `reveal.custom_css` |
| Per-slide background colour | `overtheme.reveal.background_color` |
| Per-slide background image | `overtheme.reveal.background_image` |
| Per-slide transition | `overtheme.reveal.transition` |
| Auto-animate between slides | `overtheme.reveal.auto_animate` |
