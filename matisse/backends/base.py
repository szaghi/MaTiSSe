"""
matisse.backends.base — Abstract base classes and shared utilities for MaTiSSe
rendering backends.

Every backend must provide:
  - An AbstractTheme subclass that parses the user's YAML theme source and
    can emit the CSS consumed by its renderer.
  - An AbstractBackend subclass that accepts a parsed Presentation document
    model and returns the complete HTML string for index.html.

Shared utilities
----------------
DecoratorSpec
    Dataclass representing one parsed slide decorator (header, footer, or
    sidebar) in a backend-agnostic form.

parse_layout_decorators(layout)
    Free function that converts a ``theme.layout`` dict (already parsed from
    YAML) into a sorted list of ``DecoratorSpec`` objects.  Both the impress
    and reveal backends call this function so that the same YAML schema drives
    both rendering pipelines.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from yattag import indent as _yattag_indent

# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------


def indent_html(html: str) -> str:
    """Indent HTML while preserving whitespace inside ``<pre>`` blocks.

    ``yattag.indent()`` reformats every element unconditionally, inserting
    newlines between ``<span>`` tokens inside ``<pre><code>`` blocks.  Since
    ``<pre>`` preserves whitespace, those injected newlines render as one
    token per line in the browser.

    This wrapper extracts all ``<pre>…</pre>`` subtrees before indenting and
    restores them verbatim afterwards.
    """
    pre_blocks: list[str] = []

    def _save(m: re.Match) -> str:
        pre_blocks.append(m.group(0))
        return f"\x00PRE{len(pre_blocks) - 1}\x00"

    protected = re.sub(r"<pre>.*?</pre>", _save, html, flags=re.DOTALL)
    indented = _yattag_indent(protected)
    for i, block in enumerate(pre_blocks):
        indented = indented.replace(f"\x00PRE{i}\x00", block)
    return indented


# ---------------------------------------------------------------------------
# Shared decorator model
# ---------------------------------------------------------------------------


@dataclass
class DecoratorSpec:
    """Backend-agnostic representation of one slide decorator.

    A decorator is a ``header-N``, ``footer-N``, or ``sidebar-N`` element
    defined in the ``theme.layout`` YAML block.  Both the impress and reveal
    backends parse decorators into ``DecoratorSpec`` objects via
    :func:`parse_layout_decorators` and then generate backend-specific HTML
    and CSS from them.

    Attributes
    ----------
    name : str
        Full decorator key, e.g. ``"header-1"``, ``"sidebar-2"``.
    kind : str
        One of ``"header"``, ``"footer"``, or ``"sidebar"``.
    size : str
        Primary dimension as a CSS value string.  For headers and footers
        this is the *height*; for sidebars it is the *width*.  Defaults to
        ``"10%"`` for headers/footers and ``"10%"`` for sidebars when the
        key is absent from the YAML.
    position : str
        For sidebars: ``"L"`` (left) or ``"R"`` (right).  Empty string for
        headers and footers.
    css : dict[str, str]
        Additional CSS properties (everything in the decorator YAML block
        except ``height``, ``width``, ``position``, ``active``, and
        ``metadata``).  Keys are CSS property names, values are CSS value
        strings.
    metadata : dict[str, str]
        Mapping from metadata placeholder name (e.g. ``"slidetitle"``) to
        an inline CSS string (e.g. ``"float:left;font-size:120%;"``).  Used
        to inject dynamic metadata values into the decorator HTML.
    active : bool
        Whether this decorator should be rendered.  Defaults to ``True``.
        Corresponds to the ``active: yes/no`` YAML key.
    """

    name: str
    kind: str
    size: str
    position: str
    css: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    active: bool = True


# Keys inside a decorator YAML block that are handled structurally rather
# than treated as raw CSS properties.
_STRUCTURAL_KEYS = frozenset({"height", "width", "position", "active", "metadata"})


def parse_layout_decorators(layout: dict) -> list[DecoratorSpec]:
    """Convert a ``theme.layout`` dict into a list of :class:`DecoratorSpec`.

    Iterates over every key in *layout* that matches ``header-*``,
    ``footer-*``, or ``sidebar-*``, parses the nested YAML into a
    :class:`DecoratorSpec`, and returns the results sorted by name so that
    ``header-1`` always precedes ``header-2``, etc.

    Non-decorator keys (``slide``, ``content``, or any unknown key) are
    silently ignored — this function is focused solely on the decorator
    portion of the layout.

    Parameters
    ----------
    layout : dict
        The parsed value of ``theme.layout`` from YAML.  May be empty; in
        that case an empty list is returned.

    Returns
    -------
    list[DecoratorSpec]
        Sorted list of :class:`DecoratorSpec` objects, one per decorator
        key found in *layout*.

    Examples
    --------
    >>> specs = parse_layout_decorators({
    ...     "header-1": {"height": "8%", "background": "#1a1a2e",
    ...                  "metadata": {"slidetitle": {"float": "left"}}},
    ...     "footer-1": {"height": "5%",
    ...                  "metadata": {"slidenumber": {"float": "right"}}},
    ...     "sidebar-1": {"position": "L", "width": "20%",
    ...                   "metadata": {"toc": {"depth": "1"}}},
    ...     "slide": {"width": "960", "height": "700"},   # ignored
    ... })
    >>> [s.name for s in specs]
    ['footer-1', 'header-1', 'sidebar-1']
    """
    if not layout or not isinstance(layout, dict):
        return []

    specs: list[DecoratorSpec] = []

    for key, val in layout.items():
        if not (key.startswith("header-") or key.startswith("footer-") or key.startswith("sidebar-")):
            continue
        if not val or not isinstance(val, dict):
            continue

        kind = key.split("-")[0]  # "header", "footer", or "sidebar"

        # Primary size dimension
        if kind == "sidebar":
            size = str(val.get("width", "10%"))
        else:
            size = str(val.get("height", "10%"))

        # Sidebar position
        position = str(val.get("position", "R")).upper() if kind == "sidebar" else ""

        # Active flag (YAML: active: yes/no/true/false)
        raw_active = val.get("active", True)
        if isinstance(raw_active, bool):
            active = raw_active
        else:
            active = str(raw_active).lower() not in {"no", "false", "0"}

        # Metadata placeholders: {meta_key: "prop:val;prop:val;"}
        metadata: dict[str, str] = {}
        raw_meta = val.get("metadata") or {}
        if isinstance(raw_meta, dict):
            for meta_key, meta_props in raw_meta.items():
                if isinstance(meta_props, dict):
                    metadata[meta_key] = "".join(f"{p}:{v};" for p, v in meta_props.items())
                else:
                    # scalar metadata value (e.g. toc: {depth: 1}) — keep as-is
                    metadata[meta_key] = str(meta_props) if meta_props is not None else ""

        # Remaining CSS properties (exclude structural keys)
        css: dict[str, str] = {k: str(v) for k, v in val.items() if k not in _STRUCTURAL_KEYS}

        specs.append(
            DecoratorSpec(
                name=key,
                kind=kind,
                size=size,
                position=position,
                css=css,
                metadata=metadata,
                active=active,
            )
        )

    return sorted(specs, key=lambda s: s.name)


# ---------------------------------------------------------------------------
# Abstract base classes
# ---------------------------------------------------------------------------

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
