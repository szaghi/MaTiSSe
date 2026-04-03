"""
Unit tests for matisse.metadata.Metadata.

Covers: __init__, update_value (string and list), parse (no match / match),
and the to_html dispatch for plain string metadata.
"""
import pytest

from matisse.metadata import Metadata
from matisse.parser import Parser


@pytest.fixture
def parser():
    return Parser()


# ---------------------------------------------------------------------------
# __init__
# ---------------------------------------------------------------------------

class TestMetadataInit:
    def test_name_stored(self):
        m = Metadata(name='title', value='')
        assert m.name == 'title'

    def test_default_value_stored(self):
        m = Metadata(name='title', value='Hello')
        assert m.value == 'Hello'

    def test_list_value_stored(self):
        m = Metadata(name='authors', value=[])
        assert m.value == []

    def test_regex_compiled(self):
        m = Metadata(name='title', value='')
        import re
        assert isinstance(m.regex, type(re.compile('')))

    def test_regex_matches_placeholder(self):
        m = Metadata(name='title', value='')
        assert m.regex.search('$title') is not None

    def test_regex_matches_placeholder_with_style(self):
        m = Metadata(name='title', value='')
        assert m.regex.search('$title[font-size:120%]') is not None

    def test_regex_does_not_match_other_placeholder(self):
        m = Metadata(name='title', value='')
        assert m.regex.search('$authors') is None


# ---------------------------------------------------------------------------
# update_value
# ---------------------------------------------------------------------------

class TestUpdateValue:
    def test_string_value_updated(self):
        m = Metadata(name='title', value='')
        m.update_value(value='New Title')
        assert m.value == 'New Title'

    def test_string_value_coerced_to_str(self):
        m = Metadata(name='slidenumber', value='')
        m.update_value(value=42)
        assert m.value == '42'

    def test_list_value_extended(self):
        m = Metadata(name='authors', value=[])
        m.update_value(value=['Alice', 'Bob'])
        assert 'Alice' in m.value
        assert 'Bob' in m.value

    def test_list_value_items_are_strings(self):
        m = Metadata(name='authors', value=[])
        m.update_value(value=[1, 2])
        assert m.value == ['1', '2']

    def test_list_type_mismatch_exits(self):
        """Passing a non-list to a list-valued Metadata should call sys.exit."""
        m = Metadata(name='authors', value=[])
        with pytest.raises(SystemExit):
            m.update_value(value='not-a-list')


# ---------------------------------------------------------------------------
# parse — no match
# ---------------------------------------------------------------------------

class TestParseNoMatch:
    def test_source_without_placeholder_returned_unchanged(self, parser):
        m = Metadata(name='title', value='My Talk')
        source = 'No placeholders here.'
        result = m.parse(parser=parser, source=source)
        assert result == source

    def test_empty_source_returned_unchanged(self, parser):
        m = Metadata(name='title', value='My Talk')
        result = m.parse(parser=parser, source='')
        assert result == ''


# ---------------------------------------------------------------------------
# parse — with match
# ---------------------------------------------------------------------------

class TestParseWithMatch:
    def test_string_placeholder_replaced(self, parser):
        m = Metadata(name='title', value='My Talk')
        source = 'Title: $title'
        result = m.parse(parser=parser, source=source)
        assert '$title' not in result
        assert 'My Talk' in result

    def test_multiple_placeholders_all_replaced(self, parser):
        m = Metadata(name='title', value='Demo')
        source = '$title and $title again'
        result = m.parse(parser=parser, source=source)
        assert '$title' not in result

    def test_placeholder_inside_fenced_codeblock_not_replaced(self, parser):
        m = Metadata(name='title', value='My Talk')
        source = '```\n$title\n```'
        result = m.parse(parser=parser, source=source)
        # Inside a fenced code block the placeholder must not be expanded
        assert '$title' in result

    def test_list_value_rendered_as_comma_separated(self, parser):
        m = Metadata(name='authors', value=['Alice', 'Bob'])
        source = '$authors'
        result = m.parse(parser=parser, source=source)
        assert '$authors' not in result
        assert 'Alice' in result
        assert 'Bob' in result


# ---------------------------------------------------------------------------
# YAML front-matter parsing (via Presentation)
# ---------------------------------------------------------------------------

class TestYamlFrontMatter:
    def test_metadata_extracted_from_yaml_block(self):
        """Presentation.__get_metadata picks up values from YAML front matter."""
        from matisse.matisse_config import MatisseConfig
        from matisse.presentation import Presentation

        source = (
            '---\n'
            'metadata:\n'
            '  - title: "Test Presentation"\n'
            '  - authors:\n'
            '    - Alice\n'
            '    - Bob\n'
            '---\n'
            '# Chapter\n'
            '## Section\n'
            '### Subsection\n'
            '#### Slide\n'
            'content\n'
        )
        config = MatisseConfig()
        p = Presentation()
        p.parse(config=config, source=source)
        assert p.metadata['title'].value == 'Test Presentation'
        assert 'Alice' in p.metadata['authors'].value

    def test_missing_metadata_keeps_defaults(self):
        from matisse.matisse_config import MatisseConfig
        from matisse.presentation import Presentation

        source = (
            '# Chapter\n'
            '## Section\n'
            '### Subsection\n'
            '#### Slide\ncontent\n'
        )
        config = MatisseConfig()
        p = Presentation()
        p.parse(config=config, source=source)
        assert p.metadata['title'].value == ''
        assert p.metadata['authors'].value == []
