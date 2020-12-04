from collections import defaultdict

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

    @property
    def language(self):
        self.create_tree()
        keys = [key for key in self.tree.keys() if key.endswith("lang")]
        if len(keys) > 0:
            return self.tree.attrib[keys[0]]

    def parse(self):
        self.create_tree()
        pages_dict = defaultdict(list)
        for page in self.parse_pages():
            pages_dict[page.language].append(page)
        return pages_dict

    def create_tree(self, xml=None):
        if self.tree is None:
            if xml is None:
                xml = self.read_file()
            self.tree = etree.fromstring(xml)

    def read_file(self):
        xml = ""
        with open(self.filepath) as file:
            xml = file.read()
        return xml

    def parse_pages(self):
        for node in self.tree:
            if node.tag.endswith("page"):
                page = Page(node, self.language)
                if page.contains_term_definition:
                    yield page
