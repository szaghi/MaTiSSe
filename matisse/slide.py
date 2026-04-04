#!/usr/bin/env python3
"""
slide.py, module definition of Slide class.
"""

from .box import Box
from .columns import Columns
from .figure import Figure
from .markdown_utils import markdown2html
from .note import Note
from .table import Table
from .theme import Theme
from .video import Video


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
          position dictionary containing {'x': posx, 'y': posy, 'z': posz, 'rotx': rotx, 'roty': roty, 'rotz': rotz, 'scale': scaling}
        title: str
        contents: str
        """
        self.number = number
        self.position = None
        self.set_position(position)
        self.title = title
        self.contents = contents
        self.overtheme = Theme()

    def __str__(self):
        strings = [str(self.title)]
        strings.append(str(self.contents))
        return "".join(strings)

    def get_overtheme(self, parser):
        """Get eventual overtheme definition.

        Parameters
        ----------
        parser: Parser
        """
        codeblocks = parser.tokenizer(source=self.contents, re_search=parser.regexs["codeblock"])
        yamlblocks = parser.tokenizer(source=self.contents, re_search=parser.regexs["yamlblock"], exclude=codeblocks)
        if len(yamlblocks) > 0:
            self.overtheme.get(
                source="".join([block["match"].group().strip("---") for block in yamlblocks]),
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
          position dictionary containing {'x': posx, 'y': posy, 'z': posz, 'rotx': rotx, 'roty': roty, 'rotz': rotz, 'scale': scaling}
        """
        if position is not None:
            self.position = {}
            for key in position:
                self.position[key] = position[key]

    def _parse_env(self, parser, theme, Env, re_search, source):
        """Parse an environment block from source, replacing it with its HTML.

        Parameters
        ----------
        parser: Parser
        theme: Theme()
          presentation theme
        Env: class
          environment class (Box, Note, Figure, Table, Video, Columns)
        re_search: compiled regex
        source: str

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
                obj = Env(source=env["match"].group())
                parsed_source += obj.to_html() + source[env["end"] : envs[e + 1]["start"]]
            if Env is Video:
                if self.overtheme.custom:
                    obj = Env(source=envs[-1]["match"].group(), theme=self.overtheme)
                else:
                    obj = Env(source=envs[-1]["match"].group(), theme=theme)
            else:
                obj = Env(source=envs[-1]["match"].group())
            parsed_source += obj.to_html() + source[envs[-1]["end"] :]
            return parsed_source
        return source

    def to_html(self, doc, parser, metadata, theme, current):
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
        """
        html = self.contents
        for meta in metadata:
            html = metadata[meta].parse(
                parser=parser,
                source=html,
                toc_depth=metadata["toc_depth"].value,
                max_time=metadata["max_time"].value,
                current=current,
            )
        html = self._parse_env(parser=parser, theme=theme, Env=Box, re_search=Box.regexs["box"], source=html)
        html = self._parse_env(parser=parser, theme=theme, Env=Note, re_search=Note.regexs["note"], source=html)
        html = self._parse_env(parser=parser, theme=theme, Env=Figure, re_search=Figure.regexs["figure"], source=html)
        html = self._parse_env(parser=parser, theme=theme, Env=Table, re_search=Table.regexs["table"], source=html)
        html = self._parse_env(parser=parser, theme=theme, Env=Video, re_search=Video.regexs["video"], source=html)
        html = self._parse_env(
            parser=parser, theme=theme, Env=Columns, re_search=Columns.regexs["columns"], source=html
        )
        with doc.tag("div", klass="slide-content"):
            doc.asis(markdown2html(source=html))
