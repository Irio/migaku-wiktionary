import logging

from migaku_wiktionary import ProgressBar


class Serializer:
    """
    Serialize a collection of Page's into a Migaku Dictionary JSON.
    """

    def __init__(self, pages):
        self.pages = pages

    def to_json(self):
        json = []
        logging.info(f"Parsing definitions…")
        bar = ProgressBar(max_value=len(self.pages), redirect_stdout=True)
        for index, page in enumerate(self.pages):
            bar.update(index)
            json.append(
                {
                    "term": page.title,
                    "altterm": "",
                    "pronunciation": "",
                    "definition": page.text,
                    "pos": "",
                    "examples": "",
                    "audio": "",
                }
            )
        bar.finish()
        return json
