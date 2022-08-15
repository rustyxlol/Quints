"""Champion Manager"""
import requests

from lcu_change_runes.parser.constants import URL_CHAMPIONS


class Champions:
    """Champion Manager"""

    def __init__(self):
        self.champions_source = {}
        self.champions_cache = {}
        self.load_champ_data_source()

    def load_champ_data_source(self):
        """Gets all champions from data dragon CDN"""
        self.champions_source = requests.get(URL_CHAMPIONS).json()

    def cache_champ_data(self):
        """Converts champions data from data dragon into key-value pairs of champion key and name"""
        for _, champion in self.champions_source["data"].items():
            self.champions_cache[int(champion["key"])] = champion["id"]

    def get_champ_name_by_key(self, key):
        """Gets champion name by provided champion key(integer)

        Args:
            key: Champion's unique integer identifier

        Returns:
            Champion's Name
        """
        if key not in self.champions_cache:
            return None
        return self.champions_cache[key]

    def get_champ_info_by_id(self, champion_id):
        """Gets all information of a champion

        Args:
            champion_id: unique string identifier of a champion

        Returns:
            Champion Information JSON
        """
        return self.champions_source["data"][champion_id]


if __name__ == "__main__":
    champions = Champions()
    champions.cache_champ_data()
    print(champions.get_champ_name_by_key(200))
    print(champions.get_champ_info_by_id("Annie"))
