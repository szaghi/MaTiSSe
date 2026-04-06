#!/usr/bin/env python3
"""
test_phase62_features.py — Tests for issue #62 (7 Quarto-inspired phases).

Phase 1: Callout blocks
Phase 2: Mermaid/Graphviz diagram blocks
Phase 3: Theorem/lemma/proof environments
Phase 4: Incremental lists + ". . ." pause markers
Phase 5: Per-slide backgrounds via heading attributes
Phase 6: Subfigure layouts
Phase 7: Cross-references and label registry
"""

import os
import tempfile

import pytest

from matisse.callout import Callout
from matisse.diagram import GRAPHVIZ_CDN_SCRIPTS, MERMAID_CDN_SCRIPT, Diagram
from matisse.figure_group import FigureGroup
from matisse.incremental import PAUSE_RE, IncrementalList
from matisse.labels import LabelRegistry
from matisse.matisse import make_presentation
from matisse.matisse_config import MatisseConfig
from matisse.slide import Slide
from matisse.theorem import Theorem


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _config(backend="impress"):
    class _ns:
        verbose = False
        offline = False
        code_style = "default"
        theme = None
        toc_at_chap_beginning = None
        toc_at_sec_beginning = None
        toc_at_subsec_beginning = None
        pdf = False
        print_parsed_source = False

    _ns.backend = backend
    return MatisseConfig(cliargs=_ns())


_SLIDE_PREFIX = """\
---
metadata:
  - title: Test
  - authors: [A]
---

# Chapter

## Section

### Subsection

#### Slide

"""


def _render_slide_html(content, backend="impress"):
    """Build a minimal presentation containing *content* on one slide and
    return the rendered index.html text."""
    src = _SLIDE_PREFIX + content + "\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        config = _config(backend=backend)
        make_presentation(config=config, source=src, output=tmpdir)
        with open(os.path.join(tmpdir, "index.html")) as fh:
            return fh.read()


# ===========================================================================
# Phase 1 — Callout blocks
# ===========================================================================


class TestCallout:
    def setup_method(self):
        Callout.reset()

    def test_callout_note_html(self):
        src = """::: {.callout-note}
## Note title
Content here.
:::"""
        c = Callout(source=src)
        html = c.to_html()
        assert 'class="callout callout-note"' in html
        assert "Note title" in html
        assert "Content here." in html

    def test_callout_warning(self):
        src = """::: {.callout-warning}
Watch out.
:::"""
        c = Callout(source=src)
        html = c.to_html()
        assert 'class="callout callout-warning"' in html
        assert "Watch out." in html

    def test_callout_inline_title(self):
        src = """::: {.callout-tip title="Handy hint"}
Try this.
:::"""
        c = Callout(source=src)
        assert c.title == "Handy hint"
        html = c.to_html()
        assert "Handy hint" in html

    def test_callout_default_title_from_type(self):
        src = """::: {.callout-important}
Be careful.
:::"""
        c = Callout(source=src)
        # title attribute is None when not specified; to_html() falls back to type.title()
        assert c.title is None
        assert "Important" in c.to_html()

    def test_callout_caution_color(self):
        src = """::: {.callout-caution}
Danger.
:::"""
        c = Callout(source=src)
        html = c.to_html()
        assert "border-left:" in html

    def test_callout_counter_increments(self):
        for i in range(3):
            Callout(source="::: {.callout-note}\nX.\n:::")
        assert Callout.callouts_number == 3

    def test_callout_reset(self):
        Callout(source="::: {.callout-note}\nX.\n:::")
        Callout.reset()
        assert Callout.callouts_number == 0

    def test_callout_all_types(self):
        for ctype in ("note", "tip", "warning", "caution", "important"):
            Callout.reset()
            src = f"::: {{.callout-{ctype}}}\nBody.\n:::"
            c = Callout(source=src)
            assert c.ctype == ctype
            html = c.to_html()
            assert f"callout-{ctype}" in html

    def test_callout_rendered_in_presentation(self):
        # Note: avoid ## headings inside callout blocks in a presentation context —
        # they conflict with MaTiSSe's section-heading tokenizer.  Use title= attr.
        content = '::: {.callout-tip title="Pro tip"}\nUse MaTiSSe.\n:::'
        html = _render_slide_html(content)
        assert "callout-tip" in html
        assert "Pro tip" in html

    def test_callout_reveal_backend(self):
        content = '::: {.callout-note title="Note"}\nNote content.\n:::'
        html = _render_slide_html(content, backend="reveal")
        assert "callout-note" in html
        assert "Note content." in html


