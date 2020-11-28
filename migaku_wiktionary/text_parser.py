import re


def remove_anchors(text):
    return re.sub(r"\[\[([a-zA-ZÀ-ž\-]+\|)?([a-zA-ZÀ-ž\-]+)\]\]", r"\2", text)


def replace_new_lines(text):
    return re.sub(r"\n", "<br>", text)


OPERATIONS = [replace_new_lines, remove_anchors]


class TextParser:
    """
    Parser for the MediaWiki markup-annotated[1] contents of a
    Wiktionary page.

    [1]: https://www.mediawiki.org/wiki/Specs/wikitext/1.0.0
    """

    def __init__(self, text):
        self.text = text

    def parse(self):
        parsed_text = self.text
        for operation in OPERATIONS:
            parsed_text = operation(parsed_text)
        return parsed_text
