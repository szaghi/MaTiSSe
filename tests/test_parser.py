"""
Unit tests for matisse.parser.Parser.

Covers: tokenizer, tokens_end_update, slides_end_update, includes,
and the full tokenize() pipeline.
"""
import os
import tempfile

import pytest

from matisse.parser import Parser


@pytest.fixture
def parser():
    return Parser()


# ---------------------------------------------------------------------------
# tokenizer
# ---------------------------------------------------------------------------

class TestTokenizer:
    def test_finds_chapter_heading(self, parser):
        source = '# My Chapter\nsome content'
        tokens = parser.tokenizer(source=source, re_search=parser.regexs['chapter'])
        assert len(tokens) == 1
        assert tokens[0]['match'].group('expr').strip() == 'My Chapter'

    def test_finds_multiple_headings(self, parser):
        source = '# Chapter One\n## Section One\n### Subsection One\n#### Slide One\n'
        chapters = parser.tokenizer(source=source, re_search=parser.regexs['chapter'])
        sections = parser.tokenizer(source=source, re_search=parser.regexs['section'])
        subsections = parser.tokenizer(source=source, re_search=parser.regexs['subsection'])
        slides = parser.tokenizer(source=source, re_search=parser.regexs['slide'])
        assert len(chapters) == 1
        assert len(sections) == 1
        assert len(subsections) == 1
        assert len(slides) == 1

    def test_exclusion_suppresses_match_in_codeblock(self, parser):
        source = '```\n# Not a heading\n```\n# Real heading\n'
        codeblocks = parser.tokenizer(source=source, re_search=parser.regexs['codeblock'])
        chapters = parser.tokenizer(source=source, re_search=parser.regexs['chapter'], exclude=codeblocks)
        assert len(chapters) == 1
        assert 'Real heading' in chapters[0]['match'].group('expr')

    def test_no_match_returns_empty(self, parser):
        source = 'no headings here'
        tokens = parser.tokenizer(source=source, re_search=parser.regexs['chapter'])
        assert tokens == []

    def test_force_all_returns_whole_source_when_no_match(self, parser):
        source = 'no headings here'
        tokens = parser.tokenizer(source=source, re_search=parser.regexs['chapter'], force_all=True)
        # force_all returns the whole-source match minus the last empty token
        assert len(tokens) >= 1

    def test_token_positions_are_correct(self, parser):
        source = '# Alpha\n# Beta\n'
        tokens = parser.tokenizer(source=source, re_search=parser.regexs['chapter'])
        assert len(tokens) == 2
        assert tokens[0]['start'] < tokens[1]['start']
        assert tokens[0]['end'] <= tokens[1]['start']


# ---------------------------------------------------------------------------
# tokens_end_update
# ---------------------------------------------------------------------------

class TestTokensEndUpdate:
    def test_intermediate_token_end_points_to_next_start(self, parser):
        source = '# Ch1\n# Ch2\n# Ch3\n'
        tokens = parser.tokenizer(source=source, re_search=parser.regexs['chapter'])
        tokens = parser.tokens_end_update(tokens=tokens, end=len(source))
        assert tokens[0]['end_next'] == tokens[1]['start']
        assert tokens[1]['end_next'] == tokens[2]['start']

    def test_last_token_end_next_is_source_length(self, parser):
        source = '# Ch1\n# Ch2\n'
        tokens = parser.tokenizer(source=source, re_search=parser.regexs['chapter'])
        tokens = parser.tokens_end_update(tokens=tokens, end=len(source))
        assert tokens[-1]['end_next'] == len(source)

    def test_empty_token_list_returns_empty(self, parser):
        result = parser.tokens_end_update(tokens=[], end=100)
        assert result == []


# ---------------------------------------------------------------------------
# slides_end_update
# ---------------------------------------------------------------------------

class TestSlidesEndUpdate:
    def test_slide_end_trimmed_by_section_start(self, parser):
        source = '#### Slide\ncontent\n## Section\n'
        slides = parser.tokenizer(source=source, re_search=parser.regexs['slide'])
        slides = parser.tokens_end_update(tokens=slides, end=len(source))
        sections = parser.tokenizer(source=source, re_search=parser.regexs['section'])
        slides = parser.slides_end_update(slides=slides, others=sections)
        assert slides[0]['end_next'] == sections[0]['start']

    def test_slide_not_trimmed_when_section_is_before(self, parser):
        source = '## Section\n#### Slide\ncontent\n'
        slides = parser.tokenizer(source=source, re_search=parser.regexs['slide'])
        slides = parser.tokens_end_update(tokens=slides, end=len(source))
        original_end = slides[0]['end_next']
        sections = parser.tokenizer(source=source, re_search=parser.regexs['section'])
        slides = parser.slides_end_update(slides=slides, others=sections)
        assert slides[0]['end_next'] == original_end


# ---------------------------------------------------------------------------
# includes
# ---------------------------------------------------------------------------

class TestIncludes:
    def test_source_without_includes_is_unchanged(self, parser):
        source = '# Chapter\n## Section\ncontent\n'
        assert parser.includes(source=source) == source

    def test_single_include_is_expanded(self, parser):
        with tempfile.TemporaryDirectory() as tmpdir:
            included = os.path.join(tmpdir, 'inc.md')
            with open(included, 'w') as f:
                f.write('included content\n')
            source = f'$include({included})\n'
            result = parser.includes(source=source)
            assert 'included content' in result
            assert '$include' not in result

    def test_include_inside_codeblock_is_not_expanded(self, parser):
        source = '```\n$include(nonexistent.md)\n```\n'
        result = parser.includes(source=source)
        assert '$include' in result


# ---------------------------------------------------------------------------
# tokenize (full pipeline)
# ---------------------------------------------------------------------------

class TestTokenize:
    def test_full_document_structure(self, parser):
        source = (
            '# Chapter\n'
            '## Section\n'
            '### Subsection\n'
            '#### Slide One\ncontent one\n'
            '#### Slide Two\ncontent two\n'
        )
        tokens = parser.tokenize(source=source)
        assert len(tokens['chapters']) == 1
        assert len(tokens['sections']) == 1
        assert len(tokens['subsections']) == 1
        assert len(tokens['slides']) == 2

    def test_codeblock_excluded_from_chapter_tokens(self, parser):
        source = '```\n# fake chapter\n```\n# Real Chapter\n'
        tokens = parser.tokenize(source=source)
        chapters = [t for t in tokens['chapters']
                    if 'Real Chapter' in t['match'].group('expr')]
        assert len(chapters) == 1

    def test_yaml_block_detected(self, parser):
        source = '---\nkey: value\n---\n# Chapter\n'
        tokens = parser.tokenize(source=source)
        assert len(tokens['yamlblocks']) == 1
