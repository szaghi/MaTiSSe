"""
test_code_highlighting.py — Unit tests for Pygments-based code highlighting.
"""

from matisse.markdown_utils import get_pygments_css, markdown2html

# ---------------------------------------------------------------------------
# get_pygments_css
# ---------------------------------------------------------------------------


def test_pygments_css_default_contains_highlight_class():
    css = get_pygments_css()
    assert ".highlight" in css


def test_pygments_css_style_monokai():
    css = get_pygments_css(style="monokai")
    assert ".highlight" in css
    # monokai is a dark theme — background should be present
    assert "background" in css


def test_pygments_css_custom_class():
    css = get_pygments_css(style="default", css_class="mycode")
    assert ".mycode" in css
    assert ".highlight" not in css


# ---------------------------------------------------------------------------
# markdown2html — fenced code blocks
# ---------------------------------------------------------------------------


def test_fenced_python_block_produces_highlight_div():
    source = "```python\nprint('hello')\n```"
    html = markdown2html(source)
    assert '<div class="highlight">' in html


def test_fenced_python_block_contains_pygments_tokens():
    source = "```python\ndef foo():\n    pass\n```"
    html = markdown2html(source)
    # Pygments emits <span class="..."> for tokens
    assert "<span" in html


def test_unannotated_block_still_renders():
    source = "```\nplain text\n```"
    html = markdown2html(source)
    assert "plain text" in html
    assert "<pre>" in html or '<div class="highlight">' in html


def test_code_style_parameter_accepted():
    source = "```python\nx = 1\n```"
    html_default = markdown2html(source, code_style="default")
    html_monokai = markdown2html(source, code_style="monokai")
    # Both should render code; the CSS class output is the same — style affects CSS, not HTML structure
    assert '<div class="highlight">' in html_default
    assert '<div class="highlight">' in html_monokai


def test_no_hljs_references_in_output():
    source = "```python\nprint('hi')\n```"
    html = markdown2html(source)
    assert "hljs" not in html
    assert "highlight.js" not in html


# ---------------------------------------------------------------------------
# theme code: section
# ---------------------------------------------------------------------------


def test_theme_code_section_emits_css():
    from matisse.backends.impress.theme import ImpressTheme

    ImpressTheme.reset()
    theme = ImpressTheme(
        source="""
theme:
  code:
    font-size: '85%'
    border-radius: '4px'
""",
        name="theme",
    )
    assert theme.css is not None
    assert "font-size" in theme.css
    assert "85%" in theme.css


def test_theme_code_style_is_captured():
    from matisse.backends.impress.theme import ImpressTheme

    ImpressTheme.reset()
    theme = ImpressTheme(
        source="""
theme:
  code:
    style: 'monokai'
    font-size: '90%'
""",
        name="theme",
    )
    assert theme.code_style == "monokai"


def test_theme_without_code_section_has_empty_code():
    from matisse.backends.impress.theme import ImpressTheme

    ImpressTheme.reset()
    theme = ImpressTheme(
        source="""
theme:
  canvas:
    background: '#fff'
""",
        name="theme",
    )
    assert theme.code == []
    assert theme.code_style == ""
