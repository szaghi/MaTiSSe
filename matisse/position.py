#!/usr/bin/env python3
"""
position.py — backward-compatibility re-export shim.

The Position implementation now lives in:
  matisse.backends.impress.position.Position

All existing code that imports ``from matisse.position import Position``
continues to work unchanged.
"""

from .backends.impress.position import Position

__all__ = ["Position"]
