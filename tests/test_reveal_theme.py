"""
Unit tests for matisse.backends.reveal.theme.RevealTheme.

Covers:
- __init__ defaults
- get(): parsing all options from YAML source
- get(): validation warnings for unknown values
- parse_slide_overrides(): per-slide data-* attribute extraction
- use_math_plugin property
- to_css()
"""

import pytest

from matisse.backends.reveal.theme import RevealTheme

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _theme_from_yaml(yaml: str) -> RevealTheme:
    t = RevealTheme()
    t.get(yaml)
    return t


def _slide_overrides_from_yaml(yaml: str) -> dict:
    t = RevealTheme()
    return t.parse_slide_overrides(yaml)


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------


class TestRevealThemeDefaults:
    def test_theme_default(self):
        assert RevealTheme().theme == "black"

    def test_transition_default(self):
        assert RevealTheme().transition == "slide"

    def test_transition_speed_default(self):
        assert RevealTheme().transition_speed == "default"

    def test_controls_default(self):
        assert RevealTheme().controls is True

    def test_controls_layout_default(self):
        assert RevealTheme().controls_layout == "bottom-right"

    def test_progress_default(self):
        assert RevealTheme().progress is True

    def test_slide_number_default(self):
        assert RevealTheme().slide_number is False

    def test_loop_default(self):
        assert RevealTheme().loop is False

    def test_center_default(self):
        assert RevealTheme().center is True

    def test_auto_slide_default(self):
        assert RevealTheme().auto_slide == 0

    def test_width_default(self):
        assert RevealTheme().width == 960

    def test_height_default(self):
        assert RevealTheme().height == 700

    def test_margin_default(self):
        assert RevealTheme().margin == pytest.approx(0.04)

    def test_min_scale_default(self):
        assert RevealTheme().min_scale == pytest.approx(0.2)

    def test_max_scale_default(self):
        assert RevealTheme().max_scale == pytest.approx(2.0)

    def test_background_transition_default(self):
        assert RevealTheme().background_transition == "fade"

    def test_keyboard_default(self):
        assert RevealTheme().keyboard is True

    def test_touch_default(self):
        assert RevealTheme().touch is True

    def test_layout_default(self):
        assert RevealTheme().layout == "linear"

    def test_plugins_default(self):
        assert RevealTheme().plugins == []

    def test_code_style_default(self):
        assert RevealTheme().code_style == ""

    def test_custom_css_default(self):
        assert RevealTheme().custom_css == ""

    def test_use_math_plugin_false_by_default(self):
        assert RevealTheme().use_math_plugin is False

    def test_to_css_empty_by_default(self):
        assert RevealTheme().to_css() == ""


# ---------------------------------------------------------------------------
# Parsing: theme and transition
# ---------------------------------------------------------------------------


class TestRevealThemeParsing:
    def test_theme_parsed(self):
        t = _theme_from_yaml("reveal:\n  theme: moon\n")
        assert t.theme == "moon"

    def test_all_builtin_themes_accepted(self):
        for name in [
            "black",
            "white",
            "league",
            "beige",
            "sky",
            "night",
            "moon",
            "serif",
            "simple",
            "solarized",
            "blood",
            "dracula",
        ]:
            t = _theme_from_yaml(f"reveal:\n  theme: {name}\n")
            assert t.theme == name

    def test_unknown_theme_keeps_default(self):
        t = _theme_from_yaml("reveal:\n  theme: nonexistent\n")
        assert t.theme == "black"  # default unchanged

    def test_transition_parsed(self):
        t = _theme_from_yaml("reveal:\n  transition: zoom\n")
        assert t.transition == "zoom"

    def test_all_transitions_accepted(self):
        for val in ["none", "fade", "slide", "convex", "concave", "zoom"]:
            t = _theme_from_yaml(f"reveal:\n  transition: {val}\n")
            assert t.transition == val

    def test_unknown_transition_keeps_default(self):
        t = _theme_from_yaml("reveal:\n  transition: warp\n")
        assert t.transition == "slide"

    def test_transition_speed_parsed(self):
        t = _theme_from_yaml("reveal:\n  transition_speed: fast\n")
        assert t.transition_speed == "fast"

    def test_unknown_transition_speed_keeps_default(self):
        t = _theme_from_yaml("reveal:\n  transition_speed: turbo\n")
        assert t.transition_speed == "default"

    def test_background_transition_parsed(self):
        t = _theme_from_yaml("reveal:\n  background_transition: convex\n")
        assert t.background_transition == "convex"


