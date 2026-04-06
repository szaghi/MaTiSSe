#!/usr/bin/env python3
"""
matisse.backends.reveal.renderer — reveal.js HTML renderer.

Generates a self-contained reveal.js HTML presentation from a parsed
Presentation object.  All reveal.js assets are loaded from CDN (jsDelivr).
The document structure uses the standard reveal.js layout:

    <div class="reveal">
      <div class="slides">
        <section>...</section>   <!-- linear layout -->
        ...
      </div>
    </div>

  or, with ``layout: vertical``:

    <div class="reveal">
      <div class="slides">
        <section>               <!-- chapter group (horizontal) -->
          <section>...</section>  <!-- slide (vertical within chapter) -->
        </section>
        ...
      </div>
    </div>

Each MaTiSSe slide is mapped to a ``<section>`` element.  Per-slide reveal
overrides (``overtheme.reveal`` YAML) are applied as ``data-*`` attributes.

Plugin support
--------------
Active plugins are declared in ``reveal.plugins`` and loaded from CDN.
When the ``math`` plugin is active, ``RevealMath.MathJax3`` replaces the
standalone MathJax ``<script>`` tags.
"""

from __future__ import annotations

from yattag import Doc

from ...diagram import GRAPHVIZ_CDN_SCRIPTS, MERMAID_CDN_SCRIPT, Diagram
from ..base import AbstractBackend, indent_html
from .theme import PLUGIN_CDN, PLUGIN_JS_NAME, RevealTheme

# CDN base URL (kept in sync with theme.py)
_REVEAL_CDN = "https://cdn.jsdelivr.net/npm/reveal.js@5"
_MATHJAX_CDN = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"

# ---------------------------------------------------------------------------
# JS formatting helpers
# ---------------------------------------------------------------------------


def _jsbool(v: bool) -> str:
    return "true" if v else "false"


def _jsval(v) -> str:
    """Format a Python value as a JS literal (no quoting for booleans/numbers)."""
    if isinstance(v, bool):
        return _jsbool(v)
    if isinstance(v, str):
        return f"'{v}'"
    return str(v)


# ---------------------------------------------------------------------------
# RevealBackend
# ---------------------------------------------------------------------------


