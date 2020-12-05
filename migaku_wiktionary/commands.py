import logging
import os

import unidecode

from migaku_wiktionary.exporter import Exporter
from migaku_wiktionary.serializer import Serializer
from migaku_wiktionary.wiktionary_dump import WiktionaryDump
from migaku_wiktionary.xml_parser import XMLParser


def download(language, destinationpath):
    # Download the latest dump of a language's Wiktionary.
    dump = WiktionaryDump(language, destinationpath)
    dump.save()
    dump.decompress()


def convert(filepath, destinationpath):
    # Convert a pre-downloaded dump into a Migaku Dictionary.
    def filter_dictionaries(pages_dict):
        pages_dict = {
            language: pages
            for language, pages in pages_dict.items()
            if language is not None and len(pages) > 20_000
        }
        return pages_dict

    def generate_output_path(xml_language, xml_path, output_language, output_folder):
        xml_language = normalize_string(xml_language)
        output_language = normalize_string(output_language)
        basename = f"{xml_language}_{output_language}.json"
        return os.path.join(output_folder, basename)

    def normalize_string(string):
        return unidecode.unidecode(string).lower()

    xml = XMLParser(filepath)
    pages_dict = xml.parse()
    dictionaries = filter_dictionaries(pages_dict)
    logging.info(f"Exporting {len(dictionaries)} dictionaries…")
    for index, (language, pages) in enumerate(dictionaries.items()):
        logging.info(f"Generating and exporting #{index + 1} dictionary {language}…")
        json = Serializer(pages).to_json()
        json_path = generate_output_path(
            xml.language, filepath, language, destinationpath
        )
        Exporter(json).save(json_path)
