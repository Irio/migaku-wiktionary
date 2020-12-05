import logging
import os
import subprocess
from urllib.parse import urljoin

import requests
from requests_html import HTMLSession

INDEX_URL = "https://dumps.wikimedia.org/backup-index.html"


class WiktionaryDump:
    """
    Download a Wiktionary dump from official sources.
    """

    def __init__(self, language, destinationpath):
        self.language = language
        self.destinationpath = destinationpath
        self._file_url = None
        self._filepath = None

    @property
    def file_url(self):
        if self._file_url is None:
            self._fetch_file_attributes()
        return self._file_url

    @property
    def filepath(self):
        if self._filepath is None:
            self._fetch_file_attributes()
            self._filepath = os.path.join(self.destinationpath, self._filename)
        return self._filepath

    def save(self):
        with open(self.filepath, "wb") as file:
            logging.info("Downloading it…")
            response = requests.get(self.file_url)
            file.write(response.content)

    def decompress(self):
        logging.info("Decompressing it…")
        subprocess.run(["bzip2", "-d", self.filepath])

    def _fetch_file_attributes(self):
        logging.info("Fetching the URL of the latest dump…")
        session = HTMLSession()
        response = session.get(INDEX_URL)
        anchors = response.html.xpath(f"//*[text()='{self.language}wiktionary']")
        self._fail_if_empty(anchors)
        language_index_url = urljoin(INDEX_URL, anchors[0].attrs["href"])
        response = session.get(language_index_url)
        anchors = response.html.xpath(
            "//*[contains(text(),'-pages-meta-current.xml.bz2')]"
        )
        self._fail_if_empty(anchors)
        self._file_url = urljoin(INDEX_URL, anchors[0].attrs["href"])
        self._filename = os.path.basename(self._file_url)

    def _fail_if_empty(self, anchors):
        if len(anchors) == 0:
            raise RuntimeError(f"Could not find a dump for language `{language}`.")
