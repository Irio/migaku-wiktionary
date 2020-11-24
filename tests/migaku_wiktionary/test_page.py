import pytest
from lxml import etree

from migaku_wiktionary.page import Page
from migaku_wiktionary.xml_parser import XMLParser


def create_tree(xml):
    return etree.fromstring(xml)


@pytest.fixture(scope="module")
def subject():
    return XMLParser(
        "./tests/fixtures/dewiktionary-latest-pages-meta-current_sample.xml"
    ).parse()[0]


def test_title(subject):
    assert subject.title == "Wochenende"


def test_language_when_detected(subject):
    assert subject.language == "Deutsch"


def test_language_when_not_detected():
    xml = """
    <page>
        <revision>
            <text>== Wochenende ==</text>
        </revision>
    </page>
    """
    subject = Page(create_tree(xml))
    assert subject.language is None
