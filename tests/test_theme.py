"""
Unit tests for matisse.theme.Theme.

Covers:
- __init__ defaults
- set_from (deep-copy semantics)
- copy_from (non-overwrite merge)
- palette variable resolution via __resolve_palette
- section parsers: canvas, lists, toc, layout, entities
"""

from matisse.theme import Theme

# ---------------------------------------------------------------------------
# __init__
# ---------------------------------------------------------------------------


class TestThemeInit:
    def test_default_canvas_is_empty_list(self):
        t = Theme()
        assert t.canvas == []

    def test_default_slide_is_empty_list(self):
        t = Theme()
        assert t.slide == []

    def test_default_slide_header_is_empty_dict(self):
        t = Theme()
        assert t.slide_header == {}

    def test_default_slide_footer_is_empty_dict(self):
        t = Theme()
        assert t.slide_footer == {}

    def test_default_slide_sidebar_is_empty_dict(self):
        t = Theme()
        assert t.slide_sidebar == {}

    def test_default_css_is_none(self):
        t = Theme()
        assert t.css is None

    def test_default_custom_is_false(self):
        t = Theme()
        assert t.custom is False

    def test_default_copy_from_theme_is_none(self):
        t = Theme()
        assert t.copy_from_theme is None

    def test_toc_attributes_default_to_empty_list(self):
        t = Theme()
        for attr in ("toc", "toc_chapter_emph", "toc_section_emph", "toc_subsection_emph", "toc_slide_emph"):
            assert getattr(t, attr) == [], f"{attr} should default to []"

    def test_env_list_attributes_default_to_empty_list(self):
        t = Theme()
        for attr in (
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
        ):
            assert getattr(t, attr) == [], f"{attr} should default to []"

    def test_str_returns_empty_string_when_css_none(self):
        t = Theme()
        assert str(t) == ""


# ---------------------------------------------------------------------------
# set_from
# ---------------------------------------------------------------------------


class TestSetFrom:
    def test_set_from_copies_canvas(self):
        src = Theme()
        src.canvas = [{"background": "red"}]
        dst = Theme()
        dst.set_from(other=src)
        assert dst.canvas == [{"background": "red"}]

    def test_set_from_is_deep_copy(self):
        """Mutating src after set_from must not affect dst."""
        src = Theme()
        src.canvas = [{"background": "red"}]
        dst = Theme()
        dst.set_from(other=src)
        src.canvas[0]["background"] = "blue"
        assert dst.canvas[0]["background"] == "red"

    def test_set_from_copies_slide(self):
        src = Theme()
        src.slide = [{"width": "900px"}]
        dst = Theme()
        dst.set_from(other=src)
        assert dst.slide == [{"width": "900px"}]

    def test_set_from_copies_custom_flag(self):
        src = Theme()
        src.custom = True
        dst = Theme()
        dst.set_from(other=src)
        assert dst.custom is True

    def test_set_from_copies_css(self):
        src = Theme()
        src.css = "body { color: red; }"
        dst = Theme()
        dst.set_from(other=src)
        assert dst.css == "body { color: red; }"

    def test_set_from_copies_dict_attributes(self):
        src = Theme()
        src.slide_header = {"h1": [{"font-size": "2em"}]}
        dst = Theme()
        dst.set_from(other=src)
        assert dst.slide_header == {"h1": [{"font-size": "2em"}]}

    def test_set_from_dict_is_deep_copy(self):
        src = Theme()
        src.slide_header = {"h1": [{"font-size": "2em"}]}
        dst = Theme()
        dst.set_from(other=src)
        src.slide_header["h1"][0]["font-size"] = "1em"
        assert dst.slide_header["h1"][0]["font-size"] == "2em"

    def test_set_from_all_list_attrs_copied(self):
        """Every attribute in set_from's _attrs list should be transferred."""
        src = Theme()
        src.toc = [{"color": "blue"}]
        src.box = [{"border": "1px solid black"}]
        dst = Theme()
        dst.set_from(other=src)
        assert dst.toc == [{"color": "blue"}]
        assert dst.box == [{"border": "1px solid black"}]