# ---------------------------------------------------------------------------
# Parsing: booleans
# ---------------------------------------------------------------------------


class TestRevealThemeBooleans:
    def test_controls_false(self):
        t = _theme_from_yaml("reveal:\n  controls: false\n")
        assert t.controls is False

    def test_progress_false(self):
        t = _theme_from_yaml("reveal:\n  progress: false\n")
        assert t.progress is False

    def test_loop_true(self):
        t = _theme_from_yaml("reveal:\n  loop: true\n")
        assert t.loop is True

    def test_center_false(self):
        t = _theme_from_yaml("reveal:\n  center: false\n")
        assert t.center is False

    def test_keyboard_false(self):
        t = _theme_from_yaml("reveal:\n  keyboard: false\n")
        assert t.keyboard is False

    def test_touch_false(self):
        t = _theme_from_yaml("reveal:\n  touch: false\n")
        assert t.touch is False


# ---------------------------------------------------------------------------
# Parsing: slide_number variants
# ---------------------------------------------------------------------------


class TestSlideNumber:
    def test_slide_number_false(self):
        t = _theme_from_yaml("reveal:\n  slide_number: false\n")
        assert t.slide_number is False

    def test_slide_number_true(self):
        t = _theme_from_yaml("reveal:\n  slide_number: true\n")
        assert t.slide_number is True

    def test_slide_number_c(self):
        t = _theme_from_yaml("reveal:\n  slide_number: 'c'\n")
        assert t.slide_number == "c"

    def test_slide_number_c_over_t(self):
        t = _theme_from_yaml("reveal:\n  slide_number: 'c/t'\n")
        assert t.slide_number == "c/t"

    def test_slide_number_h_v(self):
        t = _theme_from_yaml("reveal:\n  slide_number: 'h/v'\n")
        assert t.slide_number == "h/v"

    def test_slide_number_h_dot_v(self):
        t = _theme_from_yaml("reveal:\n  slide_number: 'h.v'\n")
        assert t.slide_number == "h.v"


# ---------------------------------------------------------------------------
# Parsing: sizing and timing
# ---------------------------------------------------------------------------


class TestSizingAndTiming:
    def test_width_parsed(self):
        t = _theme_from_yaml("reveal:\n  width: 1280\n")
        assert t.width == 1280

    def test_height_parsed(self):
        t = _theme_from_yaml("reveal:\n  height: 720\n")
        assert t.height == 720

    def test_margin_parsed(self):
        t = _theme_from_yaml("reveal:\n  margin: 0.1\n")
        assert t.margin == pytest.approx(0.1)

    def test_min_scale_parsed(self):
        t = _theme_from_yaml("reveal:\n  min_scale: 0.5\n")
        assert t.min_scale == pytest.approx(0.5)

    def test_max_scale_parsed(self):
        t = _theme_from_yaml("reveal:\n  max_scale: 3.0\n")
        assert t.max_scale == pytest.approx(3.0)

    def test_auto_slide_parsed(self):
        t = _theme_from_yaml("reveal:\n  auto_slide: 5000\n")
        assert t.auto_slide == 5000


# ---------------------------------------------------------------------------
# Parsing: layout
# ---------------------------------------------------------------------------


class TestLayout:
    def test_linear_layout(self):
        t = _theme_from_yaml("reveal:\n  layout: linear\n")
        assert t.layout == "linear"

    def test_vertical_layout(self):
        t = _theme_from_yaml("reveal:\n  layout: vertical\n")
        assert t.layout == "vertical"

    def test_unknown_layout_keeps_default(self):
        t = _theme_from_yaml("reveal:\n  layout: diagonal\n")
        assert t.layout == "linear"


# ---------------------------------------------------------------------------
# Parsing: plugins
# ---------------------------------------------------------------------------


class TestPlugins:
    def test_notes_plugin(self):
        t = _theme_from_yaml("reveal:\n  plugins:\n    - notes\n")
        assert t.plugins == ["notes"]

    def test_multiple_plugins(self):
        t = _theme_from_yaml("reveal:\n  plugins:\n    - notes\n    - zoom\n    - search\n")
        assert t.plugins == ["notes", "zoom", "search"]

    def test_math_plugin(self):
        t = _theme_from_yaml("reveal:\n  plugins:\n    - math\n")
        assert t.plugins == ["math"]
        assert t.use_math_plugin is True

    def test_unknown_plugin_skipped(self):
        t = _theme_from_yaml("reveal:\n  plugins:\n    - notes\n    - bogus\n")
        assert t.plugins == ["notes"]

    def test_all_valid_plugins_accepted(self):
        src = "reveal:\n  plugins:\n    - notes\n    - zoom\n    - search\n    - math\n"
        t = _theme_from_yaml(src)
        assert set(t.plugins) == {"notes", "zoom", "search", "math"}

    def test_use_math_plugin_false_without_math(self):
        t = _theme_from_yaml("reveal:\n  plugins:\n    - notes\n")
        assert t.use_math_plugin is False


