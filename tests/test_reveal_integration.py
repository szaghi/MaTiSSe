"""
Integration tests for the reveal.js rendering backend.

Uses the fixture at tests/compare/reveal/test.md and verifies:
- structural well-formedness of the generated HTML
- reveal-specific elements (Reveal.initialize, plugin scripts, etc.)
- that RevealTheme options are wired into the output
- per-slide data-* attributes
- rendering determinism
"""

import os

import pytest

from matisse.backends.reveal.renderer import RevealBackend
from matisse.matisse_config import MatisseConfig
from matisse.presentation import Presentation

_FIXTURE = os.path.join(os.path.dirname(__file__), "compare", "reveal", "test.md")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def reveal_config():
    """MatisseConfig with reveal backend."""
    cfg = MatisseConfig()
    cfg.backend = "reveal"
    return cfg


@pytest.fixture(scope="module")
def reveal_html(reveal_config):
    """Rendered HTML for the reveal fixture (rendered once for the module)."""
    source = open(_FIXTURE).read()
    p = Presentation()
    p.parse(config=reveal_config, source=source)
    return RevealBackend(reveal_config).render(p)


# ---------------------------------------------------------------------------
# Structural well-formedness
# ---------------------------------------------------------------------------


class TestRevealHtmlStructure:
    def test_doctype(self, reveal_html):
        assert "<!DOCTYPE html>" in reveal_html

    def test_html_tag(self, reveal_html):
        assert "<html>" in reveal_html

    def test_html_closes(self, reveal_html):
        assert "</html>" in reveal_html

    def test_body_tag(self, reveal_html):
        assert "<body>" in reveal_html

    def test_reveal_div(self, reveal_html):
        assert 'class="reveal"' in reveal_html

    def test_slides_div(self, reveal_html):
        assert 'class="slides"' in reveal_html

    def test_sections_rendered(self, reveal_html):
        assert "<section" in reveal_html

    def test_no_impress_root(self, reveal_html):
        assert 'id="impress"' not in reveal_html


# ---------------------------------------------------------------------------
# Head: CSS and metadata
# ---------------------------------------------------------------------------


class TestRevealHead:
    def test_reveal_reset_css(self, reveal_html):
        assert "reset.css" in reveal_html

    def test_reveal_core_css(self, reveal_html):
        assert "reveal.css" in reveal_html

    def test_moon_theme_css(self, reveal_html):
        assert "theme/moon.css" in reveal_html

    def test_pygments_css(self, reveal_html):
        # code_highlight is True by default in MatisseConfig
        assert "pygments.css" in reveal_html

    def test_custom_css_injected(self, reveal_html):
        assert "font-family: sans-serif" in reveal_html


# ---------------------------------------------------------------------------
# Scripts: Reveal.initialize() options
# ---------------------------------------------------------------------------


class TestRevealInitialize:
    def test_reveal_initialize_present(self, reveal_html):
        assert "Reveal.initialize(" in reveal_html

    def test_transition_fade(self, reveal_html):
        assert "transition: 'fade'" in reveal_html

    def test_transition_speed_fast(self, reveal_html):
        assert "transitionSpeed: 'fast'" in reveal_html

    def test_controls_true(self, reveal_html):
        assert "controls: true" in reveal_html

    def test_controls_layout(self, reveal_html):
        assert "controlsLayout: 'bottom-right'" in reveal_html

    def test_progress_true(self, reveal_html):
        assert "progress: true" in reveal_html

    def test_slide_number_c_t(self, reveal_html):
        assert "slideNumber: 'c/t'" in reveal_html

    def test_center_true(self, reveal_html):
        assert "center: true" in reveal_html

    def test_width_1280(self, reveal_html):
        assert "width: 1280" in reveal_html

    def test_height_720(self, reveal_html):
        assert "height: 720" in reveal_html

    def test_background_transition(self, reveal_html):
        assert "backgroundTransition: 'fade'" in reveal_html

    def test_hash_always_true(self, reveal_html):
        assert "hash: true" in reveal_html


# ---------------------------------------------------------------------------
# Plugins
# ---------------------------------------------------------------------------


