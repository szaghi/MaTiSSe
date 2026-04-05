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


def _complete_code_style(incomplete: str):
    """Return Pygments style names that start with *incomplete*."""
    try:
        from pygments.styles import get_all_styles

        return [s for s in sorted(get_all_styles()) if s.startswith(incomplete)]
    except ImportError:
        return []
