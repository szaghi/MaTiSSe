#!/usr/bin/env python3
"""
matisse.backends.impress.renderer — impress.js HTML renderer.

Contains ImpressBackend, which takes a parsed Presentation object and
generates the complete impress.js HTML output.
"""

from __future__ import annotations

from yattag import Doc

from ...diagram import GRAPHVIZ_CDN_SCRIPTS, MERMAID_CDN_SCRIPT, Diagram
from ..base import AbstractBackend, indent_html


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
            if config.code_highlight:
                doc.stag("link", rel="stylesheet", href="css/pygments.css")
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
        else:
            # --- online mode (default): CDN — impress.js 2, MathJax 3 ---
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
    def _put_impress_root_attributes(doc, theme):
        """Emit canvas-level data attributes on the root ``<div id="impress">``."""
        transition = theme.get_slide_transition()
        doc.attr(("data-width", str(transition["width"])))
        doc.attr(("data-height", str(transition["height"])))
        if theme.max_scale is not None:
            doc.attr(("data-max-scale", str(theme.max_scale)))
        if theme.min_scale is not None:
            doc.attr(("data-min-scale", str(theme.min_scale)))
        if theme.canvas_autoplay is not None:
            doc.attr(("data-autoplay", str(theme.canvas_autoplay)))
        if theme.autoplay_repeat is not None:
            doc.attr(("data-autoplay-repeat", "true" if theme.autoplay_repeat else "false"))
        if theme.media_autoplay:
            doc.attr(("data-media-autoplay", "true"))
        if theme.media_autostop:
            doc.attr(("data-media-autostop", "true"))
        if theme.media_autopause:
            doc.attr(("data-media-autopause", "true"))
        if theme.console_autolaunch:
            doc.attr(("data-console-autolaunch", "true"))
        if theme.console_css:
            doc.attr(("data-console-css", theme.console_css))
        if theme.console_css_iframe:
            doc.attr(("data-console-css-iframe", theme.console_css_iframe))

    @staticmethod
    def _put_ui_elements(doc, tag, theme):
        """Emit optional impress.js UI plugin HTML elements."""
        if theme.show_progress_bar:
            with tag("div", klass="impress-progressbar"):
                doc.stag("div")
        if theme.show_progress_counter:
            with tag("div", klass="impress-progress"):
                pass
        if theme.show_help_popup:
            with tag("div", id="impress-help"):
                pass
        if theme.show_navigation_toolbar:
            with tag("div", id="impress-toolbar"):
                pass

    @staticmethod
    def _put_slide_attributes(doc, slide):
        """Attach impress.js data attributes to the current slide div."""
        overtheme = slide.overtheme

        # Build CSS class string (base + optional navigation-control classes)
        extra_classes = ""
        if overtheme.custom:
            if overtheme.skip:
                extra_classes += " skip"
            if overtheme.stop:
                extra_classes += " stop"

        doc.attr(("id", f"slide-{slide.number}"))
        doc.attr(("class", f"step slide{extra_classes}"))

        # Phase 5 — per-slide background via heading attributes
        bg_style = slide.background_style()
        if bg_style:
            doc.attr(style=bg_style)

        # Positioning: relative takes precedence over absolute when any
        # rel-x/y/z attribute is set in the overtheme.
        has_relative = overtheme.custom and any(
            v is not None for v in (overtheme.rel_x, overtheme.rel_y, overtheme.rel_z)
        )
        if has_relative:
            if overtheme.rel_x is not None:
                doc.attr(("data-rel-x", str(overtheme.rel_x)))
            if overtheme.rel_y is not None:
                doc.attr(("data-rel-y", str(overtheme.rel_y)))
            if overtheme.rel_z is not None:
                doc.attr(("data-rel-z", str(overtheme.rel_z)))
            if overtheme.rel_to:
                doc.attr(("data-rel-to", overtheme.rel_to))
            if overtheme.rel_position:
                doc.attr(("data-rel-position", overtheme.rel_position))
            if overtheme.rel_reset is not None:
                doc.attr(("data-rel-reset", "true" if overtheme.rel_reset else "false"))
            if overtheme.rel_rotate_x is not None:
                doc.attr(("data-rel-rotate-x", str(overtheme.rel_rotate_x)))
            if overtheme.rel_rotate_y is not None:
                doc.attr(("data-rel-rotate-y", str(overtheme.rel_rotate_y)))
            if overtheme.rel_rotate_z is not None:
                doc.attr(("data-rel-rotate-z", str(overtheme.rel_rotate_z)))
            if overtheme.rel_rotate_order:
                doc.attr(("data-rel-rotate-order", overtheme.rel_rotate_order))
        else:
            doc.attr(("data-x", str(slide.position["x"])))
            doc.attr(("data-y", str(slide.position["y"])))
            doc.attr(("data-z", str(slide.position["z"])))
            doc.attr(("data-scale", str(slide.position["scale"])))
            doc.attr(("data-rotate-x", str(slide.position["rotx"])))
            doc.attr(("data-rotate-y", str(slide.position["roty"])))
            doc.attr(("data-rotate-z", str(slide.position["rotz"])))

        # Rotation order (#61)
        if overtheme.custom and overtheme.rotate_order:
            doc.attr(("data-rotate-order", overtheme.rotate_order))

        # Per-slide transition duration (#52)
        if overtheme.custom and overtheme.transition_duration is not None:
            doc.attr(("data-transition-duration", str(overtheme.transition_duration)))

        # Per-slide autoplay (#56)
        if overtheme.custom and overtheme.slide_autoplay is not None:
            doc.attr(("data-autoplay", str(overtheme.slide_autoplay)))

        # Per-slide media controls (#60)
        if overtheme.custom:
            if overtheme.slide_media_autoplay is not None:
                doc.attr(("data-media-autoplay", "true" if overtheme.slide_media_autoplay else "false"))
            if overtheme.slide_media_autostop is not None:
                doc.attr(("data-media-autostop", "true" if overtheme.slide_media_autostop else "false"))
            if overtheme.slide_media_autopause is not None:
                doc.attr(("data-media-autopause", "true" if overtheme.slide_media_autopause else "false"))

        # Goto plugin (#58)
        if overtheme.custom:
            if overtheme.goto:
                doc.attr(("data-goto", overtheme.goto))
            if overtheme.goto_next:
                doc.attr(("data-goto-next", overtheme.goto_next))
            if overtheme.goto_prev:
                doc.attr(("data-goto-prev", overtheme.goto_prev))
            if overtheme.goto_key_list:
                doc.attr(("data-goto-key-list", overtheme.goto_key_list))
            if overtheme.goto_next_list:
                doc.attr(("data-goto-next-list", overtheme.goto_next_list))

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
                    self._put_impress_root_attributes(doc, presentation.theme)
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
                                            label_registry=presentation.label_registry,
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
                self._put_ui_elements(doc, tag, presentation.theme)
                # Phase 2 — diagram CDN scripts (injected only when needed)
                if Diagram.has_mermaid:
                    doc.asis(MERMAID_CDN_SCRIPT)
                if Diagram.has_graphviz:
                    doc.asis(GRAPHVIZ_CDN_SCRIPTS)
                self._put_html_tags_scripts(doc, tag)
        return indent_html(doc.getvalue())
