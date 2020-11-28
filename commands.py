import os

from migaku_wiktionary.exporter import Exporter
from migaku_wiktionary.serializer import Serializer
from migaku_wiktionary.xml_parser import XMLParser


def download():
    # Download the latest dump of a language's Wiktionary.
    pass


def convert(filepath, destinationpath):
    # Convert a pre-downloaded dump into a Migaku Dictionary.
    pages = XMLParser(filepath).parse()
    json = Serializer(pages).to_json()
    destinationpath = os.path.join(
        destinationpath, os.path.basename(filepath).replace(".xml", ".json")
    )
    Exporter(json).save(destinationpath)
