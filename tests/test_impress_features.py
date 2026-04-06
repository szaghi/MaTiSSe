"""
Tests for impress.js features implemented in issues #51–#61.

Covers:
- #51  data-max-scale / data-min-scale on <div id="impress">
- #52  per-slide data-transition-duration
- #53  skip and stop CSS classes on slides
- #54  $substep / $endsubstep environment
- #55  $note → <div class="notes"> for impress (Presenter Console)
- #56  global and per-slide data-autoplay / data-autoplay-repeat
- #57  relative positioning (data-rel-x/y/z, data-rel-to, …)
- #58  Goto plugin (data-goto-next, data-goto-prev, …)
- #59  progress bar, help popup, navigation toolbar HTML elements
- #60  media plugin (data-media-autoplay/autostop/autopause)
- #61  data-rotate-order per slide
"""

from matisse.backends.impress.theme import ImpressTheme as Theme
from matisse.matisse_config import MatisseConfig
from matisse.note import Note
from matisse.presentation import Presentation
from matisse.substep import Substep

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _theme_from_yaml(yaml: str) -> Theme:
    """Parse a ``theme:`` YAML block into an ImpressTheme."""
    t = Theme()
    t.get(yaml)
    return t


def _overtheme_from_yaml(yaml: str) -> Theme:
    """Parse an ``overtheme:`` YAML block into an ImpressTheme."""
    t = Theme()
    t.get(yaml, name="overtheme")
    return t


def _rendered_html(source: str) -> str:
    """Parse *source* and return the rendered impress HTML string."""
    config = MatisseConfig()
    p = Presentation()
    p.parse(config=config, source=source)
    return p.to_html(config=config)


_BASE_SOURCE = """\
---
metadata:
  - title: "Test"
---
# Chapter
## Section
### Subsection
"""


def _slide_source(overtheme_yaml: str = "", content: str = "") -> str:
    lines = [_BASE_SOURCE, "#### Slide"]
    if overtheme_yaml:
        lines.append("---")
        lines.append("overtheme:")
        for line in overtheme_yaml.strip().splitlines():
            lines.append("  " + line)
        lines.append("---")
    if content:
        lines.append(content)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# #51 — data-max-scale / data-min-scale
# ---------------------------------------------------------------------------


