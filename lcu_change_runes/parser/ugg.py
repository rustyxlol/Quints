"""Scraper for UGG"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from lcu_change_runes.parser.champions import Champions
from lcu_change_runes.parser.constants import CHROME_DRIVER_PATH
from lcu_change_runes.parser.runes_reforged import RunesReforged


class UGGParser:
    """Parser for UGG"""

    def __init__(self):

        self.options = Options()
        self.options.headless = True
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(
            service=Service(CHROME_DRIVER_PATH),
            options=self.options,
        )
        self.rune_container = None

    def get_url_content(self, url):
        """Returns page source from URL

        Args:
            url: URL of target page

        Returns:
            Page source
        """
        self.driver.get(url)
        return self.driver.page_source

    def get_active_runes(self, url):
        """Returns active runes from given URL

        Args:
            url: URL of target page

        Returns:
            Dictionary of active runes with id and rune name pair
        """
        soup = BeautifulSoup(self.get_url_content(url), "html.parser")
        active_runes = []

        self.rune_container = soup.find(
            "div",
            class_="rune-trees-container-2 media-query media-query_MOBILE_LARGE__DESKTOP_LARGE",
        )
        rune_main_classes = [
            "rune-tree_v2 primary-tree",
            "secondary-tree",
            "rune-tree_v2 stat-shards-container_v2",
        ]
        rune_sub_classes = [
            ["perk keystone perk-active", "perk perk-active"],
            "perk perk-active",
            "shard shard-active",
        ]

        rune_paths = self.get_rune_paths()
        active_runes.extend(rune_paths)

        for (rune_class, rune_sub_class) in zip(rune_main_classes, rune_sub_classes):
            active_runes.extend((self.parse_active_runes(rune_class, rune_sub_class)))

        return active_runes

    def parse_active_runes(self, rune_class, rune_sub_class):
        """Parse active runes from u.gg URL

        Args:
            rune_container: div containing rune information
            rune_class: div containing primary rune information
            rune_sub_class: div containing secondary rune information

        Returns:
            Active runes
        """
        parsed_active_runes = []

        soup_all_runes = self.rune_container.find("div", class_=rune_class)
        soup_parsed_active_runes = soup_all_runes.find_all("div", class_=rune_sub_class)

        for rune in soup_parsed_active_runes:
            parsed_active_runes.append(rune.img["alt"])

        return parsed_active_runes

    def get_rune_paths(self):
        rune_paths = []
        for rune_path in self.rune_container.find_all("div", class_="perk-style-title"):
            rune_paths.append(rune_path.text)
        return rune_paths

    def stop_driver(self):
        """Stop the selenium driver"""
        self.driver.quit()


def generate_url(champion_name, game_mode):
    base_url = "https://u.gg/lol/champions/"
    if game_mode == "CLASSIC":
        base_url += f"{champion_name}/build"
    else:
        base_url += f"aram/{champion_name}-aram"
    return base_url


if __name__ == "__main__":
    Runes = RunesReforged()
    Runes.cache_rune_data()

    champions = Champions()
    champions.cache_champ_data()

    _ugg = UGGParser()

    for game_mode in ("CLASSIC", "ARAM"):
        for champion in list(champions.champions_cache.values())[:1]:
            current_url = generate_url(champion, game_mode)
            print("Working on", current_url)
            active_runes = Runes.map_rune_name_to_id(_ugg.get_active_runes(current_url))
            print("Generated runes for", champion)
            print(active_runes)
            print(_ugg.get_rune_paths())

    print(dict(active_runes))
    _ugg.stop_driver()