# ===========================================================================
# Phase 2 — Mermaid / Graphviz diagrams
# ===========================================================================


class TestDiagram:
    def setup_method(self):
        Diagram.reset()

    def test_mermaid_basic(self):
        src = "```{mermaid}\nflowchart LR\n  A --> B\n```"
        d = Diagram(source=src)
        assert d.engine == "mermaid"
        assert "A --> B" in d.source
        assert Diagram.has_mermaid is True
        assert Diagram.has_graphviz is False

    def test_graphviz_basic(self):
        src = "```{dot}\ndigraph G { A -> B; }\n```"
        d = Diagram(source=src)
        assert d.engine == "dot"
        assert "A -> B" in d.source
        assert Diagram.has_graphviz is True
        assert Diagram.has_mermaid is False

    def test_mermaid_html_output(self):
        src = "```{mermaid}\nflowchart LR\n  A --> B\n```"
        d = Diagram(source=src)
        html = d.to_html()
        assert 'class="mermaid"' in html
        # yattag HTML-escapes content: --> becomes --&gt;
        assert "A --" in html

    def test_graphviz_html_output(self):
        src = "```{dot}\ndigraph G { A -> B; }\n```"
        d = Diagram(source=src)
        html = d.to_html()
        assert 'class="graphviz"' in html
        assert "A -" in html

    def test_caption_parsed(self):
        src = '```{mermaid}\n%%| fig-cap: "Build pipeline"\nflowchart LR\n  A --> B\n```'
        d = Diagram(source=src)
        assert d.caption == "Build pipeline"
        html = d.to_html()
        assert "Build pipeline" in html

    def test_reset_clears_flags(self):
        Diagram(source="```{mermaid}\nA --> B\n```")
        assert Diagram.has_mermaid is True
        Diagram.reset()
        assert Diagram.has_mermaid is False
        assert Diagram.has_graphviz is False
        assert Diagram.diagrams_number == 0

    def test_mermaid_cdn_injected_in_presentation(self):
        content = "```{mermaid}\nflowchart LR\n  A --> B\n```"
        html = _render_slide_html(content)
        assert "mermaid" in html

    def test_graphviz_cdn_injected_in_presentation(self):
        content = "```{dot}\ndigraph G { A -> B; }\n```"
        html = _render_slide_html(content)
        assert "graphviz" in html

    def test_mermaid_cdn_injected_reveal(self):
        content = "```{mermaid}\nflowchart LR\n  A --> B\n```"
        html = _render_slide_html(content, backend="reveal")
        assert "mermaid" in html

    def test_diagram_figure_id(self):
        Diagram.reset()
        src = "```{mermaid}\nA --> B\n```"
        d = Diagram(source=src)
        html = d.to_html()
        assert 'id="diagram-1"' in html


# ===========================================================================
# Phase 3 — Theorem / lemma / proof environments
# ===========================================================================


class TestTheorem:
    def setup_method(self):
        Theorem.reset()

    def test_theorem_basic(self):
        src = "::: {#thm-cauchy}\n## Cauchy\n$|u|^2 \\leq 1$\n:::"
        t = Theorem(source=src)
        assert t.prefix == "thm"
        assert t.env_id == "cauchy"
        assert t.title == "Cauchy"
        assert t.env_number == 1

    def test_theorem_auto_numbering(self):
        Theorem(source="::: {#thm-one}\nFirst.\n:::")
        t2 = Theorem(source="::: {#thm-two}\nSecond.\n:::")
        assert t2.env_number == 2

    def test_proof_block(self):
        src = "::: {.proof}\nBy induction.\n:::"
        t = Theorem(source=src)
        assert t.is_proof is True
        assert t.prefix is None

    def test_proof_qed_appended(self):
        src = "::: {.proof}\nBy induction.\n:::"
        t = Theorem(source=src)
        html = t.to_html()
        assert "∎" in html

    def test_proof_no_double_qed(self):
        src = "::: {.proof}\nBy induction. ∎\n:::"
        t = Theorem(source=src)
        html = t.to_html()
        # Should not duplicate the ∎
        assert html.count("∎") == 1

    def test_theorem_html_output(self):
        src = "::: {#thm-pythagoras}\n## Pythagorean theorem\n$a^2 + b^2 = c^2$\n:::"
        t = Theorem(source=src)
        html = t.to_html()
        assert 'class="theorem theorem-thm"' in html
        assert 'id="thm-pythagoras"' in html
        assert "Theorem 1" in html
        assert "Pythagorean theorem" in html

    def test_lemma_label(self):
        src = "::: {#lem-bound}\nBound.\n:::"
        t = Theorem(source=src)
        html = t.to_html()
        assert "Lemma 1" in html
        assert 'class="theorem theorem-lem"' in html

    def test_definition_label(self):
        src = "::: {#def-metric}\nA metric space...\n:::"
        t = Theorem(source=src)
        html = t.to_html()
        assert "Definition 1" in html

    def test_separate_counters_per_prefix(self):
        Theorem(source="::: {#thm-one}\nFirst.\n:::")
        Theorem(source="::: {#lem-bound}\nLemma.\n:::")
        t3 = Theorem(source="::: {#thm-two}\nSecond theorem.\n:::")
        assert t3.env_number == 2  # thm counter is 2, not 3

    def test_reset_clears_counters(self):
        Theorem(source="::: {#thm-one}\nOne.\n:::")
        Theorem.reset()
        t = Theorem(source="::: {#thm-fresh}\nFresh.\n:::")
        assert t.env_number == 1

    def test_theorem_rendered_in_presentation(self):
        # Avoid ## headings inside theorem blocks — they conflict with the section tokenizer.
        content = "::: {#thm-main}\n$E = mc^2$\n:::"
        html = _render_slide_html(content)
        assert "theorem-thm" in html
        assert "Theorem 1" in html

    def test_theorem_reveal_backend(self):
        content = "::: {#def-field}\nA set with two operations.\n:::"
        html = _render_slide_html(content, backend="reveal")
        assert "theorem-def" in html