# ---------------------------------------------------------------------------
# copy_from — non-overwrite merge
# ---------------------------------------------------------------------------


class TestCopyFrom:
    def test_copy_from_adds_missing_canvas_entry(self):
        """copy_from should add entries from other that are absent in self."""
        base = Theme()
        base.canvas = [{"background": "white"}]

        override = Theme()
        override.copy_from(other=base)
        assert any("background" in (list(e.keys())[0] if isinstance(e, dict) else e) for e in override.canvas)

    def test_copy_from_does_not_overwrite_existing_canvas_entry(self):
        """An entry already present in self must not be replaced by other's value."""
        base = Theme()
        base.canvas = [{"background": "white"}]

        override = Theme()
        override.canvas = [{"background": "black"}]
        override.copy_from(other=base)
        backgrounds = [e for e in override.canvas if isinstance(e, dict) and "background" in e]
        assert len(backgrounds) == 1
        assert backgrounds[0]["background"] == "black"

    def test_copy_from_dict_keys_fix(self):
        """
        Regression for Phase-1 bug: iterating dict CSS entries used
        css.keys()[0] which fails in Python 3.  Verify copy_from works
        with dict-valued CSS entries (exercises next(iter(css.keys()))).
        """
        base = Theme()
        base.canvas = [{"background": "white"}, {"color": "black"}]

        override = Theme()
        override.copy_from(other=base)
        assert len(override.canvas) == 2


# ---------------------------------------------------------------------------
# Palette resolution
# ---------------------------------------------------------------------------

_PALETTE_SOURCE = """
---
theme:
  palette:
    bg: '#282a36'
    fg: '#f8f8f2'
    accent: '#50fa7b'
  canvas:
    background: '$bg'
  entities:
    box:
      caption:
        color: '$accent'
        border-bottom: '1px solid $accent'
      content:
        color: '$fg'
---
"""


class TestPaletteResolution:
    def test_palette_resolves_in_canvas(self):
        t = Theme()
        t.get(source=_PALETTE_SOURCE)
        backgrounds = [e["background"] for e in t.canvas if "background" in e]
        assert backgrounds == ["#282a36"]

    def test_palette_resolves_in_entity_caption(self):
        t = Theme()
        t.get(source=_PALETTE_SOURCE)
        colors = [e["color"] for e in t.box_caption if "color" in e]
        assert colors == ["#50fa7b"]

    def test_palette_resolves_compound_value(self):
        t = Theme()
        t.get(source=_PALETTE_SOURCE)
        borders = [e["border-bottom"] for e in t.box_caption if "border-bottom" in e]
        assert borders == ["1px solid #50fa7b"]

    def test_palette_resolves_content_color(self):
        t = Theme()
        t.get(source=_PALETTE_SOURCE)
        colors = [e["color"] for e in t.box_content if "color" in e]
        assert colors == ["#f8f8f2"]

    def test_unknown_palette_variable_left_as_is(self, capsys):
        source = """
---
theme:
  canvas:
    background: '$unknown'
---
"""
        t = Theme()
        t.get(source=source)
        # The raw string stays; a warning is printed
        backgrounds = [e["background"] for e in t.canvas if "background" in e]
        assert backgrounds == ["$unknown"]
        captured = capsys.readouterr()
        assert "unknown" in captured.out


# ---------------------------------------------------------------------------
# Section parsers
# ---------------------------------------------------------------------------

_FULL_SOURCE = """
---
theme:
  canvas:
    background: 'black'
  lists:
    ordered-items:
      content: 'counter(item)'
      color: 'red'
    unordered-items:
      color: 'blue'
      content: "'\\\\25A0'"
  toc:
    font-variant: 'small-caps'
    section-emph:
      color: 'green'
    subsection-emph:
      color: 'orange'
  layout:
    slide:
      width: '800px'
      height: '600px'
    content:
      background: 'white'
      padding: '2%'
    header-1:
      height: '10%'
      background: 'navy'
      metadata:
        slidetitle:
          float: 'left'
          font-size: '150%'
    footer-1:
      height: '6%'
      background: 'navy'
      metadata:
        slidenumber:
          float: 'right'
    sidebar-1:
      position: 'L'
      width: '20%'
      background: 'navy'
  entities:
    box:
      display: 'inline-block'
      caption:
        color: 'purple'
      content:
        padding: '0 2%'
    note:
      display: 'inline-block'
      caption:
        background: 'grey'
      content:
        font-size: '120%'
    figure:
      text-align: 'center'
      caption:
        font-size: '80%'
    video:
      caption:
        color: 'red'
      content:
        controls: ''
---
"""


