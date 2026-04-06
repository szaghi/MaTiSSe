#!/usr/bin/env python3
"""
matisse.backends.reveal.theme — reveal.js theme configuration.

RevealTheme exposes the full set of reveal.js 5 presentation options via
a ``reveal:`` YAML block, and slide decorators (headers, footers, sidebars)
via the same ``theme.layout`` YAML schema used by the impress backend.

Presentation-level YAML structure
----------------------------------
All reveal-specific options live under ``reveal:``.  Slide decorators live
under ``theme.layout``, exactly as for the impress backend::

    ---
    reveal:
      theme: moon
      transition: slide
      transition_speed: default
      controls: true
      controls_layout: bottom-right
      progress: true
      slide_number: "c/t"
      loop: false
      center: true
      auto_slide: 0
      width: 1280
      height: 720
      margin: 0.04
      min_scale: 0.2
      max_scale: 2.0
      background_transition: fade
      keyboard: true
      touch: true
      layout: linear          # linear | vertical
      plugins:
        - notes               # RevealNotes  (press S for speaker view)
        - zoom                # RevealZoom   (Alt+click to zoom)
        - search              # RevealSearch (Ctrl+Shift+F)
        - math                # RevealMath.MathJax3 (replaces standalone MathJax)
      code_style: monokai
      custom_css: |
        .reveal h1 { text-transform: none; }
    ---

    ---
    theme:
      layout:
        header-1:
          height: 8%
          background: "#1a1a2e"
          color: white
          metadata:
            slidetitle:
              float: left
              font-size: 0.9em
            slidenumber:
              float: right
        footer-1:
          height: 4%
          background: "#1a1a2e"
          metadata:
            conference:
              float: left
              font-size: 0.75em
        sidebar-1:
          position: L
          width: 20%
          metadata:
            toc:
              depth: "1"
    ---

Per-slide overrides (inside a slide's YAML overtheme block)
------------------------------------------------------------
Per-slide reveal options (``data-*`` attributes) and decorator overrides are
both supported under ``overtheme``::

    #### My Slide
    ---
    overtheme:
      reveal:
        background_color: "#1a1a2e"
        transition: zoom
      layout:
        header-1:
          height: 6%
          background: "#ff0000"
    ---

    Slide content here.
"""

from __future__ import annotations

import sys

from yaml import FullLoader, YAMLError, load_all

from ..base import AbstractTheme, DecoratorSpec, parse_layout_decorators

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_BUILTIN_THEMES = frozenset(
    {
        "black", "white", "league", "beige", "sky", "night", "moon",
        "serif", "simple", "solarized", "blood", "dracula",
    }
)

_VALID_TRANSITIONS = frozenset({"none", "fade", "slide", "convex", "concave", "zoom"})
_VALID_TRANSITION_SPEEDS = frozenset({"default", "fast", "slow"})
_VALID_CONTROLS_LAYOUTS = frozenset({"bottom-right", "edges"})
_VALID_BACKGROUND_TRANSITIONS = _VALID_TRANSITIONS
_VALID_PLUGINS = frozenset({"notes", "zoom", "search", "math"})
_VALID_LAYOUTS = frozenset({"linear", "vertical"})

# CDN base — kept in sync with renderer.py
_REVEAL_CDN = "https://cdn.jsdelivr.net/npm/reveal.js@5"

# CDN URL for each supported plugin JS file
PLUGIN_CDN: dict[str, str] = {
    "notes":  f"{_REVEAL_CDN}/plugin/notes/notes.js",
    "zoom":   f"{_REVEAL_CDN}/plugin/zoom/zoom.js",
    "search": f"{_REVEAL_CDN}/plugin/search/search.js",
    "math":   f"{_REVEAL_CDN}/plugin/math/math.js",
}

