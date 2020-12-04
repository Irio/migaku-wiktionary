import re


def change_page_header_2(text):
    return re.sub(r"=== (.+) ===\n", r"# \1\n", text)


def clear_template_functions(text):
    return re.sub(r"\{\{(?:[^\}]+\|)*([^\}]+)\}\}", r"\1", text)


def mark_section_headers(text):
    return re.sub(r"\n\{\{([a-zA-ZÀ-ž\- ]+)\}\}", r"\n## \1", text)


def remove_anchors(text):
    return re.sub(r"\[\[([a-zA-ZÀ-ž\-]+\|)?([a-zA-ZÀ-ž\-]+)\]\]", r"\2", text)


def remove_audio_examples(text):
    return re.sub(r"\n\:\{\{Hörbeispiele\}\}.+\n", "\n", text)


def remove_contents_after_deep_level_section(text):
    return re.sub(r"\n\n==== .+", "", text, flags=re.DOTALL)


def remove_multiline_template_functions(text):
    return re.sub(r"\{\{.*\n\|(?:\|?.*\n)+\}\}\n{,2}", "", text)


def remove_page_header_1(text):
    return re.sub(r"^== (.+) ==\n", "", text)


def remove_ref_tags(text):
    return re.sub(r"\<ref\>.+\<\/ref\>", "", text)


def replace_new_lines(text):
    return re.sub(r"\n", "<br>", text)


def replace_starting_item_character(text):
    return re.sub(r"\n:", r"\n* ", text)


OPERATIONS = [
    mark_section_headers,
    remove_page_header_1,
    change_page_header_2,
    remove_contents_after_deep_level_section,
    remove_multiline_template_functions,
    remove_anchors,
    remove_audio_examples,
    clear_template_functions,
    remove_ref_tags,
    replace_starting_item_character,
    replace_new_lines,
]


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
