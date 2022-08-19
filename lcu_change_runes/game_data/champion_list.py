import requests

from lcu_change_runes.game_data.structs import Rune, Runes

response = requests.get(
    "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json"
)
rune_data = response.json()

runes = Runes()
for rune in rune_data:
    runes.add(Rune(rune["id"], rune["name"]))

print(runes.from_name("Eyeball collection"))
