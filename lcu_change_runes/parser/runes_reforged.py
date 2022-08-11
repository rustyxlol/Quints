import requests

from constants import URL_RUNES_REFORGED


class RunesReforged:
    def __init__(self):
        self.runes = {}

    def get_runes(self):
        return requests.get(URL_RUNES_REFORGED).json()

    def parse_runes(self):
        all_runes = self.get_runes()
        for rune_path in all_runes:
            self.runes[rune_path["id"]] = rune_path["name"]
            for runes in rune_path["slots"]:
                for rune in runes["runes"]:
                    self.runes[rune["id"]] = rune["name"]


if __name__ == "__main__":
    runes = RunesReforged()
    runes.parse_runes()

    print(runes.runes)
