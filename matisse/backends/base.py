"""
matisse.backends.base — Abstract base classes for MaTiSSe rendering backends.

Every backend must provide:
  - An AbstractTheme subclass that parses the user's YAML theme source and
    can emit the CSS consumed by its renderer.
  - An AbstractBackend subclass that accepts a parsed Presentation document
    model and returns the complete HTML string for index.html.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..presentation import Presentation


class AbstractTheme(ABC):
    """Interface for backend-specific theme implementations.

    A theme is responsible for:
      1. Parsing the YAML ``theme:`` blocks from the presentation source.
      2. Emitting CSS (or whatever styling artefact the backend consumes).
    """

    @abstractmethod
    def get(self, source: str, name: str = "theme", div_id: str = "") -> None:
        """Parse *source* and populate internal theme state.

        Parameters
        ----------
        source:
            Raw YAML source containing one or more ``theme:`` blocks.
        name:
            YAML key to look for (default ``"theme"``; overthemes use
            ``"overtheme"``).
        div_id:
            Optional HTML id used to scope generated CSS selectors.
        """

    @abstractmethod
    def to_css(self) -> str:
        """Return the complete CSS string for this theme."""


class AbstractBackend(ABC):
    """Interface for backend renderers.

    A backend is responsible for turning the parsed document model
    (``Presentation``) into a complete, self-contained HTML string.
    """

    @abstractmethod
    def render(self, presentation: "Presentation") -> str:
        """Render *presentation* and return the full ``index.html`` content.

        Parameters
        ----------
        presentation:
            The fully parsed ``Presentation`` document model.

        Returns
        -------
        str
            Complete HTML string ready to be written to ``index.html``.
        """
