"""
_completions.py — Typer autocompletion callbacks for MaTiSSe.py CLI.

Pure filesystem reads with no imports from the rest of the package so that
tab-completion stays fast regardless of package import cost.
"""

import os


def _complete_theme(incomplete: str):
    """Return built-in theme names that start with *incomplete*."""
    themes_dir = os.path.join(os.path.dirname(__file__), "../utils/builtin_themes")
    try:
        return [t for t in sorted(os.listdir(themes_dir)) if t.startswith(incomplete)]
    except FileNotFoundError:
        return []


def _complete_highlight_style(incomplete: str):
    """Return highlight.js CSS style names that start with *incomplete*."""
    styles_dir = os.path.join(os.path.dirname(__file__), "../utils/js/highlight/styles")
    try:
        return [s for s in sorted(os.listdir(styles_dir)) if s.endswith(".css") and s.startswith(incomplete)]
    except FileNotFoundError:
        return []
