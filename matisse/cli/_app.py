"""
_app.py — Typer application instance, version callback, and namespace factory.
"""

import argparse
from typing import Annotated

import typer

# ---------------------------------------------------------------------------
# Typer application
# ---------------------------------------------------------------------------

app = typer.Typer(
    name="MaTiSSe.py",
    help="Markdown To Impressive Scientific Slides",
    no_args_is_help=True,
    add_completion=True,
    rich_markup_mode=None,
)


# ---------------------------------------------------------------------------
# Version callback
# ---------------------------------------------------------------------------


def _version_callback(value: bool) -> None:
    if value:
        from .. import __appname__, __version__

        typer.echo(f"{__appname__} {__version__}")
        raise typer.Exit()


@app.callback()
def _app_callback(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="Show version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    ctx.ensure_object(dict)


# ---------------------------------------------------------------------------
# Namespace factory
# ---------------------------------------------------------------------------


def _ns(**kwargs) -> argparse.Namespace:
    """Build an argparse.Namespace — preserves the duck-type MatisseConfig.update() expects."""
    return argparse.Namespace(**kwargs)
