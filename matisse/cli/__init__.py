"""
matisse.cli — Typer-based command-line interface for MaTiSSe.py.
"""

from . import _command  # noqa: F401 — registers @app.command() via side effect
from ._app import app


def main() -> None:
    """CLI entry point."""
    app()
