# Metadata

Presentation metadata is defined in the first YAML block of the source file.

## Supported keys

```yaml
---
title:        My Talk
subtitle:     A Subtitle
authors:      Stefano Zaghi
affiliations: CNR-INSEAN
emails:       stefano.zaghi@cnr.it
date:         April 2026
location:     Rome, Italy
conference:   My Conference 2026
session:      Invited Talk
logo:         logo.png
---
```

All keys are optional. Any key defined here becomes a `$key` placeholder available in theme `content` strings.

## Interpolation

```yaml
---
theme_slide_header_1:
  content: "$title — $authors"

theme_slide_footer_1:
  content: "$conference | $location | $date"
---
```

## Title page

The `$titlepage` token generates a slide populated entirely from metadata. Its layout is controlled by the built-in or custom title-page theme.
