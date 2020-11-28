from lxml import etree

from migaku_wiktionary.page import Page


class XMLParser:
    """
    Parse contents from a Wiktionary dump.

    Wiktionary has a few different types of dumps[1]. Although this class might
    be able to parse others, it is intended for the ones containing only the
    latest revision of wiki pages. Their names currently follow this pattern:

    [language code]wiktionary-[timestamp]-pages-meta-current.xml

    [1]: https://dumps.wikimedia.org/backup-index.html
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.tree = None

    def parse(self, language=None):
        self.create_tree()
        return self.parse_pages(language)

    def create_tree(self, xml=None):
        if xml is None:
            xml = self.read_file()
        self.tree = etree.fromstring(xml)

    def read_file(self):
        xml = ""
        with open(self.filepath) as file:
            xml = file.read()
        return xml

    def parse_pages(self, filtered_language=None):
        for node in self.tree:
            if node.tag.endswith("page"):
                page = Page(node)
                has_selected_language = (
                    filtered_language is None or page.language == filtered_language
                )
                if page.contains_term_definition and has_selected_language:
                    yield page
