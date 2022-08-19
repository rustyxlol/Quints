"""Rune Manager for scrapers"""
import requests

from lcu_change_runes.parser.constants import MISSING_SHARDS, URL_RUNES_REFORGED


class RunesReforged:
    """Rune management"""

    def __init__(self):
        self.runes_source = {}
        self.runes_cache = {}
        self.load_rune_data_source()
        self.cache_rune_data()

    def load_rune_data_source(self):
        """Gets all runes from data dragon CDN

        Returns:
            JSON of all runes
        """
        self.runes_source = requests.get(URL_RUNES_REFORGED).json()

    def cache_rune_data(self):
        """Converts runes from data dragon into key-value pairs of id and rune name"""

        for rune_path in self.runes_source:
            self.runes_cache[rune_path["id"]] = rune_path["name"]
            for runes in rune_path["slots"]:
                for rune in runes["runes"]:
                    self.runes_cache[rune["id"]] = rune["name"]

        self.runes_cache.update(MISSING_SHARDS)

    def map_rune_name_to_id(self, raw_runes):
        """FOR SCRAPERS
        Standardizes and maps runes to their respective ids/names

        Args:
            raw_runes: Rune names obtained from scraping a website

        Returns:
            list of (rune_id, rune_name) tuples
        """
        mapped_runes = []
        for rune in raw_runes:
            for rune_id, rune_name in self.runes_cache.items():
                if rune_name in rune:
                    mapped_runes.append((rune_name, rune_id))
        return mapped_runes


if __name__ == "__main__":
    _runes = RunesReforged()
    print(_runes.runes_cache)
