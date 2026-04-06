#!/usr/bin/env python3
"""
slide.py, module definition of Slide class.
"""

import re

from .box import Box
from .callout import Callout
from .columns import Columns
from .diagram import Diagram
from .figure import Figure
from .figure_group import FigureGroup
from .incremental import PAUSE_RE, IncrementalList
from .markdown_utils import markdown2html
from .note import Note
from .substep import Substep
from .table import Table
from .theorem import Theorem
from .theme import Theme
from .video import Video

# Regex that captures a ``{key=value ...}`` attribute block at the end of a
# slide heading, e.g. ``#### My Slide {background-color="#abc"}``
_HEADING_ATTRS_RE = re.compile(r"\{(?P<attrs>[^}]*)\}\s*$")
# Keys accepted as per-slide background attributes.
_BACKGROUND_KEYS = frozenset(
    [
        "background-color",
        "background-image",
        "background-size",
        "background-position",
        "background-opacity",
        "background-video",
        "background-video-loop",
        "background-video-muted",
    ]
)


def _parse_attr_block(attrs_str: str) -> dict:
    """Parse a ``key=value`` attribute string into a dict.

    Values may be quoted (``"..."`` or ``'...'``) or bare words.
    """
    result = {}
    for m in re.finditer(
        r'(?P<key>[\w-]+)\s*=\s*(?:"(?P<dq>[^"]*)"|\'(?P<sq>[^\']*)\'|(?P<bare>[^\s}]*))',
        attrs_str,
    ):
        value = m.group("dq") or m.group("sq") or m.group("bare") or ""
        result[m.group("key")] = value
    return result