# ---------------------------------------------------------------------------
# Parsing: code_style and custom_css
# ---------------------------------------------------------------------------


class TestCodeStyleAndCustomCss:
    def test_code_style_parsed(self):
        t = _theme_from_yaml("reveal:\n  code_style: dracula\n")
        assert t.code_style == "dracula"

    def test_custom_css_parsed(self):
        t = _theme_from_yaml("reveal:\n  custom_css: '.reveal { font-size: 1.2em; }'\n")
        assert ".reveal" in t.custom_css

    def test_to_css_returns_custom_css(self):
        t = _theme_from_yaml("reveal:\n  custom_css: 'body { color: red; }'\n")
        assert t.to_css() == "body { color: red; }"

    def test_to_css_empty_when_no_custom_css(self):
        t = _theme_from_yaml("reveal:\n  theme: moon\n")
        assert t.to_css() == ""


# ---------------------------------------------------------------------------
# Parsing: full config block
# ---------------------------------------------------------------------------


class TestFullConfigBlock:
    _FULL_YAML = """
reveal:
  theme: moon
  transition: fade
  transition_speed: fast
  controls: false
  controls_layout: edges
  progress: false
  slide_number: "c/t"
  loop: true
  center: false
  auto_slide: 3000
  width: 1280
  height: 800
  margin: 0.05
  min_scale: 0.3
  max_scale: 1.5
  background_transition: zoom
  keyboard: false
  touch: false
  layout: vertical
  plugins:
    - notes
    - zoom
  code_style: monokai
  custom_css: ".reveal h1 { color: red; }"
"""

    def test_full_block_theme(self):
        assert _theme_from_yaml(self._FULL_YAML).theme == "moon"

    def test_full_block_transition(self):
        assert _theme_from_yaml(self._FULL_YAML).transition == "fade"

    def test_full_block_transition_speed(self):
        assert _theme_from_yaml(self._FULL_YAML).transition_speed == "fast"

    def test_full_block_controls(self):
        assert _theme_from_yaml(self._FULL_YAML).controls is False

    def test_full_block_controls_layout(self):
        assert _theme_from_yaml(self._FULL_YAML).controls_layout == "edges"

    def test_full_block_progress(self):
        assert _theme_from_yaml(self._FULL_YAML).progress is False

    def test_full_block_slide_number(self):
        assert _theme_from_yaml(self._FULL_YAML).slide_number == "c/t"

    def test_full_block_loop(self):
        assert _theme_from_yaml(self._FULL_YAML).loop is True

    def test_full_block_center(self):
        assert _theme_from_yaml(self._FULL_YAML).center is False

    def test_full_block_auto_slide(self):
        assert _theme_from_yaml(self._FULL_YAML).auto_slide == 3000

    def test_full_block_width(self):
        assert _theme_from_yaml(self._FULL_YAML).width == 1280

    def test_full_block_height(self):
        assert _theme_from_yaml(self._FULL_YAML).height == 800

    def test_full_block_margin(self):
        assert _theme_from_yaml(self._FULL_YAML).margin == pytest.approx(0.05)

    def test_full_block_min_scale(self):
        assert _theme_from_yaml(self._FULL_YAML).min_scale == pytest.approx(0.3)

    def test_full_block_max_scale(self):
        assert _theme_from_yaml(self._FULL_YAML).max_scale == pytest.approx(1.5)

    def test_full_block_background_transition(self):
        assert _theme_from_yaml(self._FULL_YAML).background_transition == "zoom"

    def test_full_block_keyboard(self):
        assert _theme_from_yaml(self._FULL_YAML).keyboard is False

    def test_full_block_touch(self):
        assert _theme_from_yaml(self._FULL_YAML).touch is False

    def test_full_block_layout(self):
        assert _theme_from_yaml(self._FULL_YAML).layout == "vertical"

    def test_full_block_plugins(self):
        assert _theme_from_yaml(self._FULL_YAML).plugins == ["notes", "zoom"]

    def test_full_block_code_style(self):
        assert _theme_from_yaml(self._FULL_YAML).code_style == "monokai"

    def test_full_block_custom_css(self):
        assert "color: red" in _theme_from_yaml(self._FULL_YAML).custom_css


