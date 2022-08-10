import requests

from constants import LEAGUE_VER

url = f"https://ddragon.leagueoflegends.com/cdn/{LEAGUE_VER}/data/en_US/runesReforged.json"

runes_reforged = requests.get(url).json()

for keystone in runes_reforged:
    print(keystone["id"], keystone["name"])
    for runes in keystone["slots"]:
        for rune in runes["runes"]:
            print("\t", rune["id"], rune["name"])
    print()
