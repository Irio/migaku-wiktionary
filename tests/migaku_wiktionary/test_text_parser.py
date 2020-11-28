import pytest

from migaku_wiktionary.text_parser import TextParser


@pytest.fixture(scope="module")
def subject():
    return TextParser("123")


def test_parse_applies_operations_in_order(subject, mocker):
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
