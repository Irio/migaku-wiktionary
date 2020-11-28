import os
from tempfile import TemporaryDirectory

import pytest

from migaku_wiktionary.exporter import Exporter


@pytest.fixture(scope="module")
def subject():
    return Exporter([{"term": "Word 1"}])


def test_save_json_content_in_file(subject):
    with TemporaryDirectory() as directory:
        filepath = os.path.join(directory, "file.json")
        subject.save(filepath)
        with open(filepath) as file:
            assert file.read() == '[{"term": "Word 1"}]'
