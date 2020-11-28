import re


def remove_anchors(text):
    # return text
    return re.sub(r"\[\[([a-zA-ZÀ-ž\-]+\|)?([a-zA-ZÀ-ž\-]+)\]\]", r"\2", text)


def remove_audio_examples(text):
    return re.sub(r"\n\:\{\{Hörbeispiele\}\}.+\n", "\n", text)


def remove_ref_tags(text):
    return re.sub(r"\<ref\>.+\<\/ref\>", "", text)


def replace_new_lines(text):
    return re.sub(r"\n", "<br>", text)


OPERATIONS = [remove_anchors, remove_audio_examples, remove_ref_tags, replace_new_lines]


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
