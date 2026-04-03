"""
Unit tests for matisse.theme.Theme.

Covers: __init__ defaults, set_from (deep-copy semantics), copy_from
(non-overwrite merge), and the Phase-1 dict.keys() fix that is exercised
inside copy_from via next(iter(css.keys())).
"""
import pytest

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
        for attr in ('toc', 'toc_chapter_emph', 'toc_section_emph',
                     'toc_subsection_emph', 'toc_slide_emph'):
            assert getattr(t, attr) == [], f'{attr} should default to []'

    def test_env_list_attributes_default_to_empty_list(self):
        t = Theme()
        for attr in ('box', 'box_caption', 'box_content',
                     'note', 'note_caption', 'note_content',
                     'table', 'table_caption', 'table_content',
                     'figure', 'figure_caption', 'figure_content',
                     'video', 'video_caption', 'video_content'):
            assert getattr(t, attr) == [], f'{attr} should default to []'

    def test_str_returns_empty_string_when_css_none(self):
        t = Theme()
        assert str(t) == ''


# ---------------------------------------------------------------------------
# set_from
# ---------------------------------------------------------------------------

class TestSetFrom:
    def test_set_from_copies_canvas(self):
        src = Theme()
        src.canvas = [{'background': 'red'}]
        dst = Theme()
        dst.set_from(other=src)
        assert dst.canvas == [{'background': 'red'}]

    def test_set_from_is_deep_copy(self):
        """Mutating src after set_from must not affect dst."""
        src = Theme()
        src.canvas = [{'background': 'red'}]
        dst = Theme()
        dst.set_from(other=src)
        src.canvas[0]['background'] = 'blue'
        assert dst.canvas[0]['background'] == 'red'

    def test_set_from_copies_slide(self):
        src = Theme()
        src.slide = [{'width': '900px'}]
        dst = Theme()
        dst.set_from(other=src)
        assert dst.slide == [{'width': '900px'}]

    def test_set_from_copies_custom_flag(self):
        src = Theme()
        src.custom = True
        dst = Theme()
        dst.set_from(other=src)
        assert dst.custom is True

    def test_set_from_copies_css(self):
        src = Theme()
        src.css = 'body { color: red; }'
        dst = Theme()
        dst.set_from(other=src)
        assert dst.css == 'body { color: red; }'

    def test_set_from_copies_dict_attributes(self):
        src = Theme()
        src.slide_header = {'h1': [{'font-size': '2em'}]}
        dst = Theme()
        dst.set_from(other=src)
        assert dst.slide_header == {'h1': [{'font-size': '2em'}]}

    def test_set_from_dict_is_deep_copy(self):
        src = Theme()
        src.slide_header = {'h1': [{'font-size': '2em'}]}
        dst = Theme()
        dst.set_from(other=src)
        src.slide_header['h1'][0]['font-size'] = '1em'
        assert dst.slide_header['h1'][0]['font-size'] == '2em'

    def test_set_from_all_list_attrs_copied(self):
        """Every attribute in set_from's _attrs list should be transferred."""
        src = Theme()
        src.toc = [{'color': 'blue'}]
        src.box = [{'border': '1px solid black'}]
        dst = Theme()
        dst.set_from(other=src)
        assert dst.toc == [{'color': 'blue'}]
        assert dst.box == [{'border': '1px solid black'}]


# ---------------------------------------------------------------------------
# copy_from — non-overwrite merge
# ---------------------------------------------------------------------------

class TestCopyFrom:
    def test_copy_from_adds_missing_canvas_entry(self):
        """copy_from should add entries from other that are absent in self."""
        base = Theme()
        base.canvas = [{'background': 'white'}]

        override = Theme()
        # override has no canvas; after copy_from it should inherit base's canvas
        override.copy_from(other=base)
        assert any('background' in (list(e.keys())[0] if isinstance(e, dict) else e)
                   for e in override.canvas)

    def test_copy_from_does_not_overwrite_existing_canvas_entry(self):
        """An entry already present in self must not be replaced by other's value."""
        base = Theme()
        base.canvas = [{'background': 'white'}]

        override = Theme()
        override.canvas = [{'background': 'black'}]
        override.copy_from(other=base)
        # The existing 'background' in override should be kept, not duplicated
        backgrounds = [e for e in override.canvas
                       if isinstance(e, dict) and 'background' in e]
        assert len(backgrounds) == 1
        assert backgrounds[0]['background'] == 'black'

    def test_copy_from_dict_keys_fix(self):
        """
        Regression for Phase-1 bug: iterating dict CSS entries used
        css.keys()[0] which fails in Python 3.  Verify copy_from works
        with dict-valued CSS entries (exercises next(iter(css.keys()))).
        """
        base = Theme()
        base.canvas = [{'background': 'white'}, {'color': 'black'}]

        override = Theme()
        # Should not raise TypeError about subscripting dict_keys
        override.copy_from(other=base)
        assert len(override.canvas) == 2
