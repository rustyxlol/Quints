from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from constants import CHROME_DRIVER_PATH
from runes_reforged import RunesReforged


class SParser:
    """Parser for UGG"""

    def __init__(self, url):
        self.url = url

        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(
            executable_path=CHROME_DRIVER_PATH,
            options=self.options,
        )

    def get_url_content(self):
        self.driver.get(self.url)
        return self.driver.page_source.encode("utf-8").strip()

    def get_active_runes(self):
        soup = BeautifulSoup(self.get_url_content(), "html.parser")
        active_runes = []

        rune_container = soup.find(
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

        for (rune_class, rune_sub_class) in zip(rune_main_classes, rune_sub_classes):
            active_runes.extend(
                (self.parse_active_runes(rune_container, rune_class, rune_sub_class))
            )

        return active_runes

    def parse_active_runes(self, rune_container, rune_class, rune_sub_class):
        """Parse active runes from u.gg URL

        Args:
            rune_container: div containing rune information
            rune_class: div containing primary rune information
            rune_sub_class: div containing secondary rune information

        Returns:
            Active runes
        """
        parsed_active_runes = []

        soup_all_runes = rune_container.find("div", class_=rune_class)
        soup_parsed_active_runes = soup_all_runes.find_all("div", class_=rune_sub_class)

        for rune in soup_parsed_active_runes:
            parsed_active_runes.append(rune.img["alt"])

        return parsed_active_runes

    def stop_driver(self):
        """Stop the selenium driver"""
        self.driver.quit()


if __name__ == "__main__":
    url = "https://u.gg/lol/champions/nunu/build"

    Runes = RunesReforged()
    Runes.parse_all_runes()

    ugg = SParser(url)
    active_runes = Runes.map_to_id(ugg.get_active_runes())
    ugg.stop_driver()