class Slide(object):
    """
    Slide object.
    """

    @classmethod
    def reset(cls):
        """Reset to default state."""
        pass

    def __init__(self, number, position=None, title=None, contents=None):
        """
        Parameters
        ----------
        number: int
          slide global number
        position: dict
          position dictionary containing {'x': posx, 'y': posy, 'z': posz,
          'rotx': rotx, 'roty': roty, 'rotz': rotz, 'scale': scaling}
        title: str
        contents: str
        """
        self.number = number
        self.position = None
        self.set_position(position)
        self.contents = contents
        self.overtheme = Theme()
        self.raw_overtheme_yaml: str = ""  # preserved for backend-specific parsing

        # Phase 5 — heading attribute parsing
        raw_title = title or ""
        m = _HEADING_ATTRS_RE.search(raw_title)
        if m:
            self.heading_attrs: dict = _parse_attr_block(m.group("attrs"))
            self.title: str = raw_title[: m.start()].strip()
        else:
            self.heading_attrs = {}
            self.title = raw_title

    def __str__(self):
        strings = [str(self.title)]
        strings.append(str(self.contents))
        return "".join(strings)

    # ------------------------------------------------------------------
    # Phase 5 — per-slide background helpers
    # ------------------------------------------------------------------

    def background_style(self) -> str:
        """Return inline CSS for impress.js background (colour / image)."""
        parts = []
        bg_color = self.heading_attrs.get("background-color", "")
        if bg_color:
            parts.append(f"background-color: {bg_color}")
        bg_image = self.heading_attrs.get("background-image", "")
        if bg_image:
            bg_size = self.heading_attrs.get("background-size", "cover")
            bg_pos = self.heading_attrs.get("background-position", "center")
            parts.append(f"background-image: url('{bg_image}')")
            parts.append(f"background-size: {bg_size}")
            parts.append(f"background-position: {bg_pos}")
        return "; ".join(parts)

    def reveal_background_attrs(self) -> dict:
        """Return a dict of ``data-background-*`` attributes for reveal.js."""
        attrs = {}
        for key in _BACKGROUND_KEYS:
            val = self.heading_attrs.get(key, "")
            if val:
                attrs[f"data-{key}"] = val
        return attrs

    # ------------------------------------------------------------------
    # Overtheme parsing
    # ------------------------------------------------------------------

    def get_overtheme(self, parser):
        """Get eventual overtheme definition.

        Parameters
        ----------
        parser: Parser
        """
        codeblocks = parser.tokenizer(source=self.contents, re_search=parser.regexs["codeblock"])
        yamlblocks = parser.tokenizer(source=self.contents, re_search=parser.regexs["yamlblock"], exclude=codeblocks)
        if len(yamlblocks) > 0:
            combined_yaml = "".join([block["match"].group().strip("---") for block in yamlblocks])
            self.raw_overtheme_yaml = combined_yaml
            self.overtheme.get(
                source=combined_yaml,
                name="overtheme",
                div_id=f"slide-{self.number}",
            )
            purged_contents = self.contents[: yamlblocks[0]["start"]]
            for b, yamlblock in enumerate(yamlblocks[:-1]):
                purged_contents += self.contents[yamlblock["end"] : yamlblocks[b + 1]["start"]]
            purged_contents += self.contents[yamlblocks[-1]["end"] :]
            self.contents = purged_contents

    def set_position(self, position):
        """Set slide position.

        Parameters
        ----------
        position: dict
          position dictionary
        """
        if position is not None:
            self.position = {}
            for key in position:
                self.position[key] = position[key]

    # ------------------------------------------------------------------
    # Environment parsing helpers
    # ------------------------------------------------------------------

    def _parse_env(self, parser, theme, Env, re_search, source, backend="impress"):
        """Parse an environment block from source, replacing it with its HTML.

        Parameters
        ----------
        parser: Parser
        theme: Theme()
          presentation theme
        Env: class
          environment class (Box, Note, Figure, Table, Video, Columns, etc.)
        re_search: compiled regex
        source: str
        backend: str
          rendering backend; passed to Note/IncrementalList/Callout/Theorem
          to select backend-specific rendering.

        Returns
        -------
        str
          source with environment blocks replaced by HTML
        """
        codeblocks = parser.tokenizer(source=source, re_search=parser.regexs["codeblock"])
        codes = parser.tokenizer(source=source, re_search=parser.regexs["code"], exclude=codeblocks)
        yamlblocks = parser.tokenizer(source=source, re_search=parser.regexs["yamlblock"], exclude=codeblocks + codes)
        envs = parser.tokenizer(source=source, re_search=re_search, exclude=codeblocks + yamlblocks + codes)
        if len(envs) > 0:
            parsed_source = source[: envs[0]["start"]]
            for e, env in enumerate(envs[:-1]):
                html_fragment = self._env_to_html(Env, env["match"].group(), theme, backend)
                parsed_source += html_fragment + source[env["end"] : envs[e + 1]["start"]]
            html_fragment = self._env_to_html(Env, envs[-1]["match"].group(), theme, backend)
            parsed_source += html_fragment + source[envs[-1]["end"] :]
            return parsed_source
        return source

    def _env_to_html(self, Env, source, theme, backend):
        """Instantiate *Env* from *source* and return its HTML string."""
        if Env is Video:
            obj = Env(source=source, theme=self.overtheme if self.overtheme.custom else theme)
        else:
            obj = Env(source=source)

        if Env is Note:
            notes_style = getattr(
                self.overtheme if self.overtheme.custom else theme, "notes_style", "console"
            )
            return obj.to_html(backend=backend, notes_style=notes_style)

        # Environments whose to_html() accepts a backend parameter
        if Env in (IncrementalList, Callout, Theorem):
            return obj.to_html(backend=backend)

        return obj.to_html()

    # ------------------------------------------------------------------
    # Phase 2 — diagram processing (pre-markdown, before other envs)
    # ------------------------------------------------------------------

    def _process_diagrams(self, source, backend="impress"):
        """Replace ``{mermaid}`` / ``{dot}`` fenced blocks with HTML fragments.

        Diagram blocks are code blocks and therefore excluded from the standard
        ``_parse_env`` exclusion checks.  They must be processed before the
        markdown pass converts them to ``<pre><code>`` elements.
        """

        def _replace(m):
            d = Diagram(source=m.group(0))
            return d.to_html(backend=backend)

        return Diagram.regexs["diagram"].sub(_replace, source)

    # ------------------------------------------------------------------
    # Phase 4 — pause marker processing
    # ------------------------------------------------------------------

    def _process_pause_markers(self, source, parser, theme, current, backend):
        """Split *source* on ``. . .`` pause markers and wrap subsequent
        chunks in fragment (reveal) or substep (impress) divs.

        Returns the final HTML string (already markdown-converted).
        """
        chunks = PAUSE_RE.split(source)
        if len(chunks) <= 1:
            return markdown2html(source=source)

        fragment_class = "fragment" if backend == "reveal" else "substep"
        parts = []
        for i, chunk in enumerate(chunks):
            chunk_html = markdown2html(source=chunk.strip()) if chunk.strip() else ""
            if i == 0:
                parts.append(chunk_html)
            else:
                if chunk_html:
                    parts.append(f'<div class="{fragment_class}">{chunk_html}</div>')
        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Main HTML generation
    # ------------------------------------------------------------------

    def to_html(self, doc, parser, metadata, theme, current, backend="impress", label_registry=None):
        """Generate html from self.

        Parameters
        ----------
        doc: Doc
        parser: Parser
        metadata: dict
          presentation metadata
        theme: Theme()
          presentation theme
        current: list
        backend: str
          rendering backend.  When ``"reveal"``, ``$note`` environments are
          emitted as ``<aside class="notes">`` (speaker notes) instead of the
          default visible note boxes.
        label_registry: LabelRegistry | None
          optional registry for cross-reference resolution (Phase 7).
        """
        html = self.contents

        # Metadata substitution
        for meta in metadata:
            html = metadata[meta].parse(
                parser=parser,
                source=html,
                toc_depth=metadata["toc_depth"].value,
                max_time=metadata["max_time"].value,
                current=current,
            )

        # Phase 2: diagrams first (code-block contexts, processed before markdown)
        html = self._process_diagrams(html, backend=backend)

        # Phase 6: subfigure groups MUST run before Figure so the inner
        # $figure...$endfigure blocks are still in raw form when FigureGroup
        # extracts them.
        html = self._parse_env(
            parser=parser,
            theme=theme,
            Env=FigureGroup,
            re_search=FigureGroup.regexs["figure_group"],
            source=html,
            backend=backend,
        )

        # Standard environments
        html = self._parse_env(parser=parser, theme=theme, Env=Box, re_search=Box.regexs["box"], source=html)
        html = self._parse_env(
            parser=parser, theme=theme, Env=Note, re_search=Note.regexs["note"], source=html, backend=backend
        )
        html = self._parse_env(parser=parser, theme=theme, Env=Figure, re_search=Figure.regexs["figure"], source=html)
        html = self._parse_env(parser=parser, theme=theme, Env=Table, re_search=Table.regexs["table"], source=html)
        html = self._parse_env(parser=parser, theme=theme, Env=Video, re_search=Video.regexs["video"], source=html)
        html = self._parse_env(
            parser=parser, theme=theme, Env=Columns, re_search=Columns.regexs["columns"], source=html
        )
        html = self._parse_env(
            parser=parser, theme=theme, Env=Substep, re_search=Substep.regexs["substep"], source=html
        )

        # Phase 1: callout blocks
        html = self._parse_env(
            parser=parser, theme=theme, Env=Callout, re_search=Callout.regexs["callout"], source=html, backend=backend
        )

        # Phase 3: theorem/lemma/proof environments
        html = self._parse_env(
            parser=parser,
            theme=theme,
            Env=Theorem,
            re_search=Theorem.regexs["theorem"],
            source=html,
            backend=backend,
        )

        # Phase 4: incremental lists
        html = self._parse_env(
            parser=parser,
            theme=theme,
            Env=IncrementalList,
            re_search=IncrementalList.regexs["incremental"],
            source=html,
            backend=backend,
        )

        # Phase 4: pause markers + markdown conversion
        content_html = self._process_pause_markers(html, parser, theme, current, backend)

        # Phase 7: cross-reference substitution
        if label_registry is not None:
            content_html = label_registry.substitute_refs(content_html)

        with doc.tag("div", klass="slide-content"):
            doc.asis(content_html)
