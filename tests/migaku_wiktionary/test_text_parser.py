import pytest

from migaku_wiktionary.text_parser import (
    TextParser,
    remove_anchors,
    remove_audio_examples,
    remove_ref_tags,
    replace_new_lines,
)
from migaku_wiktionary.xml_parser import XMLParser


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


def test_remove_audio_examples():
    text = """{{Aussprache}}
:{{IPA}} {{Lautschrift|ˈvɔxn̩ˌʔɛndə}}
:{{Hörbeispiele}} {{Audio|De-Wochenende.ogg}}, {{Audio|De-at-Wochenende.ogg|spr=at}}

{{Bedeutungen}}"""
    expected = """{{Aussprache}}
:{{IPA}} {{Lautschrift|ˈvɔxn̩ˌʔɛndə}}

{{Bedeutungen}}"""
    assert remove_audio_examples(text) == expected


def test_remove_ref_tags():
    text = ":[1] „Papa war nach Meppen versetzt worden, hatte sich da zwei Zimmer mit Bad gemietet und kam nur noch am ''Wochenende'' nachhause.“<ref>{{Literatur | Autor= Gerhard Henschel | Titel= Kindheitsroman | TitelErg= | Verlag= Hoffmann und Campe | Ort= Hamburg |Jahr= 2004| Seiten= 346.|ISBN= 3-455-03171-4}}</ref>"
    expected = ":[1] „Papa war nach Meppen versetzt worden, hatte sich da zwei Zimmer mit Bad gemietet und kam nur noch am ''Wochenende'' nachhause.“"
    assert remove_ref_tags(text) == expected


def test_parse_integration():
    path = "./tests/fixtures/dewiktionary-latest-pages-meta-current_sample.xml"
    text = XMLParser(path).parse()["Deutsch"][0].text
    subject = TextParser(text)
    with open("./tests/fixtures/output.txt", "w") as file:
        file.write(subject.parse())