# ===========================================================================
# Phase 4 — Incremental lists + pause markers
# ===========================================================================


class TestIncrementalList:
    def setup_method(self):
        IncrementalList.reset()

    def test_incremental_parsing(self):
        src = "::: {.incremental}\n- Item A\n- Item B\n- Item C\n:::"
        il = IncrementalList(source=src)
        assert il.items == ["Item A", "Item B", "Item C"]

    def test_incremental_impress_html(self):
        src = "::: {.incremental}\n- First\n- Second\n:::"
        il = IncrementalList(source=src)
        html = il.to_html(backend="impress")
        assert 'class="substep"' in html
        assert "First" in html
        assert "Second" in html

    def test_incremental_reveal_html(self):
        src = "::: {.incremental}\n- First\n- Second\n:::"
        il = IncrementalList(source=src)
        html = il.to_html(backend="reveal")
        assert 'class="fragment"' in html
        assert "First" in html

    def test_incremental_list_class(self):
        src = "::: {.incremental}\n- A\n:::"
        il = IncrementalList(source=src)
        html = il.to_html()
        assert "incremental-list" in html

    def test_reset(self):
        IncrementalList(source="::: {.incremental}\n- A\n:::")
        IncrementalList.reset()
        assert IncrementalList.incremental_number == 0

    def test_incremental_in_presentation(self):
        content = "::: {.incremental}\n- Step 1\n- Step 2\n:::"
        html = _render_slide_html(content)
        assert "incremental-list" in html
        assert "Step 1" in html

    def test_incremental_reveal_in_presentation(self):
        content = "::: {.incremental}\n- Step 1\n- Step 2\n:::"
        html = _render_slide_html(content, backend="reveal")
        assert "fragment" in html


class TestPauseMarkers:
    def test_pause_re_matches(self):
        assert PAUSE_RE.search(". . .")
        assert PAUSE_RE.search("\n. . .\n")
        assert PAUSE_RE.search("  . . .  ")

    def test_pause_splits_content(self):
        src = "First part\n\n. . .\n\nSecond part"
        parts = PAUSE_RE.split(src)
        assert len(parts) == 2
        assert "First part" in parts[0]
        assert "Second part" in parts[1]

    def test_pause_marker_reveal_presentation(self):
        content = "Before pause.\n\n. . .\n\nAfter pause."
        html = _render_slide_html(content, backend="reveal")
        assert 'class="fragment"' in html
        assert "Before pause." in html
        assert "After pause." in html

    def test_pause_marker_impress_presentation(self):
        content = "Before pause.\n\n. . .\n\nAfter pause."
        html = _render_slide_html(content, backend="impress")
        assert 'class="substep"' in html

    def test_no_pause_no_fragment(self):
        content = "Just plain content."
        html = _render_slide_html(content, backend="reveal")
        assert 'class="fragment"' not in html


# ===========================================================================
# Phase 5 — Per-slide backgrounds via heading attributes
# ===========================================================================


