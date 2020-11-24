from lxml import etree


class XMLParser:
    """
    Parse contents from a Wiktionary dump.

    Wiktionary has a few different types of dumps[1]. Although this class might
    be able to parse others, it is intended for the ones containing only the
    latest revision of wiki pages. Their names currently follow this pattern:

    [language code]wiktionary-[timestamp]-pages-meta-current.xml

    [1]: https://dumps.wikimedia.org/backup-index.html
    """

    def __init__(self, filepath="data/dewiktionary-latest-pages-meta-current.xml"):
        self.filepath = filepath
        self.tree = None

    def parse(self):
        self.read_file()

    def read_file(self):
        xml = ""
        with open(self.filepath) as file:
            xml = file.read()
        self.tree = etree.fromstring(xml)
