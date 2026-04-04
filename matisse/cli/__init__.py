"""
matisse.cli — Typer-based command-line interface for MaTiSSe.py.
"""

import os
import sys

from . import _command  # noqa: F401 — registers @app.command() via side effect
from ._app import app

# ---------------------------------------------------------------------------
# Completion detection — mirrors the mechanism used in FoBiS.py
# ---------------------------------------------------------------------------
# Typer/Click tab-completion is triggered by the shell setting an env var:
#
#   _{PROG.upper().replace("-", "_")}_COMPLETE=complete_<shell>
#
# For "MaTiSSe.py" the generated completion script uses "_MATISSE.PY_COMPLETE".
# We also detect the explicit --install-completion / --show-completion flags
# so that both installation and runtime completion always bypass any future
# CliRunner-based configuration layer (same guard pattern as FoBiS.py).
_completion_flags = frozenset({"--install-completion", "--show-completion"})

_prog_upper = os.path.basename(sys.argv[0]).upper().replace("-", "_")
_COMPLETION_MODE: bool = bool(
    os.environ.get(f"_{_prog_upper}_COMPLETE") or _completion_flags.intersection(sys.argv[1:])
)


def main() -> None:
    """CLI entry point.

    Completion requests — whether triggered by the shell env var or by
    --install-completion / --show-completion — are forwarded directly to
    app(), mirroring the guard pattern used in FoBiS.py.
    """
    if _COMPLETION_MODE:
        app()
        return
    app()
