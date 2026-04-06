"""
Unit tests for backends/base.py — DecoratorSpec and parse_layout_decorators().
"""

import pytest

from matisse.backends.base import DecoratorSpec, parse_layout_decorators


# ---------------------------------------------------------------------------
# DecoratorSpec dataclass
# ---------------------------------------------------------------------------


class TestDecoratorSpec:
    def test_fields_stored(self):
        spec = DecoratorSpec(
            name="header-1",
            kind="header",
            size="8%",
            position="",
            css={"background": "#000"},
            metadata={"slidetitle": "float:left;"},
            active=True,
        )
        assert spec.name == "header-1"
        assert spec.kind == "header"
        assert spec.size == "8%"
        assert spec.position == ""
        assert spec.css == {"background": "#000"}
        assert spec.metadata == {"slidetitle": "float:left;"}
        assert spec.active is True

    def test_defaults(self):
        spec = DecoratorSpec(name="footer-1", kind="footer", size="5%", position="")
        assert spec.css == {}
        assert spec.metadata == {}
        assert spec.active is True


# ---------------------------------------------------------------------------
# parse_layout_decorators — edge cases
# ---------------------------------------------------------------------------


class TestParseLayoutDecoratorsEdgeCases:
    def test_empty_dict_returns_empty(self):
        assert parse_layout_decorators({}) == []

    def test_none_returns_empty(self):
        assert parse_layout_decorators(None) == []

    def test_non_dict_returns_empty(self):
        assert parse_layout_decorators("bad") == []

    def test_slide_key_ignored(self):
        layout = {"slide": {"width": "960", "height": "700"}}
        assert parse_layout_decorators(layout) == []

    def test_content_key_ignored(self):
        layout = {"content": {"padding": "10px"}}
        assert parse_layout_decorators(layout) == []

    def test_unknown_key_ignored(self):
        layout = {"canvas": {"background": "blue"}}
        assert parse_layout_decorators(layout) == []

    def test_decorator_with_empty_val_ignored(self):
        layout = {"header-1": None}
        assert parse_layout_decorators(layout) == []

    def test_decorator_with_non_dict_val_ignored(self):
        layout = {"header-1": "bad value"}
        assert parse_layout_decorators(layout) == []


# ---------------------------------------------------------------------------
# parse_layout_decorators — header
# ---------------------------------------------------------------------------


class TestParseHeader:
    def test_single_header(self):
        layout = {"header-1": {"height": "8%", "background": "#1a1a2e", "color": "white"}}
        specs = parse_layout_decorators(layout)
        assert len(specs) == 1
        s = specs[0]
        assert s.name == "header-1"
        assert s.kind == "header"
        assert s.size == "8%"
        assert s.position == ""
        assert s.active is True
        assert s.css == {"background": "#1a1a2e", "color": "white"}

    def test_header_default_height(self):
        layout = {"header-1": {"color": "white"}}
        specs = parse_layout_decorators(layout)
        assert specs[0].size == "10%"

    def test_header_metadata(self):
        layout = {
            "header-1": {
                "height": "8%",
                "metadata": {
                    "slidetitle": {"float": "left", "font-size": "0.9em"},
                    "slidenumber": {"float": "right"},
                },
            }
        }
        specs = parse_layout_decorators(layout)
        s = specs[0]
        assert "slidetitle" in s.metadata
        assert "slidenumber" in s.metadata
        assert "float:left;" in s.metadata["slidetitle"]
        assert "font-size:0.9em;" in s.metadata["slidetitle"]
        assert s.metadata["slidenumber"] == "float:right;"

    def test_header_scalar_metadata(self):
        layout = {"header-1": {"metadata": {"toc": 1}}}
        specs = parse_layout_decorators(layout)
        assert specs[0].metadata["toc"] == "1"

    def test_header_none_metadata_value(self):
        layout = {"header-1": {"metadata": {"toc": None}}}
        specs = parse_layout_decorators(layout)
        assert specs[0].metadata["toc"] == ""

    def test_header_active_false(self):
        layout = {"header-1": {"height": "8%", "active": False}}
        specs = parse_layout_decorators(layout)
        assert specs[0].active is False

    def test_header_active_no(self):
        layout = {"header-1": {"height": "8%", "active": "no"}}
        specs = parse_layout_decorators(layout)
        assert specs[0].active is False

    def test_header_active_yes(self):
        layout = {"header-1": {"height": "8%", "active": "yes"}}
        specs = parse_layout_decorators(layout)
        assert specs[0].active is True

    def test_structural_keys_not_in_css(self):
        layout = {
            "header-1": {
                "height": "8%",
                "active": True,
                "metadata": {},
                "position": "L",
                "width": "20%",
                "background": "#000",
            }
        }
        specs = parse_layout_decorators(layout)
        assert "height" not in specs[0].css
        assert "active" not in specs[0].css
        assert "metadata" not in specs[0].css
        assert "position" not in specs[0].css
        assert "width" not in specs[0].css
        assert specs[0].css == {"background": "#000"}


