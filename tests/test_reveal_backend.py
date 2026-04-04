"""
test_reveal_backend.py — Smoke tests for the reveal.js rendering backend.
"""

import os
import tempfile

from typer.testing import CliRunner

from matisse.cli import app
from matisse.matisse import __sample__, make_presentation
from matisse.matisse_config import MatisseConfig

runner = CliRunner()


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _build_sample_reveal(tmpdir):
    """Build the built-in sample with --backend reveal into *tmpdir*."""

    class _ns:
        backend = "reveal"
        verbose = False
        offline = False
        highlight_style = "github.css"
        theme = None
        toc_at_chap_beginning = None
        toc_at_sec_beginning = None
        toc_at_subsec_beginning = None
        pdf = False
        print_parsed_source = False

    config = MatisseConfig(cliargs=_ns())
    make_presentation(config=config, source=__sample__, output=tmpdir)
    return open(os.path.join(tmpdir, "index.html")).read()


# ---------------------------------------------------------------------------
# CLI smoke tests
# ---------------------------------------------------------------------------


def test_reveal_backend_sample():
    """build --sample ... --backend reveal must exit 0 and write the sample file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        sample_path = os.path.join(tmpdir, "sample.md")
        result = runner.invoke(app, ["build", "--sample", sample_path, "--backend", "reveal"])
        assert result.exit_code == 0
        assert os.path.exists(sample_path)


def test_reveal_print_themes():
    """--print-themes with --backend reveal should list reveal built-in themes."""
    result = runner.invoke(app, ["build", "--backend", "reveal", "--print-themes"])
    assert result.exit_code == 0
    assert "moon" in result.output
    assert "black" in result.output
    # Must NOT list impress built-in themes
    assert "beamer-madrid" not in result.output


# ---------------------------------------------------------------------------
# HTML output checks
# ---------------------------------------------------------------------------


def test_reveal_html_structure():
    """The reveal backend must produce the reveal.js div structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        html = _build_sample_reveal(tmpdir)
    assert '<div class="reveal">' in html
    assert '<div class="slides">' in html
    # Must NOT contain the impress.js container
    assert '<div id="impress">' not in html


def test_reveal_html_no_impress_scripts():
    """impress.js must not be loaded in reveal backend output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        html = _build_sample_reveal(tmpdir)
    assert "impress" not in html.lower() or "impress" not in html  # CDN URL check
    assert "impress.js" not in html


def test_reveal_html_cdn_scripts():
    """reveal.js and MathJax CDN links must be present."""
    with tempfile.TemporaryDirectory() as tmpdir:
        html = _build_sample_reveal(tmpdir)
    assert "reveal.js" in html
    assert "mathjax" in html.lower()


def test_reveal_html_slides_are_sections():
    """Each slide must be wrapped in a <section> element."""
    with tempfile.TemporaryDirectory() as tmpdir:
        html = _build_sample_reveal(tmpdir)
    assert "<section" in html


def test_reveal_speaker_notes():
    """$note environments must become <aside class=\"notes\"> in reveal output."""
    source = """
---
metadata:
  - title: "Notes test"
---
# Chapter
## Section
### Subsection
#### Slide
$note
$content{Speaker note text}
$endnote
"""
    with tempfile.TemporaryDirectory() as tmpdir:

        class _ns:
            backend = "reveal"
            verbose = False
            offline = False
            highlight_style = "github.css"
            theme = None
            toc_at_chap_beginning = None
            toc_at_sec_beginning = None
            toc_at_subsec_beginning = None
            pdf = False
            print_parsed_source = False

        config = MatisseConfig(cliargs=_ns())
        make_presentation(config=config, source=source, output=tmpdir)
        html = open(os.path.join(tmpdir, "index.html")).read()

    assert '<aside class="notes">' in html
    # Must NOT use the note-box markup
    assert 'class="note"' not in html


def test_impress_notes_unchanged():
    """$note environments must still render as note boxes for the impress backend."""
    source = """
---
metadata:
  - title: "Notes test impress"
---
# Chapter
## Section
### Subsection
#### Slide
$note
$content{Visible note box}
$endnote
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = MatisseConfig()
        make_presentation(config=config, source=source, output=tmpdir)
        html = open(os.path.join(tmpdir, "index.html")).read()

    assert 'class="note"' in html
    assert '<aside class="notes">' not in html


# ---------------------------------------------------------------------------
# Output tree
# ---------------------------------------------------------------------------


def test_reveal_output_tree_has_css_and_js_dirs():
    """make_output_tree for reveal must create css/ and js/ directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _build_sample_reveal(tmpdir)
        assert os.path.isdir(os.path.join(tmpdir, "css"))
        assert os.path.isdir(os.path.join(tmpdir, "js"))


def test_reveal_output_tree_no_impress_css():
    """Impress-specific CSS files must NOT be copied for the reveal backend."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _build_sample_reveal(tmpdir)
        assert not os.path.exists(os.path.join(tmpdir, "css/matisse_defaults.css"))
        assert not os.path.exists(os.path.join(tmpdir, "css/normalize.css"))
