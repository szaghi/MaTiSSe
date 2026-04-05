#!/usr/bin/env python3
"""
matisse.backends.impress.theme — ImpressTheme, the impress.js-specific theme.

This module contains the full Theme implementation moved from
``matisse/theme.py``.  ``matisse/theme.py`` is now a thin re-export shim:

    from matisse.backends.impress.theme import ImpressTheme as Theme

ImpressTheme implements AbstractTheme so it can be used interchangeably
through the backend abstraction layer.

Theme YAML schema
-----------------
All content lives under a top-level ``theme:`` (or ``overtheme:``) mapping.
Every section is optional. Example::

    theme:
      palette:                    # named variables — reference with $name
        background: '#282a36'
        accent:     '#50fa7b'
      canvas:                     # viewport / body background
        background: '$background'
      lists:
        ordered-items:
          content: 'counter(item)'
          color: '$accent'
        unordered-items:
          color: '$accent'
          content: "'\\25A0'"
      toc:
        font-variant: 'small-caps'
        section-emph:
          color: '$accent'
      layout:                     # structural shell of each slide
        slide:
          transition: 'horizontal'
          width: '900px'
          height: '700px'
        content:
          background: '$background'
          padding: '2%'
        header-1:
          height: '10%'
          background: '$accent'
          metadata:
            slidetitle:
              float: 'left'
              font-size: '150%'
        footer-1:
          height: '6%'
          metadata:
            slidenumber:
              float: 'right'
        sidebar-1:
          position: 'L'
          width: '20%'
          metadata:
            toc:
              depth: '1'
      entities:                   # content environments
        box:
          display: 'inline-block'
          caption:
            color: '$accent'
          content:
            padding: '0 2%'
        note:
          display: 'inline-block'
          caption:
            background: '$accent'
          content:
            padding: '0 1em'
        table:
          display: 'inline-block'
          caption:
            color: '$accent'
        figure:
          text-align: 'center'
          caption:
            font-size: '80%'
          content:
            padding: '1% 5%'
        video:
          caption:
            color: '$accent'

Per-slide ``overtheme:`` blocks use the same schema, plus an optional
top-level ``copy-from-theme: true`` flag that inherits the presentation
theme before applying overrides.
"""

import re
from collections import OrderedDict
from copy import deepcopy

from yaml import FullLoader, YAMLError, load_all

from ...backends.base import AbstractTheme
from ...box import Box
from ...figure import Figure
from ...note import Note
from ...table import Table
from ...video import Video