class TestRevealPlugins:
    def test_notes_plugin_script(self, reveal_html):
        assert "plugin/notes/notes.js" in reveal_html

    def test_zoom_plugin_script(self, reveal_html):
        assert "plugin/zoom/zoom.js" in reveal_html

    def test_plugins_in_initialize(self, reveal_html):
        assert "RevealNotes" in reveal_html
        assert "RevealZoom" in reveal_html

    def test_no_math_plugin_when_not_configured(self, reveal_html):
        # test.md uses notes + zoom, not math
        assert "RevealMath" not in reveal_html

    def test_standalone_mathjax_loaded(self, reveal_html):
        # math plugin not active → standalone MathJax must be loaded
        assert "mathjax@3" in reveal_html


# ---------------------------------------------------------------------------
# Speaker notes
# ---------------------------------------------------------------------------


class TestSpeakerNotes:
    def test_aside_notes_present(self, reveal_html):
        assert '<aside class="notes">' in reveal_html

    def test_note_content_in_aside(self, reveal_html):
        assert "Speaker note on the title slide" in reveal_html


# ---------------------------------------------------------------------------
# Per-slide overrides
# ---------------------------------------------------------------------------


class TestPerSlideOverrides:
    def test_background_color_attribute(self, reveal_html):
        assert 'data-background-color="#2c3e50"' in reveal_html

    def test_per_slide_transition(self, reveal_html):
        assert 'data-transition="zoom"' in reveal_html

    def test_auto_animate_attribute(self, reveal_html):
        assert "data-auto-animate" in reveal_html


# ---------------------------------------------------------------------------
# Math plugin variant
# ---------------------------------------------------------------------------


class TestMathPlugin:
    """Verify behaviour when the math plugin is active."""

    def test_math_plugin_replaces_standalone_mathjax(self, reveal_config):
        source = """---
metadata:
  - title: Math Plugin Test
  - authors:
    - Tester
---
---
reveal:
  plugins:
    - math
---
# Chapter
## Section
### Sub
#### Slide
$E = mc^2$
"""
        p = Presentation()
        p.parse(config=reveal_config, source=source)
        html = RevealBackend(reveal_config).render(p)
        assert "RevealMath.MathJax3" in html
        assert "plugin/math/math.js" in html
        # standalone MathJax script block should NOT appear
        assert "MathJax = {" not in html
        # math config inside Reveal.initialize
        assert "math: {" in html


# ---------------------------------------------------------------------------
# Vertical layout
# ---------------------------------------------------------------------------


class TestVerticalLayout:
    def test_vertical_layout_outer_sections(self, reveal_config):
        source = """---
metadata:
  - title: Vertical Test
  - authors:
    - Tester
---
---
reveal:
  layout: vertical
---
# Chapter One
## Section One
### Sub One
#### Slide 1A
Content A1.
#### Slide 1B
Content A2.
# Chapter Two
## Section Two
### Sub Two
#### Slide 2A
Content B1.
"""
        p = Presentation()
        p.parse(config=reveal_config, source=source)
        html = RevealBackend(reveal_config).render(p)
        assert "<!DOCTYPE html>" in html
        assert 'class="slides"' in html
        assert "<section" in html


# ---------------------------------------------------------------------------
# Decorator integration
# ---------------------------------------------------------------------------

_DECORATOR_FIXTURE = os.path.join(
    os.path.dirname(__file__), "compare", "reveal-decorators", "test.md"
)


@pytest.fixture(scope="module")
def decorator_html(reveal_config):
    """Rendered HTML for the decorator fixture."""
    source = open(_DECORATOR_FIXTURE).read()
    p = Presentation()
    p.parse(config=reveal_config, source=source)
    return RevealBackend(reveal_config).render(p)


