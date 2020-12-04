import pytest

from migaku_wiktionary.xml_parser import XMLParser


@pytest.fixture(scope="module")
def subject():
    return XMLParser(
        "./tests/fixtures/dewiktionary-latest-pages-meta-current_sample.xml"
    )


def test_parse_calls_internal_functions(subject, mocker):
    mocker.patch.object(subject, "create_tree")
    mocker.patch.object(subject, "parse_pages")
    subject.parse()
    subject.create_tree.assert_called_once()
    subject.parse_pages.assert_called_once()


def test_parse_returns_pages(subject, mocker):
    page_mock = mocker.patch("migaku_wiktionary.xml_parser.Page")
    page_mock.return_value.language = "Deutsch"
    pages = subject.parse()
    assert dict(pages) == {"Deutsch": [page_mock.return_value]}


def test_create_tree_stores_tree_in_instance_var(subject, mocker):
    subject.create_tree()
    assert subject.tree.tag == "{http://www.mediawiki.org/xml/export-0.10/}mediawiki"


def test_parse_pages_returns_a_page_for_each_page_element(subject):
    subject.create_tree()
    pages = [page for page in subject.parse_pages()]
    assert len(pages) == 1


def test_language(subject):
    assert subject.language == "de"
