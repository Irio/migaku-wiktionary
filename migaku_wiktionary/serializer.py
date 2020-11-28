class Serializer:
    """
    Serialize a collection of Page's into a Migaku Dictionary JSON.
    """

    def __init__(self, pages):
        self.pages = pages

    def to_json(self):
        json = []
        for page in self.pages:
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
        return json