class TestPerSlideBackground:
    def test_background_color_parsed(self):
        slide = Slide(number=1, title='My Slide {background-color="#ff0000"}')
        assert slide.heading_attrs.get("background-color") == "#ff0000"
        assert slide.title == "My Slide"

    def test_background_image_parsed(self):
        slide = Slide(number=1, title='Slide {background-image="img/bg.jpg"}')
        assert slide.heading_attrs.get("background-image") == "img/bg.jpg"

    def test_title_stripped_of_attrs(self):
        slide = Slide(number=1, title='Clean Title {background-color="blue"}')
        assert slide.title == "Clean Title"
        assert "{" not in slide.title

    def test_background_style_impress(self):
        slide = Slide(number=1, title='Slide {background-color="#abc"}')
        style = slide.background_style()
        assert "background-color: #abc" in style

    def test_background_image_style_impress(self):
        slide = Slide(number=1, title='Slide {background-image="bg.jpg"}')
        style = slide.background_style()
        assert "background-image: url('bg.jpg')" in style
        assert "background-size: cover" in style
        assert "background-position: center" in style

    def test_reveal_background_attrs(self):
        slide = Slide(number=1, title='Slide {background-color="#ff0000"}')
        attrs = slide.reveal_background_attrs()
        assert attrs.get("data-background-color") == "#ff0000"

    def test_reveal_background_image_attrs(self):
        slide = Slide(number=1, title='Slide {background-image="bg.jpg" background-opacity="0.5"}')
        attrs = slide.reveal_background_attrs()
        assert attrs.get("data-background-image") == "bg.jpg"
        assert attrs.get("data-background-opacity") == "0.5"

    def test_no_attrs_empty_dict(self):
        slide = Slide(number=1, title="Plain Slide")
        assert slide.heading_attrs == {}
        assert slide.reveal_background_attrs() == {}
        assert slide.background_style() == ""

    def test_background_color_in_reveal_section(self):
        src = """\
---
metadata:
  - title: BG Test
  - authors: [A]
---

# Chapter

## Section

### Subsection

#### My Slide {background-color="#123456"}

Some content.
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = _config(backend="reveal")
            make_presentation(config=config, source=src, output=tmpdir)
            with open(os.path.join(tmpdir, "index.html")) as fh:
                html = fh.read()
        assert 'data-background-color="#123456"' in html

    def test_background_color_in_impress_section(self):
        src = """\
---
metadata:
  - title: BG Test
  - authors: [A]
---

# Chapter

## Section

### Subsection

#### My Slide {background-color="#abcdef"}

Some content.
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = _config(backend="impress")
            make_presentation(config=config, source=src, output=tmpdir)
            with open(os.path.join(tmpdir, "index.html")) as fh:
                html = fh.read()
        assert "background-color: #abcdef" in html


# ===========================================================================
# Phase 6 — Subfigure groups
# ===========================================================================


class TestFigureGroup:
    def setup_method(self):
        FigureGroup.reset()

    def test_figure_group_parsed(self):
        src = """::: {#fig-comp layout-ncol=2}

$figure
$content[width:100%]{img/a.png}
$caption{Before}
$endfigure

$figure
$content[width:100%]{img/b.png}
$caption{After}
$endfigure

Comparison.
:::"""
        fg = FigureGroup(source=src)
        assert fg.gid == "fig-comp"
        assert fg.ncol == 2
        assert len(fg.figures) == 2
        assert fg.group_caption == "Comparison."

    def test_figure_group_grid_css_ncol(self):
        src = """::: {#fig-grid layout-ncol=3}

$figure
$content[width:100%]{img/a.png}
$caption{A}
$endfigure

Caption.
:::"""
        fg = FigureGroup(source=src)
        css = fg._grid_css()
        assert "repeat(3, 1fr)" in css

    def test_figure_group_html(self):
        src = """::: {#fig-test layout-ncol=2}

$figure
$content[width:100%]{img/a.png}
$caption{A}
$endfigure

$figure
$content[width:100%]{img/b.png}
$caption{B}
$endfigure

Group caption.
:::"""
        fg = FigureGroup(source=src)
        html = fg.to_html()
        assert 'id="fig-test"' in html
        assert "subfigure" in html
        assert "(a)" in html
        assert "(b)" in html
        assert "Group caption." in html

    def test_figure_group_reset(self):
        FigureGroup(source="::: {#fig-x layout-ncol=1}\n$figure\n$source{a.png}\n$caption{A}\n$endfigure\n\nCap.\n:::")
        FigureGroup.reset()
        assert FigureGroup.groups_number == 0

    def test_figure_group_in_presentation(self):
        content = """::: {#fig-pair layout-ncol=2}

$figure
$content[width:100%]{img/a.png}
$caption{A}
$endfigure

$figure
$content[width:100%]{img/b.png}
$caption{B}
$endfigure

Pair.
:::"""
        html = _render_slide_html(content)
        assert "fig-pair" in html
        assert "subfigure" in html


