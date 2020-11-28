import pytest

from migaku_wiktionary.text_parser import (TextParser, remove_anchors,
                                           replace_new_lines)


def test_parse_applies_operations_in_order(mocker):
    subject = TextParser("123")
    operations = [
        mocker.MagicMock(side_effect=lambda text: text[:2]),
        mocker.MagicMock(side_effect=lambda text: text[:1]),
        mocker.MagicMock(side_effect=lambda text: ""),
    ]
    mocker.patch("migaku_wiktionary.text_parser.OPERATIONS", operations)
    assert subject.parse() == ""
    assert operations[0].call_args[0] == ("123",)
    assert operations[1].call_args[0] == ("12",)
    assert operations[2].call_args[0] == ("1",)


def test_remove_anchors():
    text = ":[1] meist [[arbeitsfrei|arbeits-]] und [[schulfrei]]es [[Ende]] der [[Woche]]; [[Freitagabend]], [[Samstag]] und [[Sonntag]]"
    expected = ":[1] meist arbeits- und schulfreies Ende der Woche; Freitagabend, Samstag und Sonntag"
    assert remove_anchors(text) == expected


def test_replace_new_lines():
    text = "{{Synonyme}}\n:[1] [[Weekend]]\n\n{{Synonyme}}"
    expected = "{{Synonyme}}<br>:[1] [[Weekend]]<br><br>{{Synonyme}}"
    assert replace_new_lines(text) == expected
