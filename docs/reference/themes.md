# Theme YAML Reference

Themes are defined in YAML blocks embedded in the source file between `---` delimiters.

## Global slide properties

```yaml
---
theme_slide_global:
  width:  900px
  height: 600px
  data-transition-duration: 500
  background: white
  font-size: 16px
---
```

## Canvas

```yaml
---
theme_canvas:
  background: '#1a1a2e'
---
```

The canvas is the full-viewport background behind all slides.

## Headers and footers

Up to three independent header and footer bands are supported:

```yaml
---
theme_slide_header_1:
  active:     True
  height:     10%
  background: '#003366'
  color:      white
  content:    "$title"
  font-size:  18px

theme_slide_footer_1:
  active:     True
  height:     6%
  background: '#003366'
  color:      white
  content:    "$authors — $date"
  font-size:  12px
---
```

## Sidebars

```yaml
---
theme_slide_sidebar_1:
  active:     True
  width:      20%
  background: '#f0f0f0'
  position:   L
---
```

`position` is `L` (left) or `R` (right).

## Content area

```yaml
---
theme_slide_content:
  background: white
  color:      '#222'
  font-size:  18px
  padding:    20px
---
```

## Inheritance

Use `copy-from-theme` to inherit all properties from another theme block and override selectively:

```yaml
---
theme_slide_content:
  copy-from-theme: theme_slide_global
  font-size: 20px
---
```

## Per-slide overrides (overtheme)

A slide can override any theme property locally:

```markdown
#### My Slide

---
overtheme:
  theme_slide_content:
    background: '#ffe0e0'
---

Slide content here.
```

## Built-in themes

List available built-in themes:

```bash
MaTiSSe.py --print-themes
```

Apply a built-in theme in the metadata block:

```yaml
---
title: My Talk
theme: dark
---
```

### Theme gallery

**Antibes** — multi-level header bands with section and subsection titles

![Antibes theme screenshot](/images/antibes.png)

**Bergen** — left sidebar with TOC, wide header for slide title

![Bergen theme screenshot](/images/bergen.png)

**Berkeley** — sidebar with title/authors/TOC, coloured header

![Berkeley theme screenshot](/images/berkeley.png)

**Madrid** — bottom footer band with metadata

![Madrid theme screenshot](/images/madrid.png)

**Montpellier** — clean header with coloured accent bar

![Montpellier theme screenshot](/images/montpellier.png)

**Sapienza** — dark sidebar with light content area

![Sapienza theme screenshot](/images/sapienza.png)