class RevealBackend(AbstractBackend):
    """Renders a Presentation as a reveal.js HTML presentation."""

    def __init__(self, config):
        self.config = config

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_theme(self, presentation) -> RevealTheme:
        """Parse and return the RevealTheme from the presentation YAML blocks."""
        theme = RevealTheme()
        if presentation.yaml_source:
            theme.get(presentation.yaml_source)
        return theme

    def _slide_section_attrs(self, slide, theme: RevealTheme) -> dict:
        """Return the HTML attribute dict for a slide's ``<section>`` element.

        Merges the ``id`` with any reveal-specific per-slide overrides
        (``data-transition``, ``data-background-*``, ``data-auto-animate``).
        Phase 5: also merges heading-attribute background keys.
        When decorators are active the ``matisse-decorated`` class is added.
        """
        attrs: dict = {"id": f"slide-{slide.number}"}
        overrides = theme.parse_slide_overrides(slide.raw_overtheme_yaml)
        attrs.update(overrides)
        # Phase 5 — per-slide background via heading attributes
        attrs.update(slide.reveal_background_attrs())
        return attrs

    # ------------------------------------------------------------------
    # Decorator helpers
    # ------------------------------------------------------------------

    def _get_slide_decorators(self, slide, theme: RevealTheme):
        """Return the effective decorator list for *slide*.

        Per-slide ``overtheme.layout`` overrides replace matching decorators
        (by name) from the theme-level list.  Decorators absent from the
        override list are kept unchanged.
        """
        if not theme.has_decorators:
            return []
        overrides = theme.parse_slide_decorator_overrides(slide.raw_overtheme_yaml)
        if not overrides:
            return theme.decorators
        override_by_name = {s.name: s for s in overrides}
        return [override_by_name.get(s.name, s) for s in theme.decorators]

    def _build_placeholder_str(self, spec) -> str:
        """Build the metadata placeholder string for *spec*.

        Returns a string like ``$slidetitle[float:left;]$slidenumber[float:right;]``
        that the metadata parse chain will substitute with actual values.
        """
        return "".join(
            f"${meta_key}[{css_str}]" for meta_key, css_str in spec.metadata.items()
        )

    def _resolve_metadata(self, placeholder_str: str, presentation, current) -> str:
        """Substitute metadata placeholders in *placeholder_str*.

        Iterates over all metadata objects in *presentation* and calls their
        ``parse()`` method, exactly as the impress backend does for decorator
        content.
        """
        result = placeholder_str
        for meta_name in presentation.metadata:
            result = presentation.metadata[meta_name].parse(
                parser=presentation.parser,
                source=result,
                toc_depth=presentation.metadata["toc_depth"].value,
                max_time=presentation.metadata["max_time"].value,
                current=current,
            )
        return result

    def _put_decorator_div(self, doc, tag, spec, presentation, current) -> None:
        """Emit one ``<div class="slide-{spec.name}">`` with resolved metadata."""
        content = self._resolve_metadata(
            self._build_placeholder_str(spec), presentation, current
        )
        with tag("div", klass=f"slide-{spec.name}"):
            doc.asis(content)

    def _iter_slides(self, presentation):
        """Yield ``(chapter, section, subsection, slide, current)`` for every slide."""
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

    def _update_metadata(self, presentation, chap, sec, subsec, slide) -> None:
        """Update presentation metadata counters for the current slide."""
        md = presentation.metadata
        md["chaptertitle"].update_value(value=chap.title)
        md["chapternumber"].update_value(value=chap.number)
        md["sectiontitle"].update_value(value=sec.title)
        md["sectionnumber"].update_value(value=sec.number)
        md["subsectiontitle"].update_value(value=subsec.title)
        md["subsectionnumber"].update_value(value=subsec.number)
        md["slidetitle"].update_value(value=slide.title)
        md["slidenumber"].update_value(value=slide.number)

    def _render_slide(self, doc, tag, text, presentation, slide, chap, sec, subsec, current, theme):
        """Emit a single ``<section>`` for *slide*.

        When the theme defines active decorators the section gets the
        ``matisse-decorated`` class and is structured as:

        * headers (in decorator order)
        * slide-body wrapper (when sidebars are present)
          * left sidebars → slide-content div → right sidebars
        * footers (in decorator order)
        """
        attrs = self._slide_section_attrs(slide, theme)
        decorators = self._get_slide_decorators(slide, theme)
        active_decorators = [d for d in decorators if d.active]

        if active_decorators:
            attrs["klass"] = "matisse-decorated"

        with tag("section", **attrs):
            if not active_decorators:
                # Plain slide — no decorator scaffolding
                slide.to_html(
                    doc=doc,
                    parser=presentation.parser,
                    metadata=presentation.metadata,
                    theme=presentation.theme,
                    current=current,
                    backend="reveal",
                    label_registry=presentation.label_registry,
                )
                return

            # --- Headers ---
            for spec in active_decorators:
                if spec.kind == "header":
                    self._put_decorator_div(doc, tag, spec, presentation, current)

            # --- Body (sidebars + content) ---
            # Note: slide.to_html() always emits <div class="slide-content">...</div>
            # itself, so we must NOT add another wrapper around it.
            sidebars = [s for s in active_decorators if s.kind == "sidebar"]
            if sidebars:
                with tag("div", klass="slide-body"):
                    for spec in sidebars:
                        if spec.position == "L":
                            self._put_decorator_div(doc, tag, spec, presentation, current)
                    slide.to_html(
                        doc=doc,
                        parser=presentation.parser,
                        metadata=presentation.metadata,
                        theme=presentation.theme,
                        current=current,
                        backend="reveal",
                        label_registry=presentation.label_registry,
                    )
                    for spec in sidebars:
                        if spec.position != "L":
                            self._put_decorator_div(doc, tag, spec, presentation, current)
            else:
                slide.to_html(
                    doc=doc,
                    parser=presentation.parser,
                    metadata=presentation.metadata,
                    theme=presentation.theme,
                    current=current,
                    backend="reveal",
                    label_registry=presentation.label_registry,
                )

            # --- Footers ---
            for spec in active_decorators:
                if spec.kind == "footer":
                    self._put_decorator_div(doc, tag, spec, presentation, current)

    def _render_linear(self, doc, tag, text, presentation, theme) -> None:
        """Flat linear sequence of ``<section>`` elements (default layout)."""
        for chap, sec, subsec, slide, current in self._iter_slides(presentation):
            self._update_metadata(presentation, chap, sec, subsec, slide)
            self._render_slide(doc, tag, text, presentation, slide, chap, sec, subsec, current, theme)

    def _render_vertical(self, doc, tag, text, presentation, theme) -> None:
        """Vertical layout: chapters as outer ``<section>`` groups.

        Each chapter becomes a horizontal step; its slides stack vertically
        inside a wrapping ``<section>``.  This exposes reveal.js 2D navigation
        (left/right between chapters, up/down between slides within a chapter).
        """
        current = [0, 0, 0, 0]
        for chapter in presentation.chapters:
            current[0] += 1
            current[1] = 0
            current[2] = 0
            current[3] = 0
            slides_in_chapter = [
                (sec, subsec, slide)
                for sec in chapter.sections
                for subsec in sec.subsections
                for slide in subsec.slides
            ]
            if not slides_in_chapter:
                continue
            if len(slides_in_chapter) == 1:
                # Single slide in chapter — no need for a wrapping outer section
                sec, subsec, slide = slides_in_chapter[0]
                current[1] = current[2] = current[3] = 1
                self._update_metadata(presentation, chapter, sec, subsec, slide)
                self._render_slide(doc, tag, text, presentation, slide, chapter, sec, subsec, current, theme)
            else:
                with tag("section"):
                    for sec in chapter.sections:
                        current[1] += 1
                        current[2] = 0
                        current[3] = 0
                        for subsec in sec.subsections:
                            current[2] += 1
                            current[3] = 0
                            for slide in subsec.slides:
                                current[3] += 1
                                self._update_metadata(presentation, chapter, sec, subsec, slide)
                                self._render_slide(doc, tag, text, presentation, slide, chapter, sec, subsec, current, theme)

    def _put_head(self, doc, tag, text, presentation, theme: RevealTheme, config) -> None:
        with tag("head"):
            doc.stag("meta", charset="utf-8")
            doc.stag("meta", name="viewport", content="width=device-width, initial-scale=1.0")
            doc.stag("meta", author=" and ".join(presentation.metadata["authors"].value))
            with tag("title"):
                text(presentation.metadata["title"].value)
            # reveal.js core CSS
            doc.stag("link", rel="stylesheet", href=f"{_REVEAL_CDN}/dist/reset.css")
            doc.stag("link", rel="stylesheet", href=f"{_REVEAL_CDN}/dist/reveal.css")
            doc.stag("link", rel="stylesheet", href=f"{_REVEAL_CDN}/dist/theme/{theme.theme}.css")
            # Pygments CSS (always local — generated at build time)
            if config.code_highlight:
                doc.stag("link", rel="stylesheet", href="css/pygments.css")
            # decorator layout CSS (flex structure for header/footer/sidebar)
            if theme.has_decorators:
                with tag("style"):
                    doc.text(theme.to_decorator_css())
            # optional inline custom CSS
            if theme.custom_css:
                with tag("style"):
                    doc.text(theme.custom_css)

    def _put_scripts(self, doc, tag, theme: RevealTheme, config) -> None:
        # diagram CDN scripts (injected only when needed)
        if Diagram.has_mermaid:
            doc.asis(MERMAID_CDN_SCRIPT)
        if Diagram.has_graphviz:
            doc.asis(GRAPHVIZ_CDN_SCRIPTS)

        # reveal.js core
        with tag("script"):
            doc.attr(src=f"{_REVEAL_CDN}/dist/reveal.js")

        # plugin scripts (in order)
        for plugin in theme.plugins:
            with tag("script"):
                doc.attr(src=PLUGIN_CDN[plugin])

        # MathJax — standalone unless the math plugin handles it
        if not theme.use_math_plugin:
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
                doc.attr(src=_MATHJAX_CDN)

        # Reveal.initialize()
        with tag("script"):
            doc.text(self._reveal_init(theme))

    def _reveal_init(self, theme: RevealTheme) -> str:
        """Build the ``Reveal.initialize({...})`` JS call string."""
        parts: list[str] = []

        parts.append("hash: true")
        parts.append(f"transition: '{theme.transition}'")
        parts.append(f"transitionSpeed: '{theme.transition_speed}'")
        parts.append(f"controls: {_jsbool(theme.controls)}")
        parts.append(f"controlsLayout: '{theme.controls_layout}'")
        parts.append(f"progress: {_jsbool(theme.progress)}")

        # slideNumber: bool → JS bool literal, str → JS string literal
        if isinstance(theme.slide_number, bool):
            parts.append(f"slideNumber: {_jsbool(theme.slide_number)}")
        else:
            parts.append(f"slideNumber: '{theme.slide_number}'")

        parts.append(f"loop: {_jsbool(theme.loop)}")
        parts.append(f"center: {_jsbool(theme.center)}")
        parts.append(f"autoSlide: {theme.auto_slide}")
        parts.append(f"width: {_jsval(theme.width)}")
        parts.append(f"height: {_jsval(theme.height)}")
        parts.append(f"margin: {theme.margin}")
        parts.append(f"minScale: {theme.min_scale}")
        parts.append(f"maxScale: {theme.max_scale}")
        parts.append(f"backgroundTransition: '{theme.background_transition}'")
        parts.append(f"keyboard: {_jsbool(theme.keyboard)}")
        parts.append(f"touch: {_jsbool(theme.touch)}")

        # math plugin config (RevealMath.MathJax3)
        if theme.use_math_plugin:
            parts.append(
                "math: {\n"
                f"          mathjax: '{_MATHJAX_CDN}',\n"
                "          tex: {\n"
                "            inlineMath: [['$', '$']],\n"
                "            displayMath: [['$$', '$$']],\n"
                "            processEscapes: true\n"
                "          }\n"
                "        }"
            )

        plugin_names = [PLUGIN_JS_NAME[p] for p in theme.plugins]
        parts.append(f"plugins: [{', '.join(plugin_names)}]")

        body = ",\n          ".join(parts)
        return f"\n        Reveal.initialize({{\n          {body}\n        }});\n        "

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
            self._put_head(doc, tag, text, presentation, theme, config)
            with tag("body"):
                with tag("div", klass="reveal"):
                    with tag("div", klass="slides"):
                        if theme.layout == "vertical":
                            self._render_vertical(doc, tag, text, presentation, theme)
                        else:
                            self._render_linear(doc, tag, text, presentation, theme)
                self._put_scripts(doc, tag, theme, config)
        return indent_html(doc.getvalue())
