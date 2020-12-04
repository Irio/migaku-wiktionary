import os
from tempfile import TemporaryDirectory

from migaku_wiktionary.wiktionary_dump import WiktionaryDump


def test_save_creates_new_file_with_contents_from_url(mocker):
    with TemporaryDirectory() as directory:
        requests_mock = mocker.patch("migaku_wiktionary.wiktionary_dump.requests")
        requests_mock.get.return_value.content = b"file_contents"
        subject = WiktionaryDump("de", directory)
        file_url = "https://example.com/current.xml.bz2"
        mocker.patch.object(subject, "_file_url", file_url)
        filepath = os.path.join(directory, "current.xml.bz2")
        mocker.patch.object(subject, "_filepath", filepath)
        subject.save()
        with open(filepath, "rb") as file:
            assert file.read() == b"file_contents"


def test_decompress_calls_shell_command(mocker):
    subject = WiktionaryDump("de", "/tmp")
    filepath = "/tmp/current.xml.bz2"
    mocker.patch.object(subject, "_filepath", filepath)
    subprocess_mock = mocker.patch("migaku_wiktionary.wiktionary_dump.subprocess")
    subject.decompress()
    subprocess_mock.run.assert_called_once_with(["bzip2", "-d", filepath])
