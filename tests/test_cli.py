"""
test_cli.py — Smoke tests for the Typer-based MaTiSSe.py CLI.
"""

import os
import tempfile

from typer.testing import CliRunner

from matisse.cli import app

runner = CliRunner()


# ---------------------------------------------------------------------------
# App-level callbacks
# ---------------------------------------------------------------------------


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "MaTiSSe.py" in result.output


def test_no_args_shows_help():
    result = runner.invoke(app, [])
    # Typer exits with 2 when no_args_is_help=True triggers the help display
    assert result.exit_code in (0, 2)
    assert "Usage" in result.output


# ---------------------------------------------------------------------------
# Info exits
# ---------------------------------------------------------------------------


def test_print_themes():
    result = runner.invoke(app, ["build", "--print-themes"])
    assert result.exit_code == 0
    assert "beamer-madrid" in result.output


def test_print_code_styles():
    result = runner.invoke(app, ["build", "--print-code-styles"])
    assert result.exit_code == 0
    assert "default" in result.output
    assert "monokai" in result.output


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


def test_missing_input_flag_exits_nonzero():
    result = runner.invoke(app, ["build"])
    assert result.exit_code == 1
    assert "required" in result.output.lower()


def test_nonexistent_input_file_exits_nonzero():
    result = runner.invoke(app, ["build", "--input", "nonexistent_file.md"])
    assert result.exit_code == 1
    assert "not found" in result.output.lower()


# ---------------------------------------------------------------------------
# Sample generation
# ---------------------------------------------------------------------------


def test_sample_generates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        sample_path = os.path.join(tmpdir, "sample.md")
        result = runner.invoke(app, ["build", "--sample", sample_path])
        assert result.exit_code == 0
        assert os.path.exists(sample_path)
        content = open(sample_path).read()
        assert "First Chapter" in content
