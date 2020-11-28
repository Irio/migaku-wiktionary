import pytest
from lxml import etree

from migaku_wiktionary.page import Page
from migaku_wiktionary.xml_parser import XMLParser


def create_tree(xml):
    return etree.fromstring(xml)


@pytest.fixture(scope="module")
def subject():
    path = "./tests/fixtures/dewiktionary-latest-pages-meta-current_sample.xml"
    return [page for page in XMLParser(path).parse()][0]


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


def test_text():
    xml = """
    <page>
        <revision>
            <text>1. This is a word.</text>
        </revision>
    </page>
    """
    subject = Page(create_tree(xml))
    assert subject.text == "1. This is a word."