class TestMaxMinScale:
    def test_max_scale_parsed(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    max-scale: 2")
        assert t.max_scale == 2

    def test_min_scale_parsed(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    min-scale: 0.5")
        assert t.min_scale == 0.5

    def test_max_scale_default_is_none(self):
        assert Theme().max_scale is None

    def test_min_scale_default_is_none(self):
        assert Theme().min_scale is None

    def test_max_scale_emitted_in_html(self):
        source = _BASE_SOURCE + "#### Slide\n"
        source = (
            "---\nmetadata:\n  - title: Test\ntheme:\n  canvas:\n    max-scale: 2\n---\n"
            + "# Chapter\n## Section\n### Subsection\n#### Slide\n"
        )
        html = _rendered_html(source)
        assert 'data-max-scale="2"' in html

    def test_min_scale_emitted_in_html(self):
        source = (
            "---\nmetadata:\n  - title: Test\ntheme:\n  canvas:\n    min-scale: 0.5\n---\n"
            + "# Chapter\n## Section\n### Subsection\n#### Slide\n"
        )
        html = _rendered_html(source)
        assert 'data-min-scale="0.5"' in html

    def test_neither_scale_omits_attributes(self):
        source = _BASE_SOURCE + "#### Slide\n"
        html = _rendered_html(source)
        assert "data-max-scale" not in html
        assert "data-min-scale" not in html

    def test_canvas_emits_data_width_and_height(self):
        html = _rendered_html(_BASE_SOURCE + "#### Slide\n")
        assert "data-width=" in html
        assert "data-height=" in html


# ---------------------------------------------------------------------------
# #52 — per-slide data-transition-duration
# ---------------------------------------------------------------------------


class TestTransitionDuration:
    def test_parsed_from_overtheme(self):
        t = _overtheme_from_yaml("overtheme:\n  slide:\n    transition-duration: 300")
        assert t.transition_duration == 300

    def test_default_is_none(self):
        assert Theme().transition_duration is None

    def test_emitted_on_slide(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  transition-duration: 300"))
        assert 'data-transition-duration="300"' in html

    def test_omitted_when_not_set(self):
        html = _rendered_html(_slide_source())
        assert "data-transition-duration" not in html


# ---------------------------------------------------------------------------
# #53 — skip and stop navigation classes
# ---------------------------------------------------------------------------


class TestSkipStop:
    def test_skip_parsed_from_overtheme(self):
        t = _overtheme_from_yaml("overtheme:\n  slide:\n    skip: true")
        assert t.skip is True

    def test_stop_parsed_from_overtheme(self):
        t = _overtheme_from_yaml("overtheme:\n  slide:\n    stop: true")
        assert t.stop is True

    def test_skip_default_is_false(self):
        assert Theme().skip is False

    def test_stop_default_is_false(self):
        assert Theme().stop is False

    def test_skip_class_in_html(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  skip: true"))
        assert 'class="step slide skip"' in html

    def test_stop_class_in_html(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  stop: true"))
        assert 'class="step slide stop"' in html

    def test_both_skip_and_stop(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  skip: true\n  stop: true"))
        assert "skip" in html
        assert "stop" in html

    def test_no_extra_class_without_overtheme(self):
        html = _rendered_html(_slide_source())
        assert 'class="step slide"' in html


# ---------------------------------------------------------------------------
# #54 — $substep / $endsubstep environment
# ---------------------------------------------------------------------------


class TestSubstep:
    def test_basic_to_html(self):
        s = Substep(source="$substep\nFirst point\n$endsubstep")
        html = s.to_html()
        assert 'class="substep"' in html
        assert "First point" in html

    def test_order_attribute(self):
        s = Substep(source="$substep[order:2]\nContent\n$endsubstep")
        html = s.to_html()
        assert 'data-substep-order="2"' in html

    def test_no_order_attribute_by_default(self):
        s = Substep(source="$substep\nContent\n$endsubstep")
        html = s.to_html()
        assert "data-substep-order" not in html

    def test_substep_in_slide(self):
        source = _slide_source(content="$substep\nRevealed content\n$endsubstep")
        html = _rendered_html(source)
        assert 'class="substep"' in html
        assert "Revealed content" in html

    def test_substep_reset(self):
        Substep.substeps_number = 5
        Substep.reset()
        assert Substep.substeps_number == 0


# ---------------------------------------------------------------------------
# #55 — $note → presenter console
# ---------------------------------------------------------------------------


class TestNotePresenterConsole:
    def test_impress_default_emits_notes_div(self):
        n = Note(source="$note\n$content{Speaker text}\n$endnote")
        html = n.to_html(backend="impress")
        assert 'class="notes"' in html
        assert "Speaker text" in html

    def test_impress_visible_style_emits_note_box(self):
        n = Note(source="$note\n$content{Speaker text}\n$endnote")
        html = n.to_html(backend="impress", notes_style="visible")
        assert 'class="note"' in html

    def test_reveal_still_emits_aside_notes(self):
        n = Note(source="$note\n$content{Speaker text}\n$endnote")
        html = n.to_html(backend="reveal")
        assert '<aside class="notes">' in html

    def test_notes_style_canvas_option(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    notes-style: visible")
        assert t.notes_style == "visible"

    def test_notes_style_default_is_console(self):
        assert Theme().notes_style == "console"

    def test_notes_in_rendered_presentation(self):
        source = _slide_source(content="$note\n$content{My note}\n$endnote")
        html = _rendered_html(source)
        assert 'class="notes"' in html

    def test_visible_notes_in_rendered_presentation(self):
        source = (
            "---\nmetadata:\n  - title: Test\ntheme:\n  canvas:\n    notes-style: visible\n---\n"
            "# Chapter\n## Section\n### Subsection\n#### Slide\n"
            "$note\n$content{My note}\n$endnote\n"
        )
        html = _rendered_html(source)
        assert 'class="note"' in html


# ---------------------------------------------------------------------------
# #56 — autoplay plugin
# ---------------------------------------------------------------------------


class TestAutoplay:
    def test_global_autoplay_parsed(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    autoplay: 5")
        assert t.canvas_autoplay == 5

    def test_autoplay_repeat_parsed(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    autoplay-repeat: true")
        assert t.autoplay_repeat is True

    def test_global_autoplay_emitted(self):
        source = (
            "---\nmetadata:\n  - title: Test\ntheme:\n  canvas:\n    autoplay: 5\n---\n"
            "# Chapter\n## Section\n### Subsection\n#### Slide\n"
        )
        html = _rendered_html(source)
        assert 'data-autoplay="5"' in html

    def test_autoplay_repeat_emitted(self):
        source = (
            "---\nmetadata:\n  - title: Test\ntheme:\n  canvas:\n    autoplay-repeat: true\n---\n"
            "# Chapter\n## Section\n### Subsection\n#### Slide\n"
        )
        html = _rendered_html(source)
        assert 'data-autoplay-repeat="true"' in html

    def test_global_autoplay_omitted_when_none(self):
        html = _rendered_html(_BASE_SOURCE + "#### Slide\n")
        assert "data-autoplay-repeat" not in html

    def test_per_slide_autoplay(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  autoplay: 10"))
        assert 'data-autoplay="10"' in html

    def test_per_slide_autoplay_default_is_none(self):
        assert Theme().slide_autoplay is None


# ---------------------------------------------------------------------------
# #57 — relative positioning
# ---------------------------------------------------------------------------


class TestRelativePositioning:
    def test_rel_x_parsed(self):
        t = _overtheme_from_yaml("overtheme:\n  slide:\n    rel-x: 1000")
        assert t.rel_x == "1000"

    def test_rel_x_string_preserved(self):
        t = _overtheme_from_yaml("overtheme:\n  slide:\n    rel-x: '1w'")
        assert t.rel_x == "1w"

    def test_rel_to_parsed(self):
        t = _overtheme_from_yaml("overtheme:\n  slide:\n    rel-to: slide-5")
        assert t.rel_to == "slide-5"

    def test_rel_x_emitted(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  rel-x: 1000"))
        assert 'data-rel-x="1000"' in html

    def test_rel_to_emitted(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  rel-x: 500\n  rel-to: slide-1"))
        assert 'data-rel-to="slide-1"' in html

    def test_absolute_position_when_no_rel(self):
        html = _rendered_html(_slide_source())
        assert "data-x=" in html
        assert "data-rel-x" not in html

    def test_rel_reset_emitted(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  rel-x: 0\n  rel-reset: true"))
        assert 'data-rel-reset="true"' in html

    def test_rel_position_emitted(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  rel-x: 0\n  rel-position: absolute"))
        assert 'data-rel-position="absolute"' in html


# ---------------------------------------------------------------------------
# #58 — Goto plugin
# ---------------------------------------------------------------------------


class TestGotoPlugin:
    def test_goto_next_parsed(self):
        t = _overtheme_from_yaml("overtheme:\n  slide:\n    goto-next: slide-5")
        assert t.goto_next == "slide-5"

    def test_goto_prev_parsed(self):
        t = _overtheme_from_yaml("overtheme:\n  slide:\n    goto-prev: slide-1")
        assert t.goto_prev == "slide-1"

    def test_goto_parsed(self):
        t = _overtheme_from_yaml("overtheme:\n  slide:\n    goto: slide-overview")
        assert t.goto == "slide-overview"

    def test_goto_next_emitted(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  goto-next: slide-3"))
        assert 'data-goto-next="slide-3"' in html

    def test_goto_prev_emitted(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  goto-prev: slide-1"))
        assert 'data-goto-prev="slide-1"' in html

    def test_goto_omitted_when_empty(self):
        html = _rendered_html(_slide_source())
        assert "data-goto" not in html

    def test_goto_key_list_and_next_list(self):
        html = _rendered_html(
            _slide_source(overtheme_yaml="slide:\n  goto-key-list: 'KeyA KeyB'\n  goto-next-list: 'slide-2 slide-3'")
        )
        assert "data-goto-key-list" in html
        assert "data-goto-next-list" in html


# ---------------------------------------------------------------------------
# #59 — progress bar, help popup, navigation toolbar
# ---------------------------------------------------------------------------


class TestUIElements:
    def _source_with_canvas(self, canvas_yaml: str) -> str:
        return (
            f"---\nmetadata:\n  - title: Test\ntheme:\n  canvas:\n{canvas_yaml}\n---\n"
            "# Chapter\n## Section\n### Subsection\n#### Slide\n"
        )

    def test_progress_bar_flag_parsed(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    show-progress-bar: true")
        assert t.show_progress_bar is True

    def test_help_popup_flag_parsed(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    show-help-popup: true")
        assert t.show_help_popup is True

    def test_navigation_toolbar_flag_parsed(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    show-navigation-toolbar: true")
        assert t.show_navigation_toolbar is True

    def test_progress_counter_flag_parsed(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    show-progress-counter: true")
        assert t.show_progress_counter is True

    def test_progress_bar_emitted(self):
        html = _rendered_html(self._source_with_canvas("    show-progress-bar: true"))
        assert 'class="impress-progressbar"' in html

    def test_progress_counter_emitted(self):
        html = _rendered_html(self._source_with_canvas("    show-progress-counter: true"))
        assert 'class="impress-progress"' in html

    def test_help_popup_emitted(self):
        html = _rendered_html(self._source_with_canvas("    show-help-popup: true"))
        assert 'id="impress-help"' in html

    def test_navigation_toolbar_emitted(self):
        html = _rendered_html(self._source_with_canvas("    show-navigation-toolbar: true"))
        assert 'id="impress-toolbar"' in html

    def test_no_ui_elements_by_default(self):
        html = _rendered_html(_BASE_SOURCE + "#### Slide\n")
        assert "impress-progressbar" not in html
        assert "impress-progress" not in html
        assert "impress-help" not in html
        assert "impress-toolbar" not in html

    def test_all_flags_default_false(self):
        t = Theme()
        assert t.show_progress_bar is False
        assert t.show_progress_counter is False
        assert t.show_help_popup is False
        assert t.show_navigation_toolbar is False


# ---------------------------------------------------------------------------
# #60 — media plugin
# ---------------------------------------------------------------------------


class TestMediaPlugin:
    def test_global_media_autoplay_parsed(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    media-autoplay: true")
        assert t.media_autoplay is True

    def test_global_media_autostop_parsed(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    media-autostop: true")
        assert t.media_autostop is True

    def test_global_media_autopause_parsed(self):
        t = _theme_from_yaml("theme:\n  canvas:\n    media-autopause: true")
        assert t.media_autopause is True

    def test_global_media_defaults_false(self):
        t = Theme()
        assert t.media_autoplay is False
        assert t.media_autostop is False
        assert t.media_autopause is False

    def test_global_media_autoplay_emitted(self):
        source = (
            "---\nmetadata:\n  - title: Test\ntheme:\n  canvas:\n    media-autoplay: true\n---\n"
            "# Chapter\n## Section\n### Subsection\n#### Slide\n"
        )
        html = _rendered_html(source)
        assert 'data-media-autoplay="true"' in html

    def test_per_slide_media_autoplay(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  media-autoplay: true"))
        assert 'data-media-autoplay="true"' in html

    def test_per_slide_media_autostop(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  media-autostop: true"))
        assert 'data-media-autostop="true"' in html

    def test_per_slide_media_omitted_when_none(self):
        html = _rendered_html(_slide_source())
        assert "data-media-autoplay" not in html
        assert "data-media-autostop" not in html
        assert "data-media-autopause" not in html

    def test_per_slide_media_default_is_none(self):
        t = Theme()
        assert t.slide_media_autoplay is None
        assert t.slide_media_autostop is None
        assert t.slide_media_autopause is None


# ---------------------------------------------------------------------------
# #61 — data-rotate-order
# ---------------------------------------------------------------------------


class TestRotateOrder:
    def test_rotate_order_parsed(self):
        t = _overtheme_from_yaml("overtheme:\n  slide:\n    rotate-order: zxy")
        assert t.rotate_order == "zxy"

    def test_rotate_order_default_empty(self):
        assert Theme().rotate_order == ""

    def test_rotate_order_emitted(self):
        html = _rendered_html(_slide_source(overtheme_yaml="slide:\n  rotate-order: zxy"))
        assert 'data-rotate-order="zxy"' in html

    def test_rotate_order_omitted_when_empty(self):
        html = _rendered_html(_slide_source())
        assert "data-rotate-order" not in html

    def test_all_valid_orders(self):
        for order in ("xyz", "xzy", "yxz", "yzx", "zxy", "zyx"):
            t = _overtheme_from_yaml(f"overtheme:\n  slide:\n    rotate-order: {order}")
            assert t.rotate_order == order
