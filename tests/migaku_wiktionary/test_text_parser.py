import pytest

from migaku_wiktionary.text_parser import (
    TextParser,
    change_page_header_2,
    clear_template_functions,
    mark_section_headers,
    remove_anchors,
    remove_audio_examples,
    remove_contents_after_deep_level_section,
    remove_multiline_template_functions,
    remove_page_header_1,
    remove_ref_tags,
    replace_new_lines,
    replace_starting_item_character,
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


def test_change_page_header_2():
    text = """== Wochenende ({{Sprache|Deutsch}}) ==
=== {{Wortart|Substantiv|Deutsch}}, {{n}} ===
"""
    expected = """== Wochenende ({{Sprache|Deutsch}}) ==
# {{Wortart|Substantiv|Deutsch}}, {{n}}
"""
    assert change_page_header_2(text) == expected


def test_clear_template_functions():
    text = """:Determinativkompositum, zusammengesetzt aus den Substantiven ''Woche'' und ''Ende'' sowie dem Fugenelement ''-n.'' Seit dem 1. Weltkrieg „nach dem Vorbild von englisch {{Ü|en|week end}} auch ›Freizeit von Samstag (Vormittag oder Nachmittag) bis Sonntagabend‹, heute zumeist ›von Freitagnachmittag an‹, auch ›arbeitsfreie Zeit‹“.

{{Aussprache}}
:{{IPA}} {{Laut schrift|ˈvɔxn̩ˌʔɛndə}}"""
    expected = """:Determinativkompositum, zusammengesetzt aus den Substantiven ''Woche'' und ''Ende'' sowie dem Fugenelement ''-n.'' Seit dem 1. Weltkrieg „nach dem Vorbild von englisch week end auch ›Freizeit von Samstag (Vormittag oder Nachmittag) bis Sonntagabend‹, heute zumeist ›von Freitagnachmittag an‹, auch ›arbeitsfreie Zeit‹“.

Aussprache
:IPA ˈvɔxn̩ˌʔɛndə"""
    assert clear_template_functions(text) == expected


def test_replace_starting_item_character():
    text = """{{Bedeutungen}}
:[1] meist [[arbeitsfrei|arbeits-]] und [[schulfrei]]es [[Ende]] der [[Woche]]; [[Freitagabend]], [[Samstag]] und [[Sonntag]]
:[2] meist [[arbeitsfrei|arbeits-]] und [[schulfrei]]es [[Ende]] der [[Woche]]; [[Freitagabend]], [[Samstag]] und [[Sonntag]]

{{Abkürzungen}}
:[22] [[WE]]

{{Aussprache}}
:{{IPA}} {{Lautschrift|ˈvɔxn̩ˌʔɛndə}}"""
    expected = """{{Bedeutungen}}
* [1] meist [[arbeitsfrei|arbeits-]] und [[schulfrei]]es [[Ende]] der [[Woche]]; [[Freitagabend]], [[Samstag]] und [[Sonntag]]
* [2] meist [[arbeitsfrei|arbeits-]] und [[schulfrei]]es [[Ende]] der [[Woche]]; [[Freitagabend]], [[Samstag]] und [[Sonntag]]

{{Abkürzungen}}
* [22] [[WE]]

{{Aussprache}}
* {{IPA}} {{Lautschrift|ˈvɔxn̩ˌʔɛndə}}"""
    assert replace_starting_item_character(text) == expected


def test_remove_contents_after_deep_level_section():
    text = """{{Wortbildungen}}
:[1] [[Wochenendabsenkung]], [[Wochenendarbeit]], [[Wochenendausflug]], [[Wochenendausgabe]], [[Wochenendbeilage]], [[Wochenendbeziehung]], [[Wochenenddienst]], [[Wochenendehe]], [[Wochenendeinkauf]], [[Wochenendgrundstück]], [[Wochenendfahrt]], [[Wochenendhaus]], [[Wochenendlaune]], [[Wochenendreise]], [[Wochenendseminar]], [[Wochenendstimmung]], [[Wochenendticket]]

==== {{Übersetzungen}} ====
{{Ü-Tabelle|Ü-links=
*{{sq}}: [1] {{Ü|sq|fundjavë}} {{f}}
*{{ar}}: [1] {{Üt|ar|نهاية الأسبوع|nhạyẗ ạlạ̉sbwʿ}} {{f}}

{{Referenzen}}
:[1] {{Wikipedia}}"""
    expected = """{{Wortbildungen}}
:[1] [[Wochenendabsenkung]], [[Wochenendarbeit]], [[Wochenendausflug]], [[Wochenendausgabe]], [[Wochenendbeilage]], [[Wochenendbeziehung]], [[Wochenenddienst]], [[Wochenendehe]], [[Wochenendeinkauf]], [[Wochenendgrundstück]], [[Wochenendfahrt]], [[Wochenendhaus]], [[Wochenendlaune]], [[Wochenendreise]], [[Wochenendseminar]], [[Wochenendstimmung]], [[Wochenendticket]]"""
    assert remove_contents_after_deep_level_section(text) == expected


def test_remove_page_header_1():
    text = """== Wochenende ({{Sprache|Deutsch}}) ==
=== {{Wortart|Substantiv|Deutsch}}, {{n}} ==="""
    expected = """=== {{Wortart|Substantiv|Deutsch}}, {{n}} ==="""
    assert remove_page_header_1(text) == expected


def test_remove_multiline_template_functions():
    text = """=== {{Wortart|Substantiv|Deutsch}}, {{n}} ===

{{Deutsch Substantiv Übersicht
|Genus=n
|Nominativ Singular=Wochenende
|Nominativ Plural=Wochenenden
|Genitiv Singular=Wochenendes
|Genitiv Plural=Wochenenden
|Dativ Singular=Wochenende
|Dativ Plural=Wochenenden
|Akkusativ Singular=Wochenende
|Akkusativ Plural=Wochenenden
}}

{{Worttrennung}}
:Wo·chen·en·de, {{Pl.}} Wo·chen·en·den"""
    expected = """=== {{Wortart|Substantiv|Deutsch}}, {{n}} ===

{{Worttrennung}}
:Wo·chen·en·de, {{Pl.}} Wo·chen·en·den"""
    assert remove_multiline_template_functions(text) == expected


def test_mark_section_headers():
    text = """
{{Herkunft}}
:[[Determinativkompositum]], zusammengesetzt aus den Substantiven ''[[Woche]]'' und ''[[Ende]]'' sowie dem [[Fugenelement]] ''[[-n]].'' Seit dem 1. Weltkrieg „nach dem Vorbild von englisch {{Ü|en|weekend}} auch ›Freizeit von Samstag (Vormittag oder Nachmittag) bis Sonntagabend‹, heute zumeist ›von Freitagnachmittag an‹, auch ›arbeitsfreie Zeit‹“.&lt;ref&gt; Hermann Paul: ''Deutsches Wörterbuch'', Stichwort „Woche“.&lt;/ref&gt;

{{Synonyme}}
:[1] [[Weekend]]"""
    expected = """
## Herkunft
:[[Determinativkompositum]], zusammengesetzt aus den Substantiven ''[[Woche]]'' und ''[[Ende]]'' sowie dem [[Fugenelement]] ''[[-n]].'' Seit dem 1. Weltkrieg „nach dem Vorbild von englisch {{Ü|en|weekend}} auch ›Freizeit von Samstag (Vormittag oder Nachmittag) bis Sonntagabend‹, heute zumeist ›von Freitagnachmittag an‹, auch ›arbeitsfreie Zeit‹“.&lt;ref&gt; Hermann Paul: ''Deutsches Wörterbuch'', Stichwort „Woche“.&lt;/ref&gt;

## Synonyme
:[1] [[Weekend]]"""
    assert mark_section_headers(text) == expected


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
