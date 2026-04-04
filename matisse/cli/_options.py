"""
_options.py — Shared Annotated option type aliases for MaTiSSe.py CLI.

Each alias captures flag names, help text, and autocompletion metadata.
Default values are declared at the call site so Typer can introspect them.
"""

from typing import Annotated

import typer

from ._completions import _complete_highlight_style, _complete_theme

# ---------------------------------------------------------------------------
# I/O group
# ---------------------------------------------------------------------------

InputOpt = Annotated[
    str | None,
    typer.Option("--input", "-i", help="Input Markdown source file to parse."),
]

OutputOpt = Annotated[
    str | None,
    typer.Option(
        "--output",
        "-o",
        help="Output directory for generated presentation files. Defaults to the input filename (without extension).",
    ),
]

# ---------------------------------------------------------------------------
# Sample group
# ---------------------------------------------------------------------------

SampleOpt = Annotated[
    str | None,
    typer.Option(
        "--sample",
        "-s",
        help="Write a sample presentation skeleton to FILE and exit.",
    ),
]

ThemeOpt = Annotated[
    str | None,
    typer.Option(
        "--theme",
        "-t",
        help="Apply a built-in theme to the presentation.",
        autocompletion=_complete_theme,
    ),
]

# ---------------------------------------------------------------------------
# Rendering group
# ---------------------------------------------------------------------------

BackendOpt = Annotated[
    str,
    typer.Option(
        "--backend",
        "-b",
        help='Rendering backend: "impress" (impress.js) or "reveal" (reveal.js). Default: impress.',
    ),
]

OfflineOpt = Annotated[
    bool,
    typer.Option(
        "--offline",
        help="Bundle impress.js, MathJax, and highlight.js locally instead of loading from CDN.",
    ),
]

PdfOpt = Annotated[
    bool,
    typer.Option(
        "--pdf",
        help="Disable impress.js animations — suitable for PDF printing.",
    ),
]

HighlightStyleOpt = Annotated[
    str,
    typer.Option(
        "--highlight-style",
        "-hs",
        help='highlight.js CSS style (default: github.css). Use "disable" to turn off highlighting.',
        metavar="STYLE",
        autocompletion=_complete_highlight_style,
    ),
]

# ---------------------------------------------------------------------------
# TOC group
# ---------------------------------------------------------------------------

TocAtChapOpt = Annotated[
    str | None,
    typer.Option(
        "--toc-at-chap-beginning",
        metavar="DEPTH",
        help="Insert a TOC slide at each chapter beginning. DEPTH controls how many levels to show.",
    ),
]

TocAtSecOpt = Annotated[
    str | None,
    typer.Option(
        "--toc-at-sec-beginning",
        metavar="DEPTH",
        help="Insert a TOC slide at each section beginning. DEPTH controls how many levels to show.",
    ),
]

TocAtSubsecOpt = Annotated[
    str | None,
    typer.Option(
        "--toc-at-subsec-beginning",
        metavar="DEPTH",
        help="Insert a TOC slide at each subsection beginning. DEPTH controls how many levels to show.",
    ),
]

# ---------------------------------------------------------------------------
# Info group
# ---------------------------------------------------------------------------

PrintThemesOpt = Annotated[
    bool,
    typer.Option(
        "--print-themes",
        help="List all available built-in themes and exit.",
    ),
]

PrintHighlightStylesOpt = Annotated[
    bool,
    typer.Option(
        "--print-highlight-styles",
        help="List all available highlight.js styles and exit.",
    ),
]

# ---------------------------------------------------------------------------
# Debug group
# ---------------------------------------------------------------------------

VerboseOpt = Annotated[
    bool,
    typer.Option("--verbose", help="Print verbose build messages."),
]

PrintParsedSourceOpt = Annotated[
    bool,
    typer.Option(
        "--print-parsed-source",
        help="Print the fully resolved source (after $include expansion) and continue.",
    ),
]
