#!/usr/bin/env python3
"""
theme.py — backward-compatibility re-export shim.

The Theme implementation now lives in:
  matisse.backends.impress.theme.ImpressTheme

All existing code that imports ``from matisse.theme import Theme`` continues
to work unchanged.
"""

from .backends.impress.theme import ImpressTheme as Theme

__all__ = ["Theme"]
