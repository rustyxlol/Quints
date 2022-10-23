from urllib.request import urlopen

from bs4 import BeautifulSoup

from lcu_change_runes.game_data.all_game_data import get_all_runes
from lcu_change_runes.game_data.structs import Champion, Runes


def get_active_runes(current_url):
    page = urlopen(current_url)
    soup = BeautifulSoup(page, "html.parser")
    images = soup.findAll("img")
    runes = []

    for image in images:
        if "perk" in image["src"] and "grayscale" not in image["src"]:
            if "perkShard" in image["src"]:
                rune = image["src"].split("perkShard/")
                runes.append(rune[1][:4])
            else:
                runes.append(image["alt"])

    runes = runes[:-6]

    return runes


def generate_runes(champion, game_mode):
    all_runes = get_all_runes()
    new_runes = Runes()

    current_url = generate_url(champion.name, game_mode)
    print("Working on", current_url)

    active_runes = get_active_runes(current_url)

    for rune in active_runes[:-3]:
        new_runes.add(all_runes.from_name(rune))
    for rune in active_runes[-3:]:
        new_runes.add(all_runes.from_id(int(rune)))
    print("Generated runes for", champion.name)

    return new_runes


def generate_url(champion_name, game_mode):
    base_url = ""
    if game_mode == "CLASSIC":
        base_url = f"https://www.op.gg/champions/{champion_name}"
    else:
        base_url = f"https://www.op.gg/modes/aram/{champion_name}/build?region=global"
    return base_url


if __name__ == "__main__":
    print(generate_runes(Champion(1, "Annie"), "ARAM"))
