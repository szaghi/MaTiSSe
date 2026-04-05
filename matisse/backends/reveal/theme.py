#!/usr/bin/env python3
"""
matisse.backends.reveal.theme — reveal.js theme configuration.

RevealTheme is a lightweight alternative to ImpressTheme: instead of the
full YAML-driven CSS engine used for impress.js, reveal.js presentations
use one of reveal's own built-in themes (loaded from CDN) plus optional
per-slide transition overrides.

YAML block syntax (inside the presentation source):

    ---
    reveal:
      theme: moon          # reveal.js built-in theme name (default: black)
      transition: slide    # none | fade | slide | convex | concave | zoom
      code_style: monokai        # Pygments style (overrides CLI flag)
    ---
"""

from __future__ import annotations

from yaml import FullLoader, YAMLError, load_all

from ..base import AbstractTheme

_BUILTIN_THEMES = frozenset(
    {
        "black",
        "white",
        "league",
        "beige",
        "sky",
        "night",
        "moon",
        "serif",
        "simple",
        "solarized",
        "blood",
        "dracula",
    }
)

_VALID_TRANSITIONS = frozenset({"none", "fade", "slide", "convex", "concave", "zoom"})


class RevealTheme(AbstractTheme):
    """Reveal.js presentation theme.

    Attributes
    ----------
    theme : str
      Reveal.js built-in theme name (e.g. ``"black"``, ``"moon"``).
    transition : str
      Default slide transition (e.g. ``"slide"``, ``"fade"``).
    code_style : str
      Pygments style name (e.g. ``"monokai"``).  When set, overrides the
      value from ``MatisseConfig``.
    custom_css : str
      Raw CSS injected into the ``<head>`` as an inline ``<style>`` block.
    """

    _DEFAULTS = {
        "theme": "black",
        "transition": "slide",
        "code_style": "",
        "custom_css": "",
    }

    def __init__(self):
        self.theme = self._DEFAULTS["theme"]
        self.transition = self._DEFAULTS["transition"]
        self.code_style = self._DEFAULTS["code_style"]
        self.custom_css = self._DEFAULTS["custom_css"]

    # ------------------------------------------------------------------
    # AbstractTheme interface
    # ------------------------------------------------------------------

    def get(self, source: str, name: str = "theme", div_id: str = "") -> None:
        """Parse reveal theme settings from a YAML *source* string."""
        try:
            for data in load_all(source, Loader=FullLoader):
                if not data or "reveal" not in data:
                    continue
                cfg = data["reveal"]
                if not isinstance(cfg, dict):
                    continue
                theme = cfg.get("theme", self.theme)
                if theme in _BUILTIN_THEMES:
                    self.theme = theme
                else:
                    import sys

                    sys.stderr.write(
                        f"Warning: unknown reveal.js theme '{theme}'. "
                        f"Valid themes: {sorted(_BUILTIN_THEMES)}. "
                        f"Using '{self.theme}'.\n"
                    )
                transition = cfg.get("transition", self.transition)
                if transition in _VALID_TRANSITIONS:
                    self.transition = transition
                else:
                    import sys

                    sys.stderr.write(
                        f"Warning: unknown reveal.js transition '{transition}'. "
                        f"Valid transitions: {sorted(_VALID_TRANSITIONS)}. "
                        f"Using '{self.transition}'.\n"
                    )
                self.code_style = cfg.get("code_style", self.code_style)
                self.custom_css = cfg.get("custom_css", self.custom_css)
        except YAMLError:
            pass

    def to_css(self) -> str:
        """Return optional inline CSS (``custom_css`` field)."""
        return self.custom_css or ""
