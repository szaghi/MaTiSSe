---
theme:
  layout:
    slide:
      border: '2px solid black'
---

#### Quarto Spans — Text Classes

[Underlined text]{.underline} and [highlighted text]{.mark}.

[SMALL CAPS TITLE]{.smallcaps}

A sentence with [multiple]{.underline} [formatted]{.mark} [words]{.smallcaps}.

#### Quarto Spans — Attributes

A [custom span]{.custom-class} for user-defined CSS classes.

A [span with id]{#my-anchor} for anchoring.

#### Image Attributes

A paragraph with an inline image sized explicitly:

![logo](images/logo.png){width="120px"}

A second image with a CSS class attached:

![diagram](images/diagram.png){.figure-inline}