class ImpressTheme(AbstractTheme):
    """
    impress.js presentation theme.

    Parses ``theme:`` YAML blocks from the presentation source and emits
    the CSS string that drives the impress.js HTML renderer.
    """

    @classmethod
    def reset(cls):
        """Reset to default state."""
        Box.reset()
        Note.reset()
        Figure.reset()
        Table.reset()
        Video.reset()

    def __init__(self, source=None, name="theme", div_id=""):
        self.copy_from_theme = None
        self.canvas = []
        self.ordered_list = []
        self.unordered_list = []
        self.ordered_list_items = []
        self.unordered_list_items = []
        self.toc = []
        self.toc_chapter_emph = []
        self.toc_section_emph = []
        self.toc_subsection_emph = []
        self.toc_slide_emph = []
        self.slide = []
        self.slide_content = []
        self.slide_header = {}
        self.slide_footer = {}
        self.slide_sidebar = {}
        self.box = []
        self.box_caption = []
        self.box_content = []
        self.note = []
        self.note_caption = []
        self.note_content = []
        self.table = []
        self.table_caption = []
        self.table_content = []
        self.figure = []
        self.figure_caption = []
        self.figure_content = []
        self.video = []
        self.video_caption = []
        self.video_content = []
        self.slide_header_metadata = {}
        self.slide_footer_metadata = {}
        self.slide_sidebar_metadata = {}
        self.css = None
        self.custom = False
        self.div_id = div_id
        if source is not None:
            self.get(source=source, name=name, div_id=div_id)

    def __str__(self):
        if self.css is None:
            return ""
        return self.css

    # ------------------------------------------------------------------
    # AbstractTheme interface
    # ------------------------------------------------------------------

    def to_css(self) -> str:
        """Return the complete CSS string for this theme."""
        return self.css or ""

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def set_from(self, other):
        """Set self attributes deepcopying theme from other theme."""
        _attrs = [
            "canvas",
            "toc",
            "toc_chapter_emph",
            "toc_section_emph",
            "toc_subsection_emph",
            "toc_slide_emph",
            "slide",
            "slide_content",
            "slide_header",
            "slide_footer",
            "slide_sidebar",
            "box",
            "box_caption",
            "box_content",
            "note",
            "note_caption",
            "note_content",
            "table",
            "table_caption",
            "table_content",
            "figure",
            "figure_caption",
            "figure_content",
            "video",
            "video_caption",
            "video_content",
            "slide_header_metadata",
            "slide_footer_metadata",
            "slide_sidebar_metadata",
            "css",
            "custom",
        ]
        for attr in _attrs:
            setattr(self, attr, deepcopy(getattr(other, attr)))

    def copy_from(self, other):
        """Copy attributes from other theme if self has not already set those attributes."""

        def append_css(my_element, other_element):
            if len(other_element) > 0:
                for css in other_element:
                    found = False
                    for mycss in my_element:
                        if isinstance(css, dict):
                            if next(iter(css.keys())) in mycss:
                                found = True
                        elif css in mycss:
                            found = True
                    if not found:
                        if isinstance(my_element, list):
                            my_element.append(css)
                        else:
                            my_element[css] = other_element[css]

        append_css(my_element=self.canvas, other_element=other.canvas)
        append_css(my_element=self.toc, other_element=other.toc)
        append_css(my_element=self.toc_chapter_emph, other_element=other.toc_chapter_emph)
        append_css(my_element=self.toc_section_emph, other_element=other.toc_section_emph)
        append_css(my_element=self.toc_subsection_emph, other_element=other.toc_subsection_emph)
        append_css(my_element=self.toc_slide_emph, other_element=other.toc_slide_emph)
        append_css(my_element=self.slide, other_element=other.slide)
        append_css(my_element=self.slide_content, other_element=other.slide_content)
        for header in other.slide_header:
            if header not in self.slide_header:
                self.slide_header[header] = other.slide_header[header]
            else:
                append_css(my_element=self.slide_header[header], other_element=other.slide_header[header])
        for footer in other.slide_footer:
            if footer not in self.slide_footer:
                self.slide_footer[footer] = other.slide_footer[footer]
            else:
                append_css(my_element=self.slide_footer[footer], other_element=other.slide_footer[footer])
        for sidebar in other.slide_sidebar:
            if sidebar not in self.slide_sidebar:
                self.slide_sidebar[sidebar] = other.slide_sidebar[sidebar]
            else:
                append_css(my_element=self.slide_sidebar[sidebar], other_element=other.slide_sidebar[sidebar])
        append_css(my_element=self.box, other_element=other.box)
        append_css(my_element=self.box_caption, other_element=other.box_caption)
        append_css(my_element=self.box_content, other_element=other.box_content)
        append_css(my_element=self.note, other_element=other.note)
        append_css(my_element=self.note_caption, other_element=other.note_caption)
        append_css(my_element=self.note_content, other_element=other.note_content)
        append_css(my_element=self.table, other_element=other.table)
        append_css(my_element=self.table_caption, other_element=other.table_caption)
        append_css(my_element=self.table_content, other_element=other.table_content)
        append_css(my_element=self.figure, other_element=other.figure)
        append_css(my_element=self.figure_caption, other_element=other.figure_caption)
        append_css(my_element=self.figure_content, other_element=other.figure_content)
        append_css(my_element=self.video, other_element=other.video)
        append_css(my_element=self.video_caption, other_element=other.video_caption)
        append_css(my_element=self.video_content, other_element=other.video_content)
        for header in other.slide_header_metadata:
            if header not in self.slide_header_metadata:
                self.slide_header_metadata[header] = other.slide_header_metadata[header]
            else:
                append_css(
                    my_element=self.slide_header_metadata[header],
                    other_element=other.slide_header_metadata[header],
                )
        for footer in other.slide_footer_metadata:
            if footer not in self.slide_footer_metadata:
                self.slide_footer_metadata[footer] = other.slide_footer_metadata[footer]
            else:
                append_css(
                    my_element=self.slide_footer_metadata[footer],
                    other_element=other.slide_footer_metadata[footer],
                )
        for sidebar in other.slide_sidebar_metadata:
            if sidebar not in self.slide_sidebar_metadata:
                self.slide_sidebar_metadata[sidebar] = other.slide_sidebar_metadata[sidebar]
            else:
                append_css(
                    my_element=self.slide_sidebar_metadata[sidebar],
                    other_element=other.slide_sidebar_metadata[sidebar],
                )
        self.__check_slide()
        self.__get_css()

    @staticmethod
    def theme2css(div, div_id, klass, theme_list):
        """Convert theme list data to CSS."""
        if len(theme_list) > 0:
            head = ""
            if div_id != "":
                head += "#" + div_id
            if div != "":
                head += " " + div + " "
            if klass != "":
                if klass == "slide":
                    head += "." + klass + " "
                else:
                    head += " ." + klass + " "
            css = ["\n" + head + "{"]
            for element in theme_list:
                for key in element:
                    if "metadata" not in key.lower():
                        css.append("\n  " + key + ": " + element[key] + ";")
            css.append("\n}")
            return "".join(css)
        return ""

    @staticmethod
    def check_css_attribute(name, value, css_list, retain=False):
        """Ensure css attribute presence into CSS theme."""
        found = False
        for css in css_list:
            if found:
                break
            for key in css:
                if name.lower() in key.lower():
                    if not retain:
                        css[key] = value
                    found = True
                    break
        if not found:
            css_list.append({name: value})

    def get(self, source, name="theme", div_id=""):
        """Parse theme from source stream."""
        self.div_id = div_id
        if len(source) > 0:
            try:
                for data in load_all(source, Loader=FullLoader):
                    if not data or name not in data:
                        continue
                    theme_data = data[name]
                    if not isinstance(theme_data, dict):
                        continue
                    self.__parse_copy_from(theme_data)
                    resolved = self.__resolve_palette(theme_data)
                    self.__parse_canvas(resolved)
                    self.__parse_lists(resolved)
                    self.__parse_toc(resolved)
                    self.__parse_layout(resolved)
                    self.__parse_entities(resolved)
                self.custom = True
            except YAMLError:
                print("No valid definition of theme has been found")
        self.__get_css()

    def get_slide_decorators_metadata(self, decorator, name):
        """Get the slide decorators (headers, footers, sidebars) metadata placeholders."""
        metadata = getattr(self, "slide_" + decorator + "_metadata")[name]
        placeholders = []
        for data in metadata:
            placeholders.append(r"$" + data + r"[" + metadata[data] + "]")
        return "".join(placeholders)

    def get_slide_transition(self):
        """Get slide transition (positioning) information."""
        infos = {}
        transition = self.__get_attribute(attribute="transition", css_list=self.slide)
        if transition == "":
            transition = "horizontal"
        infos["transition"] = transition

        width = self.__get_attribute(attribute="width", css_list=self.slide)
        if width == "":
            width = "900px"
        infos["width"] = int(width.strip("px"))

        height = self.__get_attribute(attribute="height", css_list=self.slide)
        if height == "":
            height = "700px"
        infos["height"] = int(height.strip("px"))

        offset = self.__get_attribute(attribute="data-offset", css_list=self.slide)
        if offset == "":
            offset = "10"
        infos["offset"] = int(offset)

        scale = self.__get_attribute(attribute="scale", css_list=self.slide)
        if scale == "":
            scale = "1"
        infos["scale"] = int(scale)

        infos["data-x"] = self.__get_attribute(attribute="data-x", css_list=self.slide)
        infos["data-y"] = self.__get_attribute(attribute="data-y", css_list=self.slide)
        infos["data-z"] = self.__get_attribute(attribute="data-z", css_list=self.slide)
        infos["data-rotate-x"] = self.__get_attribute(attribute="data-rotate-x", css_list=self.slide)
        infos["data-rotate-y"] = self.__get_attribute(attribute="data-rotate-y", css_list=self.slide)
        infos["data-rotate-z"] = self.__get_attribute(attribute="data-rotate-z", css_list=self.slide)
        return infos

    # ------------------------------------------------------------------
    # Private: new section parsers
    # ------------------------------------------------------------------

    def __parse_copy_from(self, data):
        """Read the copy-from-theme flag (top-level in overtheme blocks)."""
        if "copy-from-theme" in data:
            self.copy_from_theme = data["copy-from-theme"]

    @staticmethod
    def __resolve_palette(data):
        """Replace $varname tokens in all string values using the palette section.

        If a token references an undefined palette variable, a warning is
        printed and the raw ``$varname`` string is left in place.
        """
        palette = data.get("palette", {})

        def _resolve(val):
            if isinstance(val, str):

                def _replacer(m):
                    key = m.group(1)
                    if key in palette:
                        return str(palette[key])
                    print(f"Warning: palette variable '${key}' not defined")
                    return m.group(0)

                return re.sub(r"\$([A-Za-z][A-Za-z0-9_-]*)", _replacer, val)
            if isinstance(val, dict):
                return {k: _resolve(v) for k, v in val.items()}
            if isinstance(val, list):
                return [_resolve(item) for item in val]
            return val

        result = {}
        for key, val in data.items():
            result[key] = val if key == "palette" else _resolve(val)
        return result

    @staticmethod
    def __dict_to_css_list(d):
        """Convert a flat {prop: value} dict to a list of single-key dicts.

        Boolean values are mapped to 'yes'/'no' so that ``active: yes`` in
        YAML (parsed as Python True) works correctly.
        """
        if not d:
            return []
        result = []
        for k, v in d.items():
            if isinstance(v, bool):
                result.append({k: "yes" if v else "no"})
            else:
                result.append({k: str(v)})
        return result

    def __parse_canvas(self, data):
        """Populate self.canvas from the ``canvas:`` section."""
        if "canvas" in data and data["canvas"]:
            self.canvas = self.__dict_to_css_list(data["canvas"])

    def __parse_lists(self, data):
        """Populate ordered/unordered list attrs from the ``lists:`` section."""
        if "lists" not in data or not data["lists"]:
            return
        lists = data["lists"]
        if lists.get("ordered"):
            self.ordered_list = self.__dict_to_css_list(lists["ordered"])
        if lists.get("ordered-items"):
            self.ordered_list_items = self.__dict_to_css_list(lists["ordered-items"])
        if lists.get("unordered"):
            self.unordered_list = self.__dict_to_css_list(lists["unordered"])
        if lists.get("unordered-items"):
            self.unordered_list_items = self.__dict_to_css_list(lists["unordered-items"])

    def __parse_toc(self, data):
        """Populate TOC attrs from the ``toc:`` section."""
        if "toc" not in data or not data["toc"]:
            return
        toc = data["toc"]
        _emph = {"chapter-emph", "section-emph", "subsection-emph", "slide-emph"}
        base = {k: v for k, v in toc.items() if k not in _emph}
        self.toc = self.__dict_to_css_list(base)
        if "chapter-emph" in toc:
            self.toc_chapter_emph = self.__dict_to_css_list(toc["chapter-emph"])
        if "section-emph" in toc:
            self.toc_section_emph = self.__dict_to_css_list(toc["section-emph"])
        if "subsection-emph" in toc:
            self.toc_subsection_emph = self.__dict_to_css_list(toc["subsection-emph"])
        if "slide-emph" in toc:
            self.toc_slide_emph = self.__dict_to_css_list(toc["slide-emph"])

    @staticmethod
    def __parse_decorator_data(d):
        """Convert a flat decorator dict to the internal list-of-single-key-dicts format.

        The ``metadata`` sub-dict ``{name: {prop: val, ...}, ...}`` is
        converted to the nested list structure expected by
        ``__get_slide_decorators_metadata``.
        """
        if not d:
            return []
        result = []
        for key, val in d.items():
            if key == "metadata":
                meta_list = []
                for meta_name, meta_props in (val or {}).items():
                    if isinstance(meta_props, dict):
                        css_list = [{p: str(pv)} for p, pv in meta_props.items()]
                    else:
                        css_list = []
                    meta_list.append({meta_name: css_list})
                result.append({"metadata": meta_list})
            elif isinstance(val, bool):
                result.append({key: "yes" if val else "no"})
            else:
                result.append({key: str(val)})
        return result

    def __parse_layout(self, data):
        """Populate slide/content/decorator attrs from the ``layout:`` section."""
        if "layout" not in data or not data["layout"]:
            return
        layout = data["layout"]

        if layout.get("slide"):
            self.slide = self.__dict_to_css_list(layout["slide"])

        if layout.get("content"):
            self.slide_content = self.__dict_to_css_list(layout["content"])

        for key, val in layout.items():
            if key.startswith("header-"):
                self.slide_header[key] = self.__parse_decorator_data(val)
            elif key.startswith("footer-"):
                self.slide_footer[key] = self.__parse_decorator_data(val)
            elif key.startswith("sidebar-"):
                self.slide_sidebar[key] = self.__parse_decorator_data(val)

        self.__check_slide()
        self.__get_slide_decorators_metadata()

    def __parse_entities(self, data):
        """Populate box/note/table/figure/video attrs from the ``entities:`` section."""
        if "entities" not in data or not data["entities"]:
            return
        entities = data["entities"]
        for env in ("box", "note", "table", "figure", "video"):
            if env not in entities or not entities[env]:
                continue
            env_data = entities[env]
            base = {}
            caption = {}
            content = {}
            for k, v in env_data.items():
                if k == "caption":
                    caption = v or {}
                elif k == "content":
                    content = v or {}
                else:
                    base[k] = v
            setattr(self, env, self.__dict_to_css_list(base))
            setattr(self, env + "_caption", self.__dict_to_css_list(caption))
            setattr(self, env + "_content", self.__dict_to_css_list(content))

    # ------------------------------------------------------------------
    # Private: slide dimension checks (unchanged)
    # ------------------------------------------------------------------

    def __get_slide_decorators_metadata(self):
        """Get metadata of slide decorators (headers, footers, sidebars)."""

        def __get_decorators(decorator):
            decorators = getattr(self, "slide_" + decorator)
            for decor in decorators:
                getattr(self, "slide_" + decorator + "_metadata")[decor] = OrderedDict()
                for data in decorators[decor]:
                    for key in data:
                        if "metadata" in key.lower():
                            for meta in data[key]:
                                for meta_key in meta:
                                    css = ""
                                    for elem in meta[meta_key]:
                                        for elem_key in elem:
                                            css += elem_key + ":" + elem[elem_key] + ";"
                                    getattr(self, "slide_" + decorator + "_metadata")[decor][meta_key] = css

        __get_decorators(decorator="header")
        __get_decorators(decorator="footer")
        __get_decorators(decorator="sidebar")

    def __check_slide_dimensions(self):
        found_w = False
        found_h = False
        for css in self.slide:
            if found_w and found_h:
                break
            for key in css:
                if "width" in key.lower():
                    found_w = True
                if "height" in key.lower():
                    found_h = True
        if not found_w:
            self.slide.append({"width": "900px"})
        if not found_h:
            self.slide.append({"height": "700px"})

    def __check_slide_headers_dimensions(self):
        for header in self.slide_header:
            margin = [0, 0, 0, 0]
            for css in self.slide_header[header]:
                for key in css:
                    if "margin-top" in key.lower():
                        margin[0] = int(css[key].strip("%"))
                    if "margin-bottom" in key.lower():
                        margin[1] = int(css[key].strip("%"))
                    if "margin-right" in key.lower():
                        margin[2] = int(css[key].strip("%"))
                    if "margin-left" in key.lower():
                        margin[3] = int(css[key].strip("%"))
            found_w = False
            found_h = False
            for css in self.slide_header[header]:
                for key in css:
                    if "width" in key.lower():
                        found_w = True
                        w = int(css[key].strip("%"))
                        css[key] = str(w - margin[2] - margin[3]) + "%"
                    if "height" in key.lower():
                        found_h = True
                        h = int(css[key].strip("%"))
                        css[key] = str(h - margin[0] - margin[1]) + "%"
            if not found_w:
                self.slide_header[header].append({"width": str(100 - margin[2] - margin[3]) + "%"})
            if not found_h:
                self.slide_header[header].append({"height": str(10 - margin[0] - margin[1]) + "%"})

    def __check_slide_footers_dimensions(self):
        for footer in self.slide_footer:
            margin = [0, 0, 0, 0]
            for css in self.slide_footer[footer]:
                for key in css:
                    if "margin-top" in key.lower():
                        margin[0] = int(css[key].strip("%"))
                    if "margin-bottom" in key.lower():
                        margin[1] = int(css[key].strip("%"))
                    if "margin-right" in key.lower():
                        margin[2] = int(css[key].strip("%"))
                    if "margin-left" in key.lower():
                        margin[3] = int(css[key].strip("%"))
            found_w = False
            found_h = False
            for css in self.slide_footer[footer]:
                for key in css:
                    if "width" in key.lower():
                        found_w = True
                        w = int(css[key].strip("%"))
                        css[key] = str(w - margin[2] - margin[3]) + "%"
                    if "height" in key.lower():
                        found_h = True
                        h = int(css[key].strip("%"))
                        css[key] = str(h - margin[0] - margin[1]) + "%"
            if not found_w:
                self.slide_footer[footer].append({"width": str(100 - margin[2] - margin[3]) + "%"})
            if not found_h:
                self.slide_footer[footer].append({"width": str(10 - margin[0] - margin[1]) + "%"})

    @staticmethod
    def __check_active(decorator):
        active = False
        for css in decorator:
            for key in css:
                if "active" in key.lower():
                    active = css[key].lower() == "yes"
        return active

    @staticmethod
    def __get_attribute(attribute, css_list):
        for css in css_list:
            for key in css:
                if attribute in key.lower():
                    return css[key]
        return ""

    def __get_slide_content_height(self):
        height = 0
        for header in self.slide_header:
            active = self.__check_active(decorator=self.slide_header[header])
            if active:
                height += int(self.__get_attribute(attribute="height", css_list=self.slide_header[header]).strip("%"))
                margin = self.__get_attribute(attribute="margin-top", css_list=self.slide_header[header]).strip("%")
                if margin != "":
                    height += int(margin)
                margin = self.__get_attribute(attribute="margin-bottom", css_list=self.slide_header[header]).strip("%")
                if margin != "":
                    height += int(margin)
        for footer in self.slide_footer:
            active = self.__check_active(decorator=self.slide_footer[footer])
            if active:
                height += int(self.__get_attribute(attribute="height", css_list=self.slide_footer[footer]).strip("%"))
                margin = self.__get_attribute(attribute="margin-top", css_list=self.slide_footer[footer]).strip("%")
                if margin != "":
                    height += int(margin)
                margin = self.__get_attribute(attribute="margin-bottom", css_list=self.slide_footer[footer]).strip("%")
                if margin != "":
                    height += int(margin)
        return 100 - height

    def __get_slide_content_width(self):
        width = 0
        for sidebar in self.slide_sidebar:
            active = self.__check_active(decorator=self.slide_sidebar[sidebar])
            if active:
                width += int(self.__get_attribute(attribute="width", css_list=self.slide_sidebar[sidebar]).strip("%"))
                margin = self.__get_attribute(attribute="margin-left", css_list=self.slide_sidebar[sidebar]).strip("%")
                if margin != "":
                    width += int(margin)
                margin = self.__get_attribute(attribute="margin-right", css_list=self.slide_sidebar[sidebar]).strip("%")
                if margin != "":
                    width += int(margin)
        return 100 - width

    def __check_slide_sidebars_dimensions(self):
        height = self.__get_slide_content_height()
        for sidebar in self.slide_sidebar:
            margin = [0, 0, 0, 0]
            for css in self.slide_sidebar[sidebar]:
                for key in css:
                    if "margin-top" in key.lower():
                        margin[0] = int(css[key].strip("%"))
                    if "margin-bottom" in key.lower():
                        margin[1] = int(css[key].strip("%"))
                    if "margin-right" in key.lower():
                        margin[2] = int(css[key].strip("%"))
                    if "margin-left" in key.lower():
                        margin[3] = int(css[key].strip("%"))
            found_w = False
            found_h = False
            for css in self.slide_sidebar[sidebar]:
                for key in css:
                    if "width" in key.lower():
                        found_w = True
                        w = int(css[key].strip("%"))
                        css[key] = str(w - margin[2] - margin[3]) + "%"
                    if "height" in key.lower():
                        found_h = True
                        h = int(css[key].strip("%"))
                        css[key] = str(h - margin[0] - margin[1]) + "%"
            if not found_w:
                self.slide_sidebar[sidebar].append({"width": "10%"})
                self.slide_sidebar[sidebar].append({"width": str(10 - margin[2] - margin[3]) + "%"})
            if not found_h:
                self.slide_sidebar[sidebar].append({"height": str(height - margin[0] - margin[1]) + "%"})

    def __check_slide_content_dimensions(self):
        height = self.__get_slide_content_height()
        width = self.__get_slide_content_width()
        margin = [0, 0, 0, 0]
        for css in self.slide_content:
            for key in css:
                if "margin-top" in key.lower():
                    margin[0] = int(css[key].strip("%"))
                if "margin-bottom" in key.lower():
                    margin[1] = int(css[key].strip("%"))
                if "margin-right" in key.lower():
                    margin[2] = int(css[key].strip("%"))
                if "margin-left" in key.lower():
                    margin[3] = int(css[key].strip("%"))
        found_w = False
        found_h = False
        for css in self.slide_content:
            for key in css:
                if "width" in key.lower():
                    css[key] = str(width - margin[2] - margin[3]) + "%"
                    found_w = True
                if "height" in key.lower():
                    css[key] = str(height - margin[0] - margin[1]) + "%"
                    found_h = True
        if not found_w:
            self.slide_content.append({"width": str(width - margin[2] - margin[3]) + "%"})
        if not found_h:
            self.slide_content.append({"height": str(height - margin[0] - margin[1]) + "%"})

    def __check_slide(self):
        self.check_css_attribute(name="display", value="block", css_list=self.slide)
        self.check_css_attribute(name="display", value="block", css_list=self.slide_content)
        self.check_css_attribute(name="float", value="left", css_list=self.slide_content)
        for header in self.slide_header:
            self.check_css_attribute(name="display", value="block", css_list=self.slide_header[header])
            self.check_css_attribute(name="active", value="yes", css_list=self.slide_header[header], retain=True)
        for footer in self.slide_footer:
            self.check_css_attribute(name="display", value="block", css_list=self.slide_footer[footer])
            self.check_css_attribute(name="active", value="yes", css_list=self.slide_footer[footer], retain=True)
        for sidebar in self.slide_sidebar:
            self.check_css_attribute(name="display", value="block", css_list=self.slide_sidebar[sidebar])
            self.check_css_attribute(name="float", value="left", css_list=self.slide_sidebar[sidebar])
            self.check_css_attribute(name="position", value="R", css_list=self.slide_sidebar[sidebar], retain=True)
            self.check_css_attribute(name="active", value="yes", css_list=self.slide_sidebar[sidebar], retain=True)
        self.__check_slide_dimensions()
        self.__check_slide_headers_dimensions()
        self.__check_slide_footers_dimensions()
        self.__check_slide_sidebars_dimensions()
        self.__check_slide_content_dimensions()

    def __get_css(self):
        css = []
        css.append(self.theme2css(div="body", div_id=self.div_id, klass="", theme_list=self.canvas))
        css.append(self.theme2css(div="ol li", div_id=self.div_id, klass="", theme_list=self.ordered_list))
        css.append(self.theme2css(div="ul li", div_id=self.div_id, klass="", theme_list=self.unordered_list))
        css.append(self.theme2css(div="ol li:before", div_id=self.div_id, klass="", theme_list=self.ordered_list_items))
        css.append(
            self.theme2css(div="ul li:before", div_id=self.div_id, klass="", theme_list=self.unordered_list_items)
        )
        css.append(self.theme2css(div="", div_id=self.div_id, klass="toc", theme_list=self.toc))
        css.append(
            self.theme2css(div="", div_id=self.div_id, klass="toc-chapter-emph", theme_list=self.toc_chapter_emph)
        )
        css.append(
            self.theme2css(div="", div_id=self.div_id, klass="toc-section-emph", theme_list=self.toc_section_emph)
        )
        css.append(
            self.theme2css(div="", div_id=self.div_id, klass="toc-subsection-emph", theme_list=self.toc_subsection_emph)
        )
        css.append(self.theme2css(div="", div_id=self.div_id, klass="toc-slide-emph", theme_list=self.toc_slide_emph))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="slide", theme_list=self.slide))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="slide-content", theme_list=self.slide_content))
        for header in self.slide_header:
            css.append(
                self.theme2css(
                    div="", div_id=self.div_id, klass="slide-" + header, theme_list=self.slide_header[header]
                )
            )
        for footer in self.slide_footer:
            css.append(
                self.theme2css(
                    div="", div_id=self.div_id, klass="slide-" + footer, theme_list=self.slide_footer[footer]
                )
            )
        for sidebar in self.slide_sidebar:
            css.append(
                self.theme2css(
                    div="", div_id=self.div_id, klass="slide-" + sidebar, theme_list=self.slide_sidebar[sidebar]
                )
            )
        css.append(self.theme2css(div="", div_id=self.div_id, klass="box", theme_list=self.box))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="box-caption", theme_list=self.box_caption))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="box-content", theme_list=self.box_content))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="note", theme_list=self.note))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="note-caption", theme_list=self.note_caption))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="note-content", theme_list=self.note_content))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="table", theme_list=self.table))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="table-caption", theme_list=self.table_caption))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="table-content", theme_list=self.table_content))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="figure", theme_list=self.figure))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="figure-caption", theme_list=self.figure_caption))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="figure-content", theme_list=self.figure_content))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="video", theme_list=self.video))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="video-caption", theme_list=self.video_caption))
        css.append(self.theme2css(div="", div_id=self.div_id, klass="video-content", theme_list=self.video_content))
        self.css = "".join(css)
