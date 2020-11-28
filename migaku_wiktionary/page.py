from migaku_wiktionary.text_parser import TextParser


class Page:
    """
    Parse contents from a <page> tag.
    """

    def __init__(self, tree):
        self.tree = tree
        self._title = None
        self._text = None
        self._text_node = None

    @property
    def title(self):
        self.parse_if_empty(self._title)
        return self._title

    @property
    def language(self):
        self.parse_if_empty(self._text_node)
        strings = self._text_node.text.split("({{Sprache|")
        if len(strings) > 1:
            strings = strings[1].split("}}) ==")
            if len(strings) > 1:
                return strings[0]

    @property
    def text(self):
        self.parse_if_empty(self._text_node)
        if self._text is None:
            self._text = self._text_node.text or ""
            self._text = TextParser(self._text).parse()
        return self._text

    @property
    def contains_term_definition(self):
        patterns = ["Benutzer:", "MediaWiki:", "Wiktionary:"]
        for pattern in patterns:
            if self.title.startswith(pattern):
                return False
        return True

    def parse_if_empty(self, attribute):
        if attribute is None:
            self.parse()

    def parse(self):
        for node in self.tree.getchildren():
            if node.tag.endswith("title"):
                self._title = node.text

            if node.tag.endswith("revision"):
                for child_node in node.getchildren():
                    if child_node.tag.endswith("text"):
                        self._text_node = child_node
