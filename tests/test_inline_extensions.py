"""
Unit tests for the new inline markdown extensions:
  - mdx_strikethrough  (~~text~~)
  - mdx_sup_sub        (^text^  ~text~)
  - mdx_quarto_span    ([text]{.class})
and the built-in extensions added to markdown_utils:
  - footnotes, def_list, attr_list
"""

from matisse.markdown_utils import markdown2html

# ---------------------------------------------------------------------------
# Strikethrough
# ---------------------------------------------------------------------------


class TestStrikethrough:
    def test_basic(self):
        html = markdown2html("~~deleted~~")
        assert "<del>deleted</del>" in html

    def test_does_not_match_single_tilde(self):
        html = markdown2html("~not deleted~")
        assert "<del>" not in html

    def test_strikethrough_and_subscript_coexist(self):
        html = markdown2html("~~strike~~ and H~2~O")
        assert "<del>strike</del>" in html
        assert "<sub>2</sub>" in html

    def test_inline_within_sentence(self):
        html = markdown2html("This is ~~wrong~~ and correct.")
        assert "<del>wrong</del>" in html


# ---------------------------------------------------------------------------
# Superscript
# ---------------------------------------------------------------------------


class TestSuperscript:
    def test_basic(self):
        html = markdown2html("E = mc^2^")
        assert "<sup>2</sup>" in html

    def test_multiple(self):
        html = markdown2html("x^2^ + y^2^ = r^2^")
        assert html.count("<sup>") == 3

    def test_does_not_break_math(self):
        # MathJax wraps $...$ as AtomicString — ^ inside must not be touched
        html = markdown2html("$x^{n+1}$")
        assert "<sup>" not in html
        assert "x^{n+1}" in html


# ---------------------------------------------------------------------------
# Subscript
# ---------------------------------------------------------------------------


class TestSubscript:
    def test_basic(self):
        html = markdown2html("H~2~O")
        assert "<sub>2</sub>" in html

    def test_multiple(self):
        html = markdown2html("CO~2~ and O~3~")
        assert html.count("<sub>") == 2

    def test_double_tilde_not_subscript(self):
        # ~~text~~ should be strikethrough, not nested subscripts
        html = markdown2html("~~deleted~~")
        assert "<del>deleted</del>" in html
        assert "<sub>" not in html

    def test_does_not_break_math(self):
        html = markdown2html("$x_{n}$")
        assert "<sub>" not in html
        assert "x_{n}" in html


# ---------------------------------------------------------------------------
# Quarto-style spans
# ---------------------------------------------------------------------------


class TestQuartoSpan:
    def test_underline_class(self):
        html = markdown2html("[hello]{.underline}")
        assert '<span class="underline">hello</span>' in html

    def test_mark_class(self):
        html = markdown2html("[important]{.mark}")
        assert '<span class="mark">important</span>' in html

    def test_smallcaps_class(self):
        html = markdown2html("[Title]{.smallcaps}")
        assert '<span class="smallcaps">Title</span>' in html

    def test_multiple_classes(self):
        html = markdown2html("[text]{.bold .red}")
        assert "bold" in html
        assert "red" in html
        assert "<span" in html

    def test_id_attribute(self):
        html = markdown2html("[anchor]{#my-id}")
        assert 'id="my-id"' in html

    def test_key_value_attribute(self):
        html = markdown2html('[styled]{style="color:red"}')
        assert 'style="color:red"' in html

    def test_does_not_match_empty_attrs(self):
        # {} with no content — no span should be emitted
        html = markdown2html("[text]{}")
        assert "<span" not in html

    def test_does_not_steal_links(self):
        # Standard links must still work
        html = markdown2html("[Quarto](https://quarto.org)")
        assert '<a href="https://quarto.org"' in html
        assert "<span" not in html


# ---------------------------------------------------------------------------
# Footnotes (built-in Python-Markdown extension)
# ---------------------------------------------------------------------------


class TestFootnotes:
    def test_basic_footnote(self):
        source = "Some text[^1].\n\n[^1]: The footnote."
        html = markdown2html(source)
        assert "footnote" in html.lower()
        assert "The footnote." in html

    def test_inline_footnote_not_supported(self):
        # Python-Markdown footnotes extension does not support ^[inline] form
        # (that is a Pandoc extension); just ensure no crash
        html = markdown2html("text^[note]")
        assert html  # no exception


# ---------------------------------------------------------------------------
# Definition lists (built-in Python-Markdown extension)
# ---------------------------------------------------------------------------


class TestDefinitionLists:
    def test_basic_definition(self):
        source = "Term\n:   A definition of the term."
        html = markdown2html(source)
        assert "<dl>" in html
        assert "<dt>" in html
        assert "<dd>" in html

    def test_term_content(self):
        source = "Apple\n:   A fruit."
        html = markdown2html(source)
        assert "Apple" in html
        assert "A fruit." in html


# ---------------------------------------------------------------------------
# Image attributes (built-in attr_list extension)
# ---------------------------------------------------------------------------


class TestImageAttributes:
    def test_width_attribute(self):
        html = markdown2html('![alt](image.png){width="60%"}')
        assert 'width="60%"' in html
        assert "<img" in html

    def test_class_on_image(self):
        html = markdown2html("![alt](image.png){.centered}")
        assert "<img" in html
        assert "centered" in html
