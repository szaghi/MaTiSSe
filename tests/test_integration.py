"""
Integration tests for MaTiSSe.py.

Each fixture directory under compare/ contains a test.md.  The test
parametrises over those directories, parses the source with the
Presentation API and asserts that the resulting HTML is well-formed.

Design choices
--------------
* All output is produced in-memory via the API — no CLI subprocess,
  no chdir, no per-Python-version baseline directories.
* The config fixture is session-scoped (conftest.py) so MatisseConfig
  is constructed exactly once for the whole run.
* Skipping is handled per-fixture via pytest.mark.skipif rather than
  inside __init__.
"""
import os

import pytest

from matisse.markdown_utils import __mdx_checklist__
from matisse.presentation import Presentation

_COMPARE_ROOT = os.path.join(os.path.dirname(__file__), 'compare')
COMPARE_DIRS = sorted(
    dirpath
    for dirpath, _dirnames, filenames in os.walk(_COMPARE_ROOT)
    if 'test.md' in filenames
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fixture_id(path):
    """Return a short test ID from a fixture directory path."""
    return os.path.basename(path)


def _should_skip(dirpath):
    """Return (skip, reason) for a given fixture directory."""
    if os.path.basename(dirpath) == 'checklists' and not __mdx_checklist__:
        return True, 'markdown_checklist not installed'
    return False, ''


# ---------------------------------------------------------------------------
# Parametrised integration test
# ---------------------------------------------------------------------------

@pytest.mark.parametrize('fixture_dir', COMPARE_DIRS, ids=_fixture_id)
def test_presentation_renders(fixture_dir, config):
    """Parse test.md and verify the output is a complete HTML document."""
    skip, reason = _should_skip(fixture_dir)
    if skip:
        pytest.skip(reason)

    source_path = os.path.join(fixture_dir, 'test.md')
    source = open(source_path).read()

    presentation = Presentation()
    presentation.parse(config=config, source=source)
    html = presentation.to_html(config=config)

    # Basic structural assertions — every rendered presentation must have these.
    assert '<!DOCTYPE html>' in html,        'Missing DOCTYPE declaration'
    assert '<html>' in html,                 'Missing <html> tag'
    assert '<body' in html,                  'Missing <body> tag'
    assert 'id="impress"' in html,           'Missing impress.js root element'
    assert 'class="step slide"' in html,     'No slides rendered'
    assert '</html>' in html,                'HTML document not closed'


@pytest.mark.parametrize('fixture_dir', COMPARE_DIRS, ids=_fixture_id)
def test_presentation_is_deterministic(fixture_dir, config):
    """Rendering the same source twice must produce identical HTML."""
    skip, reason = _should_skip(fixture_dir)
    if skip:
        pytest.skip(reason)

    source = open(os.path.join(fixture_dir, 'test.md')).read()

    p1 = Presentation()
    p1.parse(config=config, source=source)
    html1 = p1.to_html(config=config)

    p2 = Presentation()
    p2.parse(config=config, source=source)
    html2 = p2.to_html(config=config)

    assert html1 == html2, 'Rendering is not deterministic across two runs'
