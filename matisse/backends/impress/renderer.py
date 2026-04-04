#!/usr/bin/env python3
"""
matisse.backends.impress.renderer — impress.js HTML renderer.

Contains ImpressBackend, which takes a parsed Presentation object and
generates the complete impress.js HTML output.
"""

from __future__ import annotations

from yattag import Doc, indent

from ..base import AbstractBackend


class ImpressBackend(AbstractBackend):
    """Renders a Presentation as an impress.js HTML presentation."""

    def __init__(self, config):
        self.config = config

    # ------------------------------------------------------------------
    # Private helpers (moved from Presentation)
    # ------------------------------------------------------------------

    def _put_html_tag_head(self, doc, tag, text, presentation):
        config = self.config
        with tag("head"):
            doc.stag("meta", charset="utf-8")
            doc.stag("meta", author=" and ".join(presentation.metadata["authors"].value))
            with tag("title"):
                text(presentation.metadata["title"].value)
            doc.stag("meta", subtitle=presentation.metadata["subtitle"].value)
            doc.stag("link", rel="stylesheet", href="css/normalize.css")
            doc.stag("link", rel="stylesheet", href="css/matisse_defaults.css")
            doc.stag("link", rel="stylesheet", href="css/matisse_defaults_printing.css")
            if config.highlight:
                if config.offline:
                    doc.stag(
                        "link",
                        rel="stylesheet",
                        href=f"js/highlight/styles/{config.highlight_style}",
                    )
                else:
                    doc.stag(
                        "link",
                        rel="stylesheet",
                        href=f"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/{config.highlight_style}",
                    )
            doc.stag("link", rel="stylesheet", href="css/theme.css")
            for css in presentation.metadata["css_overtheme"].value:
                doc.stag("link", rel="stylesheet", href=css)
            for chapter in presentation.chapters:
                for section in chapter.sections:
                    for subsection in section.subsections:
                        for slide in subsection.slides:
                            if slide.overtheme.custom:
                                doc.stag(
                                    "link",
                                    rel="stylesheet",
                                    href=f"css/slide-{slide.number}-overtheme.css",
                                )

    def _put_html_tags_scripts(self, doc, tag):
        config = self.config
        with tag("script"):
            doc.attr(src="js/countDown.js")
        if config.offline:
            # --- offline mode: use local bundles ---
            with tag("script"):
                doc.attr(src="js/impress.js")
            if not config.pdf:
                with tag("script"):
                    doc.asis("impress().init();")
            with tag("script"):
                doc.attr(("type", "text/x-mathjax-config"))
                doc.text("""
          MathJax.Hub.Config({
            extensions: ["tex2jax.js"],
            jax: ["input/TeX", "output/HTML-CSS"],
            tex2jax: {
              inlineMath: [ ['$','$'] ],
              displayMath: [ ['$$','$$'] ],
              processEscapes: true
            },
            "HTML-CSS": { availableFonts: ["Neo-Euler"] }
          });
        """)
            with tag("script"):
                doc.attr(("type", "text/javascript"))
                doc.attr(src="js/MathJax/MathJax.js")
            if config.highlight:
                with tag("script"):
                    doc.attr(src="js/highlight/highlight.pack.js")
                with tag("script"):
                    doc.text("hljs.initHighlightingOnLoad();")
        else:
            # --- online mode (default): CDN — impress.js 2, MathJax 3, highlight.js 11 ---
            with tag("script"):
                doc.attr(src="https://cdn.jsdelivr.net/npm/impress.js@2/dist/impress.min.js")
            if not config.pdf:
                with tag("script"):
                    doc.asis("impress().init();")
            with tag("script"):
                doc.text("""
          MathJax = {
            tex: {
              inlineMath: [['$', '$']],
              displayMath: [['$$', '$$']],
              processEscapes: true
            }
          };
        """)
            with tag("script"):
                doc.attr(src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js")
            if config.highlight:
                with tag("script"):
                    doc.attr(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js")
                with tag("script"):
                    doc.text("hljs.highlightAll();")

    def _put_html_slide_decorators(
        self, tag, doc, decorator, presentation, position=None, overtheme=None, current=None
    ):
        if overtheme is not None and overtheme.custom:
            theme = overtheme
        else:
            theme = presentation.theme
        decorators = getattr(theme, "slide_" + decorator)
        for decor in sorted(decorators):
            insert = True
            # position check for sidebars
            if decorator == "sidebar" and position is not None:
                for css in decorators[decor]:
                    for key in css:
                        if "position" in key.lower():
                            pos = css[key]
                            break
                insert = pos.lower() == position.lower()
            # active check
            for css in decorators[decor]:
                for key in css:
                    if "active" in key.lower():
                        insert = insert and css[key].lower() == "yes"
            if insert:
                placeholders = theme.get_slide_decorators_metadata(decorator=decorator, name=decor)
                for metadata in presentation.metadata:
                    placeholders = presentation.metadata[metadata].parse(
                        parser=presentation.parser,
                        source=placeholders,
                        toc_depth=presentation.metadata["toc_depth"].value,
                        max_time=presentation.metadata["max_time"].value,
                        current=current,
                    )
                if decorator != "sidebar":
                    with doc.tag("div"):
                        doc.attr(style="clear: both;")
                with tag("div", klass="slide-" + decor):
                    doc.asis(placeholders)

    @staticmethod
    def _put_slide_attributes(doc, slide):
        """Attach impress.js data attributes to the current slide div."""
        doc.attr(("id", f"slide-{slide.number}"))
        doc.attr(("class", "step slide"))
        doc.attr(("data-x", str(slide.position["x"])))
        doc.attr(("data-y", str(slide.position["y"])))
        doc.attr(("data-z", str(slide.position["z"])))
        doc.attr(("data-scale", str(slide.position["scale"])))
        doc.attr(("data-rotate-x", str(slide.position["rotx"])))
        doc.attr(("data-rotate-y", str(slide.position["roty"])))
        doc.attr(("data-rotate-z", str(slide.position["rotz"])))

    # ------------------------------------------------------------------
    # AbstractBackend interface
    # ------------------------------------------------------------------

    def render(self, presentation) -> str:
        """Generate the complete impress.js HTML for *presentation*."""
        doc, tag, text = Doc().tagtext()
        doc.asis("<!DOCTYPE html>")
        with tag("html"):
            self._put_html_tag_head(doc, tag, text, presentation)
            with tag(
                "body",
                onload=f"resetCountdown({presentation.metadata['max_time'].value});",
            ):
                doc.attr(klass="impress-not-supported")
                with tag("div", id="impress"):
                    current = [0, 0, 0, 0]
                    for chapter in presentation.chapters:
                        current[0] += 1
                        current[1] = 0
                        current[2] = 0
                        current[3] = 0
                        presentation.metadata["chaptertitle"].update_value(value=chapter.title)
                        presentation.metadata["chapternumber"].update_value(value=chapter.number)
                        for section in chapter.sections:
                            current[1] += 1
                            current[2] = 0
                            current[3] = 0
                            presentation.metadata["sectiontitle"].update_value(value=section.title)
                            presentation.metadata["sectionnumber"].update_value(value=section.number)
                            for subsection in section.subsections:
                                current[2] += 1
                                current[3] = 0
                                presentation.metadata["subsectiontitle"].update_value(value=subsection.title)
                                presentation.metadata["subsectionnumber"].update_value(value=subsection.number)
                                for slide in subsection.slides:
                                    current[3] += 1
                                    presentation.metadata["slidetitle"].update_value(value=slide.title)
                                    presentation.metadata["slidenumber"].update_value(value=slide.number)
                                    with doc.tag("div"):
                                        chapter.put_html_attributes(doc=doc)
                                        section.put_html_attributes(doc=doc)
                                        subsection.put_html_attributes(doc=doc)
                                        self._put_slide_attributes(doc, slide)
                                        self._put_html_slide_decorators(
                                            tag=tag,
                                            doc=doc,
                                            decorator="header",
                                            presentation=presentation,
                                            current=current,
                                            overtheme=slide.overtheme,
                                        )
                                        self._put_html_slide_decorators(
                                            tag=tag,
                                            doc=doc,
                                            decorator="sidebar",
                                            presentation=presentation,
                                            position="L",
                                            current=current,
                                            overtheme=slide.overtheme,
                                        )
                                        slide.to_html(
                                            doc=doc,
                                            parser=presentation.parser,
                                            metadata=presentation.metadata,
                                            theme=presentation.theme,
                                            current=current,
                                        )
                                        self._put_html_slide_decorators(
                                            tag=tag,
                                            doc=doc,
                                            decorator="sidebar",
                                            presentation=presentation,
                                            position="R",
                                            current=current,
                                            overtheme=slide.overtheme,
                                        )
                                        self._put_html_slide_decorators(
                                            tag=tag,
                                            doc=doc,
                                            decorator="footer",
                                            presentation=presentation,
                                            current=current,
                                            overtheme=slide.overtheme,
                                        )
                self._put_html_tags_scripts(doc, tag)
        return indent(doc.getvalue())