class TestDecoratorLayout:
    def test_decorator_css_injected(self, decorator_html):
        assert "matisse-decorated" in decorator_html

    def test_flex_column_on_section(self, decorator_html):
        assert "flex-direction: column" in decorator_html

    def test_slide_header_div(self, decorator_html):
        assert 'class="slide-header-1"' in decorator_html

    def test_slide_footer_div(self, decorator_html):
        assert 'class="slide-footer-1"' in decorator_html

    def test_slide_content_div(self, decorator_html):
        assert 'class="slide-content"' in decorator_html

    def test_section_has_matisse_decorated_class(self, decorator_html):
        assert 'class="matisse-decorated"' in decorator_html

    def test_decorator_css_height(self, decorator_html):
        assert "height: 8%;" in decorator_html

    def test_decorator_css_footer_height(self, decorator_html):
        assert "height: 4%;" in decorator_html

    def test_decorator_background_color(self, decorator_html):
        assert "#1a1a2e" in decorator_html

    def test_no_slide_body_when_no_sidebar(self, decorator_html):
        # The fixture has no sidebar, so slide-body wrapper should not appear
        assert 'class="slide-body"' not in decorator_html

    def test_per_slide_decorator_override_applied(self, decorator_html):
        # Per-slide background-color override (reveal data attribute) is applied
        assert 'data-background-color="#2c3e50"' in decorator_html

    def test_per_slide_background_color(self, decorator_html):
        assert 'data-background-color="#2c3e50"' in decorator_html

    def test_slides_without_decorators_render_normally(self, reveal_config):
        """A presentation with no theme.layout decorators produces plain sections without decorator scaffolding."""
        source = open(_FIXTURE).read()  # the standard fixture has no decorators
        p = Presentation()
        p.parse(config=reveal_config, source=source)
        html = RevealBackend(reveal_config).render(p)
        assert 'class="matisse-decorated"' not in html
        assert 'class="slide-header-1"' not in html
        # No decorator CSS injected
        assert "matisse-decorated" not in html


class TestSidebarLayout:
    """Verify sidebar layout produces slide-body wrapper and correct structure."""

    def test_sidebar_produces_slide_body_div(self, reveal_config):
        source = """---
metadata:
  - title: Sidebar Test
  - authors:
    - Tester
---
---
theme:
  layout:
    sidebar-1:
      position: L
      width: 20%
      background: "#abc"
      metadata:
        slidetitle:
          float: left
---
# Chapter
## Section
### Sub
#### Slide
Slide content.
"""
        p = Presentation()
        p.parse(config=reveal_config, source=source)
        html = RevealBackend(reveal_config).render(p)
        assert 'class="slide-body"' in html
        assert 'class="slide-sidebar-1"' in html
        assert 'class="slide-content"' in html

    def test_right_sidebar(self, reveal_config):
        source = """---
metadata:
  - title: Right Sidebar Test
  - authors:
    - Tester
---
---
theme:
  layout:
    sidebar-1:
      position: R
      width: 15%
---
# Chapter
## Section
### Sub
#### Slide
Slide content.
"""
        p = Presentation()
        p.parse(config=reveal_config, source=source)
        html = RevealBackend(reveal_config).render(p)
        assert 'class="slide-body"' in html
        assert 'class="slide-sidebar-1"' in html

    def test_inactive_decorator_skipped(self, reveal_config):
        source = """---
metadata:
  - title: Inactive Test
  - authors:
    - Tester
---
---
theme:
  layout:
    header-1:
      height: 8%
      active: no
---
# Chapter
## Section
### Sub
#### Slide
Slide content.
"""
        p = Presentation()
        p.parse(config=reveal_config, source=source)
        html = RevealBackend(reveal_config).render(p)
        assert 'class="slide-header-1"' not in html
        # No active decorators → section should NOT have matisse-decorated class
        assert 'class="matisse-decorated"' not in html


# ---------------------------------------------------------------------------
# Rendering determinism
# ---------------------------------------------------------------------------


class TestRevealDeterminism:
    def test_same_source_produces_identical_html(self, reveal_config):
        source = open(_FIXTURE).read()

        p1 = Presentation()
        p1.parse(config=reveal_config, source=source)
        html1 = RevealBackend(reveal_config).render(p1)

        p2 = Presentation()
        p2.parse(config=reveal_config, source=source)
        html2 = RevealBackend(reveal_config).render(p2)

        assert html1 == html2
