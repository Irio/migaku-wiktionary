import pytest

from migaku_wiktionary.serializer import Serializer


@pytest.fixture
def subject(mocker):
    return Serializer(
        [
            mocker.MagicMock(title="Word 1", text="Text 1"),
            mocker.MagicMock(title="Word 2", text="Text 2"),
        ]
    )


def test_to_json_maps_pages_into_dictionaries(subject):
    assert subject.to_json() == [
        {
            "term": "Word 1",
            "altterm": "",
            "pronunciation": "",
            "definition": "Text 1",
            "pos": "",
            "examples": "",
            "audio": "",
        },
        {
            "term": "Word 2",
            "altterm": "",
            "pronunciation": "",
            "definition": "Text 2",
            "pos": "",
            "examples": "",
            "audio": "",
        },
    ]