# JS global name used inside Reveal.initialize({ plugins: [...] })
PLUGIN_JS_NAME: dict[str, str] = {
    "notes":  "RevealNotes",
    "zoom":   "RevealZoom",
    "search": "RevealSearch",
    "math":   "RevealMath.MathJax3",
}

# ---------------------------------------------------------------------------
# RevealTheme
# ---------------------------------------------------------------------------


class RevealTheme(AbstractTheme):
    """Reveal.js presentation theme.

    Attributes
    ----------
    theme : str
        Reveal.js built-in theme name (e.g. ``"black"``, ``"moon"``).
    transition : str
        Default slide transition (e.g. ``"slide"``, ``"fade"``).
    transition_speed : str
        Transition speed: ``"default"``, ``"fast"``, or ``"slow"``.
    controls : bool
        Show navigation arrows.
    controls_layout : str
        Arrow placement: ``"bottom-right"`` or ``"edges"``.
    progress : bool
        Show progress bar along the bottom.
    slide_number : bool or str
        Slide number display: ``False``, ``True``, ``"c"``, ``"c/t"``,
        ``"h/v"``, or ``"h.v"``.
    loop : bool
        Loop the deck.
    center : bool
        Vertically centre slide content.
    auto_slide : int
        Auto-advance interval in milliseconds (0 = disabled).
    width : int or str
        Slide canvas width.
    height : int or str
        Slide canvas height.
    margin : float
        Viewport margin as a fraction of the canvas size.
    min_scale : float
        Minimum zoom scale.
    max_scale : float
        Maximum zoom scale.
    background_transition : str
        Transition applied to slide backgrounds.
    keyboard : bool
        Keyboard navigation.
    touch : bool
        Touch navigation.
    layout : str
        Slide layout mode: ``"linear"`` or ``"vertical"``.
    plugins : list[str]
        Active plugin names.
    code_style : str
        Pygments style name; overrides ``MatisseConfig.code_style`` when set.
    custom_css : str
        Raw CSS injected into ``<head>`` as an inline ``<style>`` block.
    decorators : list[DecoratorSpec]
        Parsed slide decorators (headers, footers, sidebars) from
        ``theme.layout``.  Empty when no decorators are defined.
    """

    _DEFAULTS: dict = {
        "theme":                 "black",
        "transition":            "slide",
        "transition_speed":      "default",
        "controls":              True,
        "controls_layout":       "bottom-right",
        "progress":              True,
        "slide_number":          False,
        "loop":                  False,
        "center":                True,
        "auto_slide":            0,
        "width":                 960,
        "height":                700,
        "margin":                0.04,
        "min_scale":             0.2,
        "max_scale":             2.0,
        "background_transition": "fade",
        "keyboard":              True,
        "touch":                 True,
        "layout":                "linear",
        "plugins":               (),
        "code_style":            "",
        "custom_css":            "",
    }

    def __init__(self) -> None:
        d = self._DEFAULTS
        self.theme:                  str        = d["theme"]
        self.transition:             str        = d["transition"]
        self.transition_speed:       str        = d["transition_speed"]
        self.controls:               bool       = d["controls"]
        self.controls_layout:        str        = d["controls_layout"]
        self.progress:               bool       = d["progress"]
        self.slide_number:           bool | str = d["slide_number"]
        self.loop:                   bool       = d["loop"]
        self.center:                 bool       = d["center"]
        self.auto_slide:             int        = d["auto_slide"]
        self.width:                  int | str  = d["width"]
        self.height:                 int | str  = d["height"]
        self.margin:                 float      = d["margin"]
        self.min_scale:              float      = d["min_scale"]
        self.max_scale:              float      = d["max_scale"]
        self.background_transition:  str        = d["background_transition"]
        self.keyboard:               bool       = d["keyboard"]
        self.touch:                  bool       = d["touch"]
        self.layout:                 str        = d["layout"]
        self.plugins:                list[str]  = list(d["plugins"])
        self.code_style:             str        = d["code_style"]
        self.custom_css:             str        = d["custom_css"]
        self.decorators:             list[DecoratorSpec] = []

    # ------------------------------------------------------------------
    # AbstractTheme interface
    # ------------------------------------------------------------------

    def get(self, source: str, name: str = "theme", div_id: str = "") -> None:
        """Parse reveal theme settings and decorator specs from YAML *source*.

        Looks for two distinct YAML keys:

        ``reveal:``
            Reveal.js initialisation options (transition, plugins, etc.).
            Present at top level for the presentation theme; nested inside
            ``overtheme:`` for per-slide overrides.

        ``theme.layout`` (or ``overtheme.layout`` for per-slide overrides)
            Slide decorator definitions (``header-*``, ``footer-*``,
            ``sidebar-*``) using the same schema as the impress backend.
        """
        try:
            for data in load_all(source, Loader=FullLoader):
                if not data or not isinstance(data, dict):
                    continue

                if name == "theme":
                    # Presentation-level: reveal: block
                    if "reveal" in data and isinstance(data["reveal"], dict):
                        self._parse_cfg(data["reveal"])
                    # Presentation-level: theme.layout decorators
                    if "theme" in data and isinstance(data["theme"], dict):
                        layout = data["theme"].get("layout") or {}
                        if layout:
                            self.decorators = parse_layout_decorators(layout)

                elif name == "overtheme":
                    # Per-slide: overtheme.reveal options
                    ot = data.get("overtheme")
                    if not isinstance(ot, dict):
                        continue
                    if "reveal" in ot and isinstance(ot["reveal"], dict):
                        self._parse_cfg(ot["reveal"])
                    # Per-slide: overtheme.layout decorator overrides
                    if "layout" in ot and isinstance(ot["layout"], dict):
                        override = parse_layout_decorators(ot["layout"])
                        if override:
                            self.decorators = override

        except YAMLError:
            pass

    def to_css(self) -> str:
        """Return optional inline CSS (``custom_css`` field)."""
        return self.custom_css or ""

    # ------------------------------------------------------------------
    # Decorator CSS generation
    # ------------------------------------------------------------------

    @property
    def has_decorators(self) -> bool:
        """True when at least one active decorator is defined."""
        return any(d.active for d in self.decorators)

    def to_decorator_css(self) -> str:
        """Generate flex-based CSS for the slide decorator layout.

        Returns an empty string when no decorators are defined.

        The generated CSS uses a flex-column layout on
        ``section.matisse-decorated`` so that headers and footers occupy
        fixed heights, the body (containing sidebars and content) fills the
        remaining space, and sidebars occupy fixed widths inside a flex-row
        wrapper.

        Layout model (no sidebars)::

            section.matisse-decorated  ← flex column
              .slide-header-1          ← flex-shrink: 0; height: <size>
              .slide-content           ← flex: 1  (fills remaining height)
              .slide-footer-1          ← flex-shrink: 0; height: <size>

        Layout model (with sidebars)::

            section.matisse-decorated  ← flex column
              .slide-header-1          ← flex-shrink: 0
              .slide-body              ← flex: 1; flex-direction: row
                .slide-sidebar-1       ← flex-shrink: 0; width: <size>
                .slide-content         ← flex: 1
                .slide-sidebar-2       ← flex-shrink: 0; width: <size>
              .slide-footer-1          ← flex-shrink: 0
        """
        if not self.has_decorators:
            return ""

        parts: list[str] = []

        # --- Base flex structure ---
        parts.append(
            ".reveal section.matisse-decorated {\n"
            "  display: flex !important;\n"
            "  flex-direction: column !important;\n"
            "  padding: 0 !important;\n"
            "  box-sizing: border-box !important;\n"
            "  text-align: left !important;\n"
            "}"
        )
        parts.append(
            ".reveal .slide-body {\n"
            "  display: flex;\n"
            "  flex-direction: row;\n"
            "  flex: 1 1 0%;\n"
            "  min-height: 0;\n"
            "  overflow: hidden;\n"
            "}"
        )
        parts.append(
            ".reveal section.matisse-decorated .slide-content {\n"
            "  flex: 1 1 0%;\n"
            "  min-width: 0;\n"
            "  min-height: 0;\n"
            "  overflow: auto;\n"
            "  box-sizing: border-box;\n"
            "}"
        )

        # --- Per-decorator rules ---
        for spec in self.decorators:
            if not spec.active:
                continue
            lines: list[str] = []
            if spec.kind in ("header", "footer"):
                lines.append(f"  flex-shrink: 0;")
                lines.append(f"  height: {spec.size};")
                lines.append(f"  width: 100%;")
                lines.append(f"  box-sizing: border-box;")
                lines.append(f"  overflow: hidden;")
            else:  # sidebar
                lines.append(f"  flex-shrink: 0;")
                lines.append(f"  width: {spec.size};")
                lines.append(f"  overflow: auto;")
                lines.append(f"  box-sizing: border-box;")
            for prop, val in spec.css.items():
                lines.append(f"  {prop}: {val};")
            body = "\n".join(lines)
            parts.append(f".reveal .slide-{spec.name} {{\n{body}\n}}")

        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Per-slide overrides
    # ------------------------------------------------------------------

    def parse_slide_overrides(self, yaml_src: str) -> dict:
        """Extract reveal-specific per-slide ``<section>`` data-* attributes.

        Reads ``overtheme.reveal`` from *yaml_src* and returns a dict of
        HTML ``data-*`` attribute key→value pairs.

        Supported YAML keys and their ``<section>`` attribute mapping:

        ========================  ==============================
        YAML key                  ``<section>`` attribute
        ========================  ==============================
        ``transition``            ``data-transition``
        ``background_color``      ``data-background-color``
        ``background_image``      ``data-background-image``
        ``background_size``       ``data-background-size``
        ``background_position``   ``data-background-position``
        ``background_video``      ``data-background-video``
        ``auto_animate``          ``data-auto-animate`` (bool)
        ========================  ==============================
        """
        if not yaml_src:
            return {}
        overrides: dict = {}
        try:
            for data in load_all(yaml_src, Loader=FullLoader):
                if not data or "overtheme" not in data:
                    continue
                cfg = data["overtheme"]
                if not isinstance(cfg, dict) or "reveal" not in cfg:
                    continue
                rv = cfg["reveal"]
                if not isinstance(rv, dict):
                    continue
                _STR_KEYS = {
                    "transition":          "data-transition",
                    "background_color":    "data-background-color",
                    "background_image":    "data-background-image",
                    "background_size":     "data-background-size",
                    "background_position": "data-background-position",
                    "background_video":    "data-background-video",
                }
                for yaml_key, attr in _STR_KEYS.items():
                    if yaml_key in rv:
                        overrides[attr] = str(rv[yaml_key])
                if rv.get("auto_animate"):
                    overrides["data-auto-animate"] = ""
                break
        except YAMLError:
            pass
        return overrides

    def parse_slide_decorator_overrides(self, yaml_src: str) -> list[DecoratorSpec]:
        """Extract per-slide decorator overrides from ``overtheme.layout``.

        Returns a list of :class:`DecoratorSpec` objects parsed from
        ``overtheme.layout.*`` in *yaml_src*.  Returns an empty list when no
        ``overtheme.layout`` block is present.

        The returned specs are meant to *replace* matching decorators in
        :attr:`decorators` by name when rendering the slide.
        """
        if not yaml_src:
            return []
        try:
            for data in load_all(yaml_src, Loader=FullLoader):
                if not data or "overtheme" not in data:
                    continue
                ot = data["overtheme"]
                if not isinstance(ot, dict) or "layout" not in ot:
                    continue
                layout = ot["layout"]
                if isinstance(layout, dict):
                    return parse_layout_decorators(layout)
        except YAMLError:
            pass
        return []

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def use_math_plugin(self) -> bool:
        """True when the ``math`` plugin is active (disables standalone MathJax)."""
        return "math" in self.plugins

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _parse_cfg(self, cfg: dict) -> None:
        """Populate attributes from a validated ``reveal:`` YAML mapping."""
        # theme
        theme = cfg.get("theme", self.theme)
        if theme in _BUILTIN_THEMES:
            self.theme = theme
        else:
            sys.stderr.write(
                f"Warning: unknown reveal.js theme '{theme}'. "
                f"Valid themes: {sorted(_BUILTIN_THEMES)}. "
                f"Using '{self.theme}'.\n"
            )

        # transitions
        self.transition = self._validated(
            cfg, "transition", self.transition, _VALID_TRANSITIONS, "transition"
        )
        self.transition_speed = self._validated(
            cfg, "transition_speed", self.transition_speed, _VALID_TRANSITION_SPEEDS, "transition_speed"
        )
        self.background_transition = self._validated(
            cfg, "background_transition", self.background_transition,
            _VALID_BACKGROUND_TRANSITIONS, "background_transition"
        )
        self.layout = self._validated(
            cfg, "layout", self.layout, _VALID_LAYOUTS, "layout"
        )

        # controls
        self.controls = bool(cfg.get("controls", self.controls))
        controls_layout = cfg.get("controls_layout", self.controls_layout)
        if controls_layout in _VALID_CONTROLS_LAYOUTS:
            self.controls_layout = controls_layout
        else:
            sys.stderr.write(
                f"Warning: unknown controls_layout '{controls_layout}'. "
                f"Using '{self.controls_layout}'.\n"
            )

        # booleans
        self.progress = bool(cfg.get("progress",  self.progress))
        self.loop     = bool(cfg.get("loop",      self.loop))
        self.center   = bool(cfg.get("center",    self.center))
        self.keyboard = bool(cfg.get("keyboard",  self.keyboard))
        self.touch    = bool(cfg.get("touch",     self.touch))

        # slide_number: accept bool or str
        sn = cfg.get("slide_number", self.slide_number)
        if isinstance(sn, bool):
            self.slide_number = sn
        else:
            sn_str = str(sn)
            if sn_str in {"false", "False"}:
                self.slide_number = False
            elif sn_str in {"true", "True"}:
                self.slide_number = True
            else:
                self.slide_number = sn_str

        # sizing / timing
        self.auto_slide = int(cfg.get("auto_slide", self.auto_slide))
        self.width      = cfg.get("width",     self.width)
        self.height     = cfg.get("height",    self.height)
        self.margin     = float(cfg.get("margin",    self.margin))
        self.min_scale  = float(cfg.get("min_scale", self.min_scale))
        self.max_scale  = float(cfg.get("max_scale", self.max_scale))

        # plugins
        plugins_raw = cfg.get("plugins", None)
        if plugins_raw is not None:
            self.plugins = []
            for p in plugins_raw:
                if p in _VALID_PLUGINS:
                    self.plugins.append(p)
                else:
                    sys.stderr.write(
                        f"Warning: unknown reveal plugin '{p}'. "
                        f"Valid plugins: {sorted(_VALID_PLUGINS)}. Skipping.\n"
                    )

        # misc
        self.code_style = cfg.get("code_style", self.code_style)
        self.custom_css = cfg.get("custom_css", self.custom_css)

    @staticmethod
    def _validated(cfg: dict, key: str, current, valid_set: frozenset, label: str) -> str:
        val = cfg.get(key, current)
        if val in valid_set:
            return val
        sys.stderr.write(
            f"Warning: unknown reveal.js {label} '{val}'. "
            f"Valid values: {sorted(valid_set)}. "
            f"Using '{current}'.\n"
        )
        return current
