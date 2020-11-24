import pytest

from migaku_wiktionary.xml_parser import XMLParser


@pytest.fixture(scope="module")
def subject():
    return XMLParser(
        "./tests/fixtures/dewiktionary-latest-pages-meta-current_sample.xml"
    )


def test_parse_calls_internal_functions(mocker, subject):
    mocker.patch.object(subject, "read_file")
    subject.parse()
    subject.read_file.assert_called_once()


def test_read_file_stores_tree_in_instance_var(mocker, subject):
    subject.read_file()
    assert subject.tree.tag == "{http://www.mediawiki.org/xml/export-0.10/}mediawiki"
