"""
_command.py — MaTiSSe.py build command.

Registers the single @app.command() that replaces the argparse if/elif
dispatch in the original matisse.py::main().
"""

import os

import typer

from ..matisse import __sample__, make_presentation
from ..matisse_config import MatisseConfig
from ._app import _ns, app
from ._options import (
    BackendOpt,
    CodeStyleOpt,
    InputOpt,
    OfflineOpt,
    OutputOpt,
    PdfOpt,
    PrintCodeStylesOpt,
    PrintParsedSourceOpt,
    PrintThemesOpt,
    SampleOpt,
    ThemeOpt,
    TocAtChapOpt,
    TocAtSecOpt,
    TocAtSubsecOpt,
    VerboseOpt,
)


@app.command()
def build(
    # I/O group
    input: InputOpt = None,
    output: OutputOpt = None,
    # Sample group
    sample: SampleOpt = None,
    theme: ThemeOpt = None,
    # Rendering group
    backend: BackendOpt = "impress",
    offline: OfflineOpt = False,
    pdf: PdfOpt = False,
    code_style: CodeStyleOpt = "default",
    # TOC group
    toc_at_chap_beginning: TocAtChapOpt = None,
    toc_at_sec_beginning: TocAtSecOpt = None,
    toc_at_subsec_beginning: TocAtSubsecOpt = None,
    # Info group
    print_themes: PrintThemesOpt = False,
    print_code_styles: PrintCodeStylesOpt = False,
    # Debug group
    verbose: VerboseOpt = False,
    print_parsed_source: PrintParsedSourceOpt = False,
) -> None:
    """Build an HTML presentation from a Markdown source file."""

    # Build a Namespace the existing MatisseConfig.update() understands unchanged.
    cliargs = _ns(
        backend=backend,
        verbose=verbose,
        offline=offline,
        code_style=code_style,
        theme=theme,
        toc_at_chap_beginning=toc_at_chap_beginning,
        toc_at_sec_beginning=toc_at_sec_beginning,
        toc_at_subsec_beginning=toc_at_subsec_beginning,
        pdf=pdf,
        print_parsed_source=print_parsed_source,
    )
    config = MatisseConfig(cliargs=cliargs)

    # --- Info exits ---
    if print_themes:
        typer.echo(config.str_themes())
        raise typer.Exit()

    if print_code_styles:
        typer.echo(config.str_code_styles())
        raise typer.Exit()

    # --- Sample generation ---
    if sample:
        out = os.path.normpath(os.path.splitext(os.path.basename(sample))[0])
        source = make_presentation(config=config, source=__sample__, output=out)
        with open(sample, "w") as f:
            f.write(source)
        return

    # --- Normal build ---
    if not input:
        typer.echo("Error: --input is required for building a presentation.", err=True)
        raise typer.Exit(1)

    if not os.path.exists(input):
        typer.echo(f'Error: input file "{input}" not found.', err=True)
        raise typer.Exit(1)

    with open(input) as f:
        source = f.read()

    out = os.path.normpath(output or os.path.splitext(os.path.basename(input))[0])
    make_presentation(config=config, source=source, output=out)
