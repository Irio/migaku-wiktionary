import re

from migaku_wiktionary.text_parser import TextParser

LANGUAGE_TAGS = {
    "de": "Sprache",
    "fr": "langue",
}


class Page:
    """
    Parse contents from a <page> tag.
    """

    def __init__(self, tree, source_language):
        self.tree = tree
        self.source_language = source_language
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
        if self._text_node.text is None:
            return
        language_tag = LANGUAGE_TAGS[self.source_language]
        matches = self._text_node.text.split(f"{{{language_tag}|")
        if len(matches) < 2:
            return
        matches = matches[1].split("}}")
        if len(matches) < 1:
            return
        if re.match(r"\A([a-zA-ZÀ-ž\- ]+)\Z", matches[0]):
            return matches[0]

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