# ===========================================================================
# Phase 7 — Cross-references and label registry
# ===========================================================================


class TestLabelRegistry:
    def test_register_and_resolve(self):
        reg = LabelRegistry()
        entry = reg.register("fig", "results")
        assert entry.label == "fig-results"
        assert entry.kind == "fig"
        assert entry.number == 1
        assert entry.html_id == "fig-results"

    def test_sequential_numbering(self):
        reg = LabelRegistry()
        reg.register("fig", "first")
        e2 = reg.register("fig", "second")
        assert e2.number == 2

    def test_separate_counters_per_kind(self):
        reg = LabelRegistry()
        reg.register("fig", "f1")
        e_tbl = reg.register("tbl", "t1")
        assert e_tbl.number == 1  # tbl counter is separate

    def test_resolve_known_label(self):
        reg = LabelRegistry()
        reg.register("fig", "results")
        assert reg.resolve("fig-results") == "Figure 1"

    def test_resolve_unknown_label(self, capsys):
        reg = LabelRegistry()
        result = reg.resolve("fig-missing")
        assert result == "??"
        captured = capsys.readouterr()
        assert "unresolved" in captured.out

    def test_collect_from_source(self):
        reg = LabelRegistry()
        src = "See {#fig-results} and {#tbl-data layout-ncol=2}"
        reg.collect_from_source(src)
        assert "fig-results" in reg._entries
        assert "tbl-data" in reg._entries

    def test_substitute_refs(self):
        reg = LabelRegistry()
        reg.register("fig", "results")
        html = "See @fig-results for details."
        out = reg.substitute_refs(html)
        assert '<a href="#fig-results"' in out
        assert "Figure 1" in out

    def test_substitute_unknown_ref(self, capsys):
        reg = LabelRegistry()
        html = "See @fig-missing for details."
        out = reg.substitute_refs(html)
        assert "??" in out

    def test_idempotent_register(self):
        reg = LabelRegistry()
        e1 = reg.register("thm", "cauchy")
        e2 = reg.register("thm", "cauchy")
        assert e1 is e2
        assert reg._counters["thm"] == 1

    def test_theorem_label(self):
        reg = LabelRegistry()
        reg.register("thm", "main")
        assert reg.resolve("thm-main") == "Theorem 1"

    def test_equation_label(self):
        reg = LabelRegistry()
        reg.register("eq", "schrodinger")
        assert reg.resolve("eq-schrodinger") == "Equation 1"

    def test_cross_ref_in_presentation(self):
        src = """\
---
metadata:
  - title: Ref Test
  - authors: [A]
---

# Chapter

## Section

### Subsection

#### Slide A

::: {#fig-diagram layout-ncol=1}

$figure
$content[width:100%]{img/a.png}
$caption{A figure}
$endfigure

Caption.
:::

#### Slide B

See @fig-diagram for the results.
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = _config(backend="impress")
            make_presentation(config=config, source=src, output=tmpdir)
            with open(os.path.join(tmpdir, "index.html")) as fh:
                html = fh.read()
        assert "Figure 1" in html
        assert 'href="#fig-diagram"' in html


# ===========================================================================
# Integration — multiple phases together
# ===========================================================================


class TestPhase62Integration:
    def test_callout_and_theorem_together(self):
        content = '::: {.callout-note title="Background"}\nUseful note.\n:::\n\n::: {#thm-main}\n$f(x) = x^2$\n:::'
        html = _render_slide_html(content)
        assert "callout-note" in html
        assert "theorem-thm" in html

    def test_incremental_and_pause_together(self):
        content = """::: {.incremental}
- First
- Second
:::

. . .

After pause.
"""
        html = _render_slide_html(content, backend="reveal")
        assert "incremental-list" in html
        assert "fragment" in html

    def test_diagram_and_cross_ref_together(self):
        content = """```{mermaid}
%%| fig-cap: "Pipeline"
flowchart LR
  A --> B
```

See @dia-pipeline for the flow."""
        html = _render_slide_html(content)
        assert "mermaid" in html
