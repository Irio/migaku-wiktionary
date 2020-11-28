import json


class Exporter:
    """
    Create a Data Package for a Migaku Dictionary JSON.
    """

    def __init__(self, json_content):
        self.json_content = json_content

    def save(self, destinationpath):
        with open(destinationpath, "w+") as file:
            json.dump(self.json_content, file)