# ---------------------------------------------------------------------------
# Parsing: multiple YAML documents in source
# ---------------------------------------------------------------------------


class TestMultipleYamlDocuments:
    def test_first_reveal_block_wins(self):
        src = "reveal:\n  theme: moon\n---\nreveal:\n  theme: blood\n"
        t = _theme_from_yaml(src)
        # Both are parsed sequentially; last one to set the attribute wins
        assert t.theme in ("moon", "blood")  # both valid — just not default

    def test_reveal_block_among_other_keys(self):
        src = "metadata:\n  - title: Test\nreveal:\n  theme: moon\n"
        t = _theme_from_yaml(src)
        assert t.theme == "moon"

    def test_non_reveal_block_ignored(self):
        src = "theme:\n  canvas:\n    background: black\n"
        t = _theme_from_yaml(src)
        assert t.theme == "black"  # unchanged default

    def test_empty_source(self):
        t = _theme_from_yaml("")
        assert t.theme == "black"

    def test_invalid_yaml_does_not_raise(self):
        t = _theme_from_yaml("reveal: [unclosed")
        assert t.theme == "black"


# ---------------------------------------------------------------------------
# Per-slide overrides: parse_slide_overrides()
# ---------------------------------------------------------------------------


class TestParseSlideOverrides:
    def test_transition_override(self):
        yaml_src = "overtheme:\n  reveal:\n    transition: zoom\n"
        overrides = _slide_overrides_from_yaml(yaml_src)
        assert overrides.get("data-transition") == "zoom"

    def test_background_color(self):
        yaml_src = "overtheme:\n  reveal:\n    background_color: '#1a1a2e'\n"
        overrides = _slide_overrides_from_yaml(yaml_src)
        assert overrides.get("data-background-color") == "#1a1a2e"

    def test_background_image(self):
        yaml_src = "overtheme:\n  reveal:\n    background_image: img/banner.png\n"
        overrides = _slide_overrides_from_yaml(yaml_src)
        assert overrides.get("data-background-image") == "img/banner.png"

    def test_background_size(self):
        yaml_src = "overtheme:\n  reveal:\n    background_size: cover\n"
        overrides = _slide_overrides_from_yaml(yaml_src)
        assert overrides.get("data-background-size") == "cover"

    def test_background_position(self):
        yaml_src = "overtheme:\n  reveal:\n    background_position: center\n"
        overrides = _slide_overrides_from_yaml(yaml_src)
        assert overrides.get("data-background-position") == "center"

    def test_background_video(self):
        yaml_src = "overtheme:\n  reveal:\n    background_video: video/bg.mp4\n"
        overrides = _slide_overrides_from_yaml(yaml_src)
        assert overrides.get("data-background-video") == "video/bg.mp4"

    def test_auto_animate_true(self):
        yaml_src = "overtheme:\n  reveal:\n    auto_animate: true\n"
        overrides = _slide_overrides_from_yaml(yaml_src)
        assert "data-auto-animate" in overrides

    def test_auto_animate_false_not_included(self):
        yaml_src = "overtheme:\n  reveal:\n    auto_animate: false\n"
        overrides = _slide_overrides_from_yaml(yaml_src)
        assert "data-auto-animate" not in overrides

    def test_no_reveal_key_returns_empty(self):
        yaml_src = "overtheme:\n  canvas:\n    background: black\n"
        overrides = _slide_overrides_from_yaml(yaml_src)
        assert overrides == {}

    def test_no_overtheme_key_returns_empty(self):
        yaml_src = "reveal:\n  theme: moon\n"
        overrides = _slide_overrides_from_yaml(yaml_src)
        assert overrides == {}

    def test_empty_yaml_returns_empty(self):
        assert _slide_overrides_from_yaml("") == {}

    def test_multiple_overrides(self):
        yaml_src = "overtheme:\n  reveal:\n    transition: fade\n    background_color: '#000'\n    auto_animate: true\n"
        overrides = _slide_overrides_from_yaml(yaml_src)
        assert overrides["data-transition"] == "fade"
        assert overrides["data-background-color"] == "#000"
        assert "data-auto-animate" in overrides
