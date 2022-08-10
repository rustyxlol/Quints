from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from constants import CHROME_DRIVER_PATH


class SDriver:
    def __init__(self, url):
        self.url = url

        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(
            executable_path=CHROME_DRIVER_PATH,
            options=self.options,
        )
        self.content = None
        self.soup = None

    def get_url_content(self):
        self.driver.get(self.url)
        return self.driver.page_source.encode("utf-8").strip()

    def parse_url_content(self):
        soup = BeautifulSoup(self.get_url_content(), "html.parser")

        rune_container = soup.find(
            "div",
            class_="rune-trees-container-2 media-query media-query_MOBILE_LARGE__DESKTOP_LARGE",
        )

        full_primary = rune_container.find("div", class_="rune-tree_v2 primary-tree")
        full_secondary = rune_container.find("div", class_="secondary-tree")
        full_shards = rune_container.find(
            "div", class_="rune-tree_v2 stat-shards-container_v2"
        )

        active_primary = full_primary.find_all(
            "div", class_=["perk keystone perk-active", "perk perk-active"]
        )
        active_secondary = full_secondary.find_all("div", class_="perk perk-active")
        active_shards = full_shards.find_all("div", class_="shard shard-active")

        for rune in active_primary:
            print(rune.img["alt"])

        for rune in active_secondary:
            print(rune.img["alt"])

        for rune in active_shards:
            print(rune.img["alt"])

        self.stop_driver()

    def stop_driver(self):
        self.driver.quit()


url = "https://u.gg/lol/champions/nunu/build"

ugg = SDriver(url)
ugg.parse_url_content()
