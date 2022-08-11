from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from constants import CHROME_DRIVER_PATH
from runes_reforged import RunesReforged


class SParser:
    def __init__(self, url):
        self.url = url

        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(
            executable_path=CHROME_DRIVER_PATH,
            options=self.options,
        )

        self.active_runes = []

    def get_url_content(self):
        self.driver.get(self.url)
        return self.driver.page_source.encode("utf-8").strip()

    def parse_url_content(self):
        soup = BeautifulSoup(self.get_url_content(), "html.parser")

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
            self.active_runes.extend(
                (self.get_active_runes(rune_container, rune_class, rune_sub_class))
            )

        self.map_runes()

        self.stop_driver()

    def get_active_runes(self, rune_container, rune_class, rune_sub_class):
        active_runes = []

        soup_all_runes = rune_container.find("div", class_=rune_class)
        soup_active_runes = soup_all_runes.find_all("div", class_=rune_sub_class)

        for rune in soup_active_runes:
            active_runes.append(rune.img["alt"])

        return active_runes

    def stop_driver(self):
        self.driver.quit()


url = "https://u.gg/lol/champions/nunu/build"

Runes = RunesReforged()
Runes.parse_runes()

ugg = SParser(url)
ugg.parse_url_content()
