import requests

from constants import URL_RUNES_REFORGED


class RunesReforged:
    def __init__(self):
        self.runes = {
            5008: "The Adaptive Force Shard",
            5005: "The Attack Speed Shard",
            5007: "The Scaling CDR Shard",
            5002: "The Armor Shard",
            5003: "The Magic Resist Shard",
            5001: "The Scaling Bonus Health Shard",
        }

    def get_runes(self):
        return requests.get(URL_RUNES_REFORGED).json()

    def parse_all_runes(self):
        all_runes = self.get_runes()
        for rune_path in all_runes:
            self.runes[rune_path["id"]] = rune_path["name"]
            for runes in rune_path["slots"]:
                for rune in runes["runes"]:
                    self.runes[rune["id"]] = rune["name"]

    def map_to_id(self, raw_runes):
        mapped_runes = {}
        for rune in raw_runes:
            for rune_id, rune_name in self.runes.items():
                if rune_name in rune:
                    mapped_runes[rune_id] = rune_name
        return mapped_runes


if __name__ == "__main__":
    runes = RunesReforged()
    runes.parse_all_runes()

    print(runes.runes)
