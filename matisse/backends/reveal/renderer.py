#!/usr/bin/env python3
"""
matisse.backends.reveal.renderer — reveal.js HTML renderer.

Generates a self-contained reveal.js HTML presentation from a parsed
Presentation object.  All reveal.js assets are loaded from CDN (jsDelivr).
The document structure uses the standard reveal.js layout:

    <div class="reveal">
      <div class="slides">
        <section>...</section>
        ...
      </div>
    </div>

Each MaTiSSe slide (across all chapters/sections/subsections) is mapped
to a single ``<section>`` element.  The impress.js positioning system is
not used; slide ordering is linear.
"""

from __future__ import annotations

from yattag import Doc, indent

from ..base import AbstractBackend
from .theme import RevealTheme

# CDN base URLs
_REVEAL_CDN = "https://cdn.jsdelivr.net/npm/reveal.js@5"
_HLJS_CDN = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0"


class RevealBackend(AbstractBackend):
    """Renders a Presentation as a reveal.js HTML presentation."""

    def __init__(self, config):
        self.config = config

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_theme(self, presentation) -> RevealTheme:
        """Return a RevealTheme for this presentation.

        Reveal-specific YAML configuration (``reveal:`` key) is not yet
        parsed from the source in this initial implementation — the default
        theme is returned.  Full YAML integration is a future enhancement.
        """
        return RevealTheme()

    def _iter_slides(self, presentation):
        """Yield (chapter, section, subsection, slide, current) for every slide."""
        current = [0, 0, 0, 0]
        for chapter in presentation.chapters:
            current[0] += 1
            current[1] = 0
            current[2] = 0
            current[3] = 0
            for section in chapter.sections:
                current[1] += 1
                current[2] = 0
                current[3] = 0
                for subsection in section.subsections:
                    current[2] += 1
                    current[3] = 0
                    for slide in subsection.slides:
                        current[3] += 1
                        yield chapter, section, subsection, slide, list(current)

    def _put_head(self, doc, tag, text, presentation, theme):
        config = self.config
        highlight_style = theme.highlight_style or config.highlight_style
        with tag("head"):
            doc.stag("meta", charset="utf-8")
            doc.stag("meta", name="viewport", content="width=device-width, initial-scale=1.0")
            doc.stag("meta", author=" and ".join(presentation.metadata["authors"].value))
            with tag("title"):
                text(presentation.metadata["title"].value)
            # reveal.js CSS
            doc.stag("link", rel="stylesheet", href=f"{_REVEAL_CDN}/dist/reset.css")
            doc.stag("link", rel="stylesheet", href=f"{_REVEAL_CDN}/dist/reveal.css")
            doc.stag("link", rel="stylesheet", href=f"{_REVEAL_CDN}/dist/theme/{theme.theme}.css")
            # highlight.js CSS
            if config.highlight:
                doc.stag(
                    "link",
                    rel="stylesheet",
                    href=f"{_HLJS_CDN}/styles/{highlight_style}",
                )
            # optional custom CSS
            if theme.custom_css:
                with tag("style"):
                    doc.text(theme.custom_css)

    def _put_scripts(self, doc, tag, theme, config):
        with tag("script"):
            doc.attr(src=f"{_REVEAL_CDN}/dist/reveal.js")
        if config.highlight:
            with tag("script"):
                doc.attr(src=f"{_REVEAL_CDN}/plugin/highlight/highlight.js")
        # MathJax 3 for LaTeX equations
        with tag("script"):
            doc.text(
                """
        MathJax = {
          tex: {
            inlineMath: [['$', '$']],
            displayMath: [['$$', '$$']],
            processEscapes: true
          }
        };
        """
            )
        with tag("script"):
            doc.attr(src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js")
        # Reveal.initialize
        plugins = "RevealHighlight" if config.highlight else ""
        with tag("script"):
            doc.text(
                f"""
        Reveal.initialize({{
          hash: true,
          transition: '{theme.transition}',
          plugins: [{plugins}],
        }});
        """
            )

    # ------------------------------------------------------------------
    # AbstractBackend interface
    # ------------------------------------------------------------------

    def render(self, presentation) -> str:
        """Generate the complete reveal.js HTML for *presentation*."""
        theme = self._build_theme(presentation)
        config = self.config

        doc, tag, text = Doc().tagtext()
        doc.asis("<!DOCTYPE html>")
        with tag("html"):
            self._put_head(doc, tag, text, presentation, theme)
            with tag("body"):
                with tag("div", klass="reveal"):
                    with tag("div", klass="slides"):
                        for chap, sec, subsec, slide, current in self._iter_slides(presentation):
                            # Update metadata counters (needed for placeholder expansion)
                            presentation.metadata["chaptertitle"].update_value(value=chap.title)
                            presentation.metadata["chapternumber"].update_value(value=chap.number)
                            presentation.metadata["sectiontitle"].update_value(value=sec.title)
                            presentation.metadata["sectionnumber"].update_value(value=sec.number)
                            presentation.metadata["subsectiontitle"].update_value(value=subsec.title)
                            presentation.metadata["subsectionnumber"].update_value(value=subsec.number)
                            presentation.metadata["slidetitle"].update_value(value=slide.title)
                            presentation.metadata["slidenumber"].update_value(value=slide.number)
                            with tag("section", id=f"slide-{slide.number}"):
                                slide.to_html(
                                    doc=doc,
                                    parser=presentation.parser,
                                    metadata=presentation.metadata,
                                    theme=presentation.theme,
                                    current=current,
                                )
                self._put_scripts(doc, tag, theme, config)
        return indent(doc.getvalue())
