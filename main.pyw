import requests
import webbrowser
from lcu_driver import Connector
from bs4 import BeautifulSoup

gameType = "CLASSIC"

champion_dict = requests.get(
    "https://ddragon.leagueoflegends.com/cdn/12.12.1/data/en_US/champion.json"
).json()
id_to_name = {data["key"]: data["name"] for _, data in champion_dict["data"].items()}

rdict = requests.get(
    "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json"
).json()
runeDict = {}
for i in rdict:
    runeDict[i["name"]] = i["id"]

rhead = requests.get(
    "http://ddragon.leagueoflegends.com/cdn/11.11.1/data/en_US/runesReforged.json"
).json()
runeHeading = {}
for i in range(5):
    runeHeading[rhead[i]["key"]] = rhead[i]["id"]

subRunes = {
    "The Adaptive Force Shard": 5008,
    "The Attack Speed Shard": 5005,
    "The Scaling CDR Shard": 5007,
    "The Armor Shard": 5002,
    "The Magic Resist Shard": 5003,
    "The Scaling Bonus Health Shard": 5001,
}


def uggParsing(champion):
    perkList = []
    if gameType == "ARAM":
        URL = "https://u.gg/lol/champions/aram/" + champion + "-aram"
    else:
        URL = "https://u.gg/lol/champions/" + champion + "/build"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    y = soup.find(
        "div",
        class_="rune-trees-container-2 media-query media-query_MOBILE_LARGE__DESKTOP_LARGE",
    )
    y = y.find("div", class_="secondary-tree")
    y = y.find("div", class_="perk-style-title").text

    perkList.append(runeHeading[soup.find("div", class_="perk-style-title").text])
    perkList.append(runeHeading[y])

    x = soup.find("div", {"class": "perk keystone perk-active"})
    primary = x.img["alt"]
    primary = primary[13:]
    perkList.append(runeDict[primary])

    primary_tree = soup.find(
        "div",
        class_="rune-trees-container-2 media-query media-query_MOBILE_LARGE__DESKTOP_LARGE",
    )

    for j in primary_tree.find_all("div", class_="perk perk-active"):
        p_tree = j.img["alt"]
        perkList.append(runeDict[p_tree[9:]])

    sub_tree = soup.find(
        "div",
        class_="rune-trees-container-2 media-query media-query_MOBILE_LARGE__DESKTOP_LARGE",
    ).find("div", class_="rune-tree_v2 stat-shards-container_v2")

    for i in sub_tree.find_all("div", class_="shard shard-active"):
        p_tree = i.img["alt"]
        perkList.append(subRunes[p_tree])

    return (perkList, URL)


connector = Connector()


@connector.ready
async def connect(connection):
    print("LCU API is ready to be used.")


async def lobby_type(connection, event):
    return event.data["gameData"]["queue"]["gameMode"]


async def get_details(connection, champion):
    currentRuneData = await connection.request("get", "/lol-perks/v1/currentpage")
    currentRuneData = await currentRuneData.json()
    currentPageId = currentRuneData["id"]
    Perks, URL = uggParsing(champion)
    await connection.request("delete", "/lol-perks/v1/pages" + "/" + str(currentPageId))
    newRune = {
        "primaryStyleId": Perks[0],
        "subStyleId": Perks[1],
        "selectedPerkIds": Perks[2:11],
        "name": champion,
    }
    await connection.request("post", "/lol-perks/v1/pages", data=newRune)
    webbrowser.open(URL)

    print(f"{champion} - RUNES HAVE BEEN UPDATED")


@connector.ws.register(
    "/lol-gameflow/v1/session",
    event_types=(
        "UPDATE",
        "CREATE",
        "DELETE",
    ),
)
async def get_gametype(connection, event):
    if event.data["phase"] == "ChampSelect":
        global gameType
        gameType = await lobby_type(connection, event)


@connector.ws.register(
    "/lol-champ-select/v1/current-champion",
    event_types=(
        "UPDATE",
        "CREATE",
        "DELETE",
    ),
)
async def get_champion(connection, event):
    if event.data:
        currentChamp = await connection.request(
            "get", "/lol-champ-select/v1/current-champion"
        )
        currentChamp = await currentChamp.json()
        currentChamp = id_to_name[str(currentChamp)]

        await get_details(connection, currentChamp)


connector.start()
