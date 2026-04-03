"""
pytest configuration and shared fixtures for MaTiSSe.py tests.

The matisse package lives at the repo root (flat layout) and is importable
directly — no sys.path manipulation needed.
"""
import os

import pytest

from matisse.matisse_config import MatisseConfig

# ---------------------------------------------------------------------------
# Locate all integration-test fixture directories (those containing test.md).
# ---------------------------------------------------------------------------
_COMPARE_ROOT = os.path.join(os.path.dirname(__file__), 'compare')


def _find_compare_dirs():
    dirs = []
    for dirpath, _dirnames, filenames in os.walk(_COMPARE_ROOT):
        if 'test.md' in filenames:
            dirs.append(dirpath)
    return sorted(dirs)


COMPARE_DIRS = _find_compare_dirs()


# ---------------------------------------------------------------------------
# Session-scoped fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope='session')
def config():
    """A single, shared MatisseConfig instance for the whole test session."""
    return MatisseConfig()


@pytest.fixture(scope='session')
def compare_dirs():
    """Sorted list of fixture directories that contain a test.md file."""
    return COMPARE_DIRS
