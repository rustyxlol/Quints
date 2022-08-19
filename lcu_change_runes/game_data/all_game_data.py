from lcu_change_runes.game_data.apis import API_GET
from lcu_change_runes.game_data.structs import Champion, Champions, Rune, Runes


def get_latest_version():
    version_data = API_GET("http://ddragon.leagueoflegends.com/api/versions.json")
    return version_data[0]


def get_all_champions():
    champions = Champions()
    champions_data = API_GET(
        f"http://ddragon.leagueoflegends.com/cdn/{get_latest_version()}/data/en_US/champion.json"
    )
    for _, champion in champions_data["data"].items():
        champions.add(Champion(champion["key"], champion["id"]))

    return champions


def get_all_runes():
    runes_data = API_GET(
        "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json"
    )

    runes = Runes()

    # Add rune paths
    for rune_id, rune_name in get_rune_paths().items():
        runes.add(Rune(rune_id, rune_name))

    # Add rune slots
    for rune in runes_data:
        runes.add(Rune(rune["id"], rune["name"]))

    return runes


def get_rune_paths():
    runes_data = API_GET(
        f"https://ddragon.leagueoflegends.com/cdn/{get_latest_version()}/data/en_US/runesReforged.json"
    )
    runes = {}
    for rune in runes_data:
        runes[rune["id"]] = rune["key"]
    return runes


if __name__ == "__main__":
    print(get_all_runes())