# ---------------------------------------------------------------------------
# parse_layout_decorators — footer
# ---------------------------------------------------------------------------


class TestParseFooter:
    def test_single_footer(self):
        layout = {"footer-1": {"height": "4%", "background": "#000"}}
        specs = parse_layout_decorators(layout)
        assert len(specs) == 1
        assert specs[0].kind == "footer"
        assert specs[0].size == "4%"

    def test_footer_default_height(self):
        # Empty dict is falsy and filtered out by parse_layout_decorators
        layout = {"footer-1": {"color": "white"}}
        specs = parse_layout_decorators(layout)
        assert specs[0].size == "10%"


# ---------------------------------------------------------------------------
# parse_layout_decorators — sidebar
# ---------------------------------------------------------------------------


class TestParseSidebar:
    def test_sidebar_left(self):
        layout = {"sidebar-1": {"position": "L", "width": "20%", "background": "#abc"}}
        specs = parse_layout_decorators(layout)
        assert len(specs) == 1
        s = specs[0]
        assert s.kind == "sidebar"
        assert s.size == "20%"
        assert s.position == "L"
        assert s.css == {"background": "#abc"}

    def test_sidebar_right(self):
        layout = {"sidebar-1": {"position": "R", "width": "15%"}}
        specs = parse_layout_decorators(layout)
        assert specs[0].position == "R"

    def test_sidebar_position_uppercased(self):
        layout = {"sidebar-1": {"position": "l", "width": "20%"}}
        specs = parse_layout_decorators(layout)
        assert specs[0].position == "L"

    def test_sidebar_default_position(self):
        layout = {"sidebar-1": {"width": "15%"}}
        specs = parse_layout_decorators(layout)
        assert specs[0].position == "R"

    def test_sidebar_default_width(self):
        layout = {"sidebar-1": {"background": "blue"}}
        specs = parse_layout_decorators(layout)
        assert specs[0].size == "10%"


# ---------------------------------------------------------------------------
# parse_layout_decorators — sorting and multiple decorators
# ---------------------------------------------------------------------------


class TestParseMultipleDecorators:
    def test_sorted_by_name(self):
        layout = {
            "footer-1": {"height": "5%"},
            "header-2": {"height": "4%"},
            "header-1": {"height": "8%"},
            "sidebar-1": {"position": "L", "width": "20%"},
        }
        specs = parse_layout_decorators(layout)
        names = [s.name for s in specs]
        assert names == sorted(names)

    def test_multiple_headers(self):
        layout = {
            "header-3": {"height": "3%"},
            "header-1": {"height": "8%"},
            "header-2": {"height": "5%"},
        }
        specs = parse_layout_decorators(layout)
        assert [s.name for s in specs] == ["header-1", "header-2", "header-3"]

    def test_mixed_decorator_types(self):
        layout = {
            "header-1": {"height": "8%"},
            "footer-1": {"height": "4%"},
            "sidebar-1": {"position": "L", "width": "20%"},
            "slide": {"width": "960"},  # ignored
        }
        specs = parse_layout_decorators(layout)
        assert len(specs) == 3
        kinds = {s.kind for s in specs}
        assert kinds == {"header", "footer", "sidebar"}
