#!/usr/bin/env python3
"""
presentation.py, module definition of Presentation class.
"""

from __future__ import annotations

import os
from collections import OrderedDict
from shutil import copytree

from yaml import FullLoader, YAMLError, load_all

from .chapter import Chapter
from .diagram import Diagram
from .labels import LabelRegistry
from .metadata import Metadata
from .parser import Parser
from .position import Position
from .section import Section
from .slide import Slide
from .subsection import Subsection
from .theorem import Theorem
from .theme import Theme


class Presentation(object):
    """
    Presentation object.

    Attributes
    ----------
    chapters_number: int
    """

    chapters_number = 0

    @classmethod
    def reset(cls):
        """Reset to default state."""
        cls.chapters_number = 0
        Theme.reset()
        Chapter.reset()
        Theorem.reset()
        Diagram.reset()

    def __init__(self):
        """
        Attributes
        ----------
        metadata: dict
          presentation metadata; each element of the dictionary if a dict with ['value', 'user'] items: value contains
          the metadata value and user indicates if the value comes from user (if True) or from defaults (if False).
        """
        self.reset()
        self.metadata = {
            "title": Metadata(name="title", value=""),
            "subtitle": Metadata(name="subtitle", value=""),
            "authors": Metadata(name="authors", value=[]),
            "authors_short": Metadata(name="authors_short", value=[]),
            "emails": Metadata(name="emails", value=[]),
            "affiliations": Metadata(name="affiliations", value=[]),
            "affiliations_short": Metadata(name="affiliations_short", value=[]),
            "logo": Metadata(name="logo", value=""),
            "timer": Metadata(name="timer", value=""),
            "location": Metadata(name="location", value=""),
            "location_short": Metadata(name="location_short", value=""),
            "date": Metadata(name="date", value=""),
            "conference": Metadata(name="conference", value=""),
            "conference_short": Metadata(name="conference_short", value=""),
            "session": Metadata(name="session", value=""),
            "session_short": Metadata(name="session_short", value=""),
            "max_time": Metadata(name="max_time", value="25"),
            "total_slides_number": Metadata(name="total_slides_number", value=""),
            "dirs_to_copy": Metadata(name="dirs_to_copy", value=[]),
            "toc": Metadata(name="toc", value=OrderedDict()),
            "toc_depth": Metadata(name="toc_depth", value="2"),
            "chaptertitle": Metadata(name="chaptertitle", value=""),
            "chapternumber": Metadata(name="chapternumber", value=""),
            "sectiontitle": Metadata(name="sectiontitle", value=""),
            "sectionnumber": Metadata(name="sectionnumber", value=""),
            "subsectiontitle": Metadata(name="subsectiontitle", value=""),
            "subsectionnumber": Metadata(name="subsectionnumber", value=""),
            "slidetitle": Metadata(name="slidetitle", value=""),
            "slidenumber": Metadata(name="slidenumber", value=""),
            "css_overtheme": Metadata(name="css_overtheme", value=[]),
            "custom": Metadata(name="custom-[0-9]*", value=""),
        }
        self.theme = Theme()
        self.parser = Parser()
        self.chapters = []
        self.position = Position()
        self.source: str = ""       # fully expanded source (after $include)
        self.yaml_source: str = ""  # concatenated YAML block content (used by reveal backend)
        # Phase 7 — label registry for cross-references
        self.label_registry: LabelRegistry = LabelRegistry()
        # Phase 7b — bibliography (optional)
        self.bibliography: str = ""   # path to .bib file
        self.csl: str = ""            # path to .csl file

    def __str__(self):
        strings = [f"Chapters number {Presentation.chapters_number}"]
        strings.append(f"Sections number {Chapter.sections_number}")
        strings.append(f"Subsections number {Section.subsections_number}")
        strings.append(f"Slides number {Subsection.slides_number}")
        for chapter in self.chapters:
            strings.append(str(chapter))
        return "\n".join(strings)

    def __update_toc(self):
        """Update TOC after a new chapter (the last one) has been added."""
        self.metadata["toc"].value[self.chapters[-1].title] = self.chapters[-1].toc

    def __get_metadata(self, source):
        """
        Get metadata from source stream.

        Parameters
        ----------
        source: str
        """
        codeblocks = self.parser.tokenizer(source=source, re_search=self.parser.regexs["codeblock"])
        yamlblocks = self.parser.tokenizer(source=source, re_search=self.parser.regexs["yamlblock"], exclude=codeblocks)
        try:
            for block in yamlblocks:
                for data in load_all(block["match"].group().strip("---"), Loader=FullLoader):
                    if "metadata" in data:
                        for element in data["metadata"]:
                            for key in element:
                                if key in self.metadata:
                                    self.metadata[key].update_value(value=element[key])
        except YAMLError:
            print("No valid definition of metadata has been found")

    def __get_theme(self, source):
        """
        Get theme from source stream.

        Parameters
        ----------
        source: str
        """
        codeblocks = self.parser.tokenizer(source=source, re_search=self.parser.regexs["codeblock"])
        yamlblocks = self.parser.tokenizer(source=source, re_search=self.parser.regexs["yamlblock"], exclude=codeblocks)
        self.yaml_source = "".join([block["match"].group().strip("---") for block in yamlblocks])
        self.theme.get(self.yaml_source)

    def __add_chapter(self, chapter):
        """
        Add a chapter to the presentation.

        Parameters
        ----------
        chapter: Chapter
        """
        Presentation.chapters_number += 1
        self.chapters.append(chapter)
        self.__update_toc()

    def __check_bad_sectioning(self, tokens):
        """Check if the presentation has a bad sectioning.

        Parameters
        ----------
        tokens: Parser.tokens
        source: str
        """
        if "$titlepage" not in tokens["slides"][0]["match"].group().lower():
            if (
                tokens["slides"][0]["start"] < tokens["subsections"][0]["start"]
                or tokens["slides"][0]["start"] < tokens["sections"][0]["start"]
                or tokens["slides"][0]["start"] < tokens["chapters"][0]["start"]
            ):
                print("Warning: found bad presentation sectioning!")
                print("The slide definition:")
                print(tokens["slides"][0]["match"].group() + "\n")
                print("is placed before the first defined chapter/section/subsection.")
                print("All contents before the first defined chapter/section/subsection is omitted!")
                print()

    def __make_toc_slide(self, slides_number, depth):
        """Create a Table of Contents slide at the current position.

        Parameters
        ----------
        slides_number : int
          slide number to assign
        depth : int or str
          TOC depth

        Returns
        -------
        Slide
        """
        self.position.update_position(presentation_theme=self.theme)
        return Slide(
            number=slides_number,
            position=self.position.position,
            title="Table of Contents",
            contents=f"$toc[depth:{depth}]",
        )

    def __build_slides(
        self,
        tokens,
        subsec,
        subsection,
        slides_number,
        slide_local_numbers,
        titlepage_inserted,
        complete_source,
        config,
    ):
        """Build slides for one subsection token, inserting TOC slides as configured.

        Parameters
        ----------
        tokens : dict
        subsec : dict
          subsection token
        subsection : Subsection
        slides_number : int
        slide_local_numbers : list
        titlepage_inserted : bool
        complete_source : str
        config : MatisseConfig

        Returns
        -------
        slides_number : int
        titlepage_inserted : bool
        """
        for sld in tokens["slides"]:
            if "$titlepage" in sld["match"].group().lower() and not titlepage_inserted:
                slide = Slide(number=0, title="titlepage", contents=complete_source[sld["end"] : sld["end_next"]])
                slide.get_overtheme(parser=self.parser)
                if slide.overtheme.copy_from_theme is not None and slide.overtheme.copy_from_theme:
                    slide.overtheme.copy_from(other=self.theme)
                self.position.update_position(presentation_theme=self.theme, overtheme=slide.overtheme)
                slide.set_position(position=self.position.position)
                subsection.add_slide(slide=slide)
                titlepage_inserted = True
            elif sld["start"] >= subsec["start"] and sld["start"] <= subsec["end_next"]:
                slide_local_numbers[0] += 1
                slide_local_numbers[1] += 1
                slide_local_numbers[2] += 1
                if slide_local_numbers[0] == 1 and config.toc_at_chap_beginning is not None:
                    slides_number += 1
                    subsection.add_slide(slide=self.__make_toc_slide(slides_number, config.toc_at_chap_beginning))
                if slide_local_numbers[1] == 1 and config.toc_at_sec_beginning is not None:
                    slides_number += 1
                    subsection.add_slide(slide=self.__make_toc_slide(slides_number, config.toc_at_sec_beginning))
                if slide_local_numbers[2] == 1 and config.toc_at_subsec_beginning is not None:
                    slides_number += 1
                    subsection.add_slide(slide=self.__make_toc_slide(slides_number, config.toc_at_subsec_beginning))
                slides_number += 1
                slide = Slide(
                    number=slides_number,
                    title=sld["match"].group("expr"),
                    contents=complete_source[sld["end"] : sld["end_next"]],
                )
                slide.get_overtheme(parser=self.parser)
                if slide.overtheme.copy_from_theme is not None and slide.overtheme.copy_from_theme:
                    slide.overtheme.copy_from(other=self.theme)
                self.position.update_position(presentation_theme=self.theme, overtheme=slide.overtheme)
                slide.set_position(position=self.position.position)
                subsection.add_slide(slide=slide)
        return slides_number, titlepage_inserted

    def __parse_chapters(self, tokens, complete_source, config):
        """Iterate over chapter/section/subsection/slide tokens to build the document tree.

        Parameters
        ----------
        tokens : dict
        complete_source : str
        config : MatisseConfig
        """
        chapters_number = 0
        sections_number = 0
        subsections_number = 0
        slides_number = 0
        titlepage_inserted = False
        for chap in tokens["chapters"]:
            chapters_number += 1
            slide_local_numbers = [0, 0, 0]
            title = chap["match"].group("expr") or ""
            chapter = Chapter(number=chapters_number, title=title)
            for sec in tokens["sections"]:
                if sec["start"] >= chap["start"] and sec["start"] <= chap["end_next"]:
                    sections_number += 1
                    slide_local_numbers[1] = 0
                    slide_local_numbers[2] = 0
                    section = Section(number=sections_number, title=sec["match"].group("expr"))
                    for subsec in tokens["subsections"]:
                        if subsec["start"] >= sec["start"] and subsec["start"] <= sec["end_next"]:
                            subsections_number += 1
                            slide_local_numbers[2] = 0
                            subsection = Subsection(number=subsections_number, title=subsec["match"].group("expr"))
                            slides_number, titlepage_inserted = self.__build_slides(
                                tokens=tokens,
                                subsec=subsec,
                                subsection=subsection,
                                slides_number=slides_number,
                                slide_local_numbers=slide_local_numbers,
                                titlepage_inserted=titlepage_inserted,
                                complete_source=complete_source,
                                config=config,
                            )
                            section.add_subsection(subsection=subsection)
                    chapter.add_section(section=section)
            self.__add_chapter(chapter=chapter)
            self.metadata["total_slides_number"].update_value(value=str(Subsection.slides_number))

    def parse(self, config, source: str) -> None:
        """Parse presentation from source stream.

        Parameters
        ----------
        config : MatisseConfig
          MaTiSSe configuration
        source: str
        """
        complete_source = self.parser.includes(source=source)
        self.source = complete_source
        if config.print_parsed_source:
            print(complete_source)
        self.__get_metadata(source=complete_source)
        self.__get_theme(source=complete_source)
        new_theme = Theme()
        new_theme.set_from(other=self.theme)
        tokens = self.parser.tokenize(source=complete_source)
        self.__check_bad_sectioning(tokens=tokens)
        self.__parse_chapters(tokens=tokens, complete_source=complete_source, config=config)
        # Phase 7 — collect labels for cross-reference resolution
        self._collect_labels()

    def _collect_labels(self) -> None:
        """Phase 7 — first pass: register all ``{#PREFIX-id}`` labels.

        Walks every slide's raw contents and heading attributes so that
        ``@PREFIX-id`` references can be resolved during rendering.
        """
        self.label_registry = LabelRegistry()
        for chapter in self.chapters:
            for section in chapter.sections:
                for subsection in section.subsections:
                    for slide in subsection.slides:
                        self.label_registry.collect_from_source(slide.contents or "")
                        # Also scan heading attrs for labeled figures, etc.
                        for key, val in slide.heading_attrs.items():
                            pass  # heading attrs don't carry #{} labels directly

    def to_html(self, config) -> str:
        """Generate a html stream of the whole presentation.

        Parameters
        ----------
        config : MatisseConfig
          MaTiSSe configuration
        """
        from .backends.impress.renderer import ImpressBackend

        return ImpressBackend(config).render(self)

    def save(self, config, output):
        """Save the html form of presentation into external file.

        Parameters
        ----------
        config : MatisseConfig
          MaTiSSe configuration
        output : str
          output path
        """
        if not os.path.exists(output):
            os.makedirs(output)

        if config.backend == "reveal":
            from .backends.reveal.renderer import RevealBackend

            backend = RevealBackend(config)
        else:
            from .backends.impress.renderer import ImpressBackend

            backend = ImpressBackend(config)

        with open(os.path.join(output, "index.html"), "w") as html:
            html.write(backend.render(self))

        # copy user defined directories if set
        if len(self.metadata["dirs_to_copy"].value) > 0:
            for data in self.metadata["dirs_to_copy"].value:
                copytree(data, os.path.join(output, data), dirs_exist_ok=True)

        # regenerate pygments.css if the theme specifies a code style override
        if config.code_highlight:
            effective_style = self.theme.code_style if self.theme.code_style else config.code_style
            if effective_style != config.code_style:
                from .markdown_utils import get_pygments_css

                with open(os.path.join(output, "css", "pygments.css"), "w") as fh:
                    fh.write(get_pygments_css(style=effective_style))

        # impress.js-specific CSS assets (theme.css + per-slide overtheme CSS)
        if config.backend != "reveal":
            with open(os.path.join(output, "css/theme.css"), "w") as css_theme:
                css_theme.writelines(self.theme.css)
            for chapter in self.chapters:
                for section in chapter.sections:
                    for subsection in section.subsections:
                        for slide in subsection.slides:
                            if slide.overtheme.custom:
                                with open(
                                    os.path.join(output, f"css/slide-{slide.number}-overtheme.css"),
                                    "w",
                                ) as css_theme:
                                    css_theme.writelines(slide.overtheme.css)