class TestCanvasParser:
    def test_canvas_background_set(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        backgrounds = [e["background"] for e in t.canvas if "background" in e]
        assert backgrounds == ["black"]


class TestListsParser:
    def test_ordered_items_color(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        colors = [e["color"] for e in t.ordered_list_items if "color" in e]
        assert colors == ["red"]

    def test_unordered_items_color(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        colors = [e["color"] for e in t.unordered_list_items if "color" in e]
        assert colors == ["blue"]


class TestTocParser:
    def test_toc_base_css(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        variants = [e["font-variant"] for e in t.toc if "font-variant" in e]
        assert variants == ["small-caps"]

    def test_toc_section_emph(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        colors = [e["color"] for e in t.toc_section_emph if "color" in e]
        assert colors == ["green"]

    def test_toc_subsection_emph(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        colors = [e["color"] for e in t.toc_subsection_emph if "color" in e]
        assert colors == ["orange"]

    def test_toc_chapter_emph_defaults_empty(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        assert t.toc_chapter_emph == []


class TestLayoutParser:
    def test_slide_width(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        widths = [e["width"] for e in t.slide if "width" in e]
        assert widths == ["800px"]

    def test_slide_height(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        heights = [e["height"] for e in t.slide if "height" in e]
        assert heights == ["600px"]

    def test_content_background(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        bgs = [e["background"] for e in t.slide_content if "background" in e]
        assert bgs == ["white"]

    def test_header_registered(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        assert "header-1" in t.slide_header

    def test_header_metadata_parsed(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        assert "header-1" in t.slide_header_metadata
        assert "slidetitle" in t.slide_header_metadata["header-1"]

    def test_footer_registered(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        assert "footer-1" in t.slide_footer

    def test_sidebar_registered(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        assert "sidebar-1" in t.slide_sidebar

    def test_slide_transition_defaults(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        info = t.get_slide_transition()
        assert info["transition"] == "horizontal"
        assert info["width"] == 800
        assert info["height"] == 600


class TestEntitiesParser:
    def test_box_base_css(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        displays = [e["display"] for e in t.box if "display" in e]
        assert displays == ["inline-block"]

    def test_box_caption_color(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        colors = [e["color"] for e in t.box_caption if "color" in e]
        assert colors == ["purple"]

    def test_box_content_padding(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        paddings = [e["padding"] for e in t.box_content if "padding" in e]
        assert paddings == ["0 2%"]

    def test_note_caption_background(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        bgs = [e["background"] for e in t.note_caption if "background" in e]
        assert bgs == ["grey"]

    def test_figure_caption_font_size(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        sizes = [e["font-size"] for e in t.figure_caption if "font-size" in e]
        assert sizes == ["80%"]

    def test_video_content_controls(self):
        t = Theme()
        t.get(source=_FULL_SOURCE)
        controls = [e["controls"] for e in t.video_content if "controls" in e]
        assert controls == [""]


# ---------------------------------------------------------------------------
# Overtheme: copy-from-theme flag location
# ---------------------------------------------------------------------------


class TestOvertheme:
    def test_copy_from_theme_top_level(self):
        source = """
---
overtheme:
  copy-from-theme: true
  layout:
    slide:
      border-radius: '50%'
---
"""
        t = Theme()
        t.get(source=source, name="overtheme")
        assert t.copy_from_theme is True

    def test_overtheme_layout_override(self):
        source = """
---
overtheme:
  layout:
    slide:
      transition: 'absolute'
      data-y: '500'
---
"""
        t = Theme()
        t.get(source=source, name="overtheme")
        info = t.get_slide_transition()
        assert info["transition"] == "absolute"
