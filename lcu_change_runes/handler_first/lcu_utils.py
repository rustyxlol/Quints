from lcu_change_runes.parser.champions import Champions
from lcu_change_runes.parser.runes_reforged import RunesReforged
from lcu_change_runes.parser.ugg import UGGParser

RunesRef = RunesReforged()

champions = Champions()

parse_ugg = UGGParser()


def summoner_greeting(summoner_details):
    print(summoner_details["displayName"], "Connected")
    print(
        f"Summoner Level Completion: {summoner_details['percentCompleteForNextLevel']}% "
        f"({summoner_details['summonerLevel']})"
    )


async def change_runes(connection):
    current_rune_page_id = await get_current_rune_page(connection)
    await delete_current_rune_page(connection, current_rune_page_id)
    ugg_runes = await get_ugg_runes(connection)
    await create_new_rune_page(connection, ugg_runes)


async def get_current_rune_page(connection):
    req_current_rune_page = await connection.request("get", "/lol-perks/v1/currentpage")
    current_rune_page_source = await req_current_rune_page.json()
    try:
        current_rune_page_name = current_rune_page_source["name"]
        current_rune_page_id = current_rune_page_source["id"]
        print("Current rune page:", current_rune_page_name)
        return current_rune_page_id
    except KeyError:
        print("No rune page found!")


async def delete_current_rune_page(connection, rune_page_id):
    print("Deleting current rune page...")
    await connection.request("delete", "/lol-perks/v1/pages/" + str(rune_page_id))


async def create_new_rune_page(connection, runes):
    print("Creating new rune page...\n")
    rune_sequence_ids = [rune[0] for rune in runes]
    primary_keystone = rune_sequence_ids[0]
    secondary_keystone = rune_sequence_ids[1]
    active_rune_ids = rune_sequence_ids[2:]

    new_rune_body = {
        "name": connection.locals["current_champion_name"] + " Runes",
        "primaryStyleId": primary_keystone,
        "subStyleId": secondary_keystone,
        "selectedPerkIds": active_rune_ids,
    }
    await connection.request("post", "/lol-perks/v1/pages", data=new_rune_body)
    print("Runes successfully updated!\n")


async def get_ugg_runes(connection):
    print("Obtaining runes from u.gg...")
    ugg_url = "https://u.gg/lol/champions"
    if connection.locals["game_mode"] == "ARAM":
        ugg_url += "/aram/" + connection.locals["current_champion_name"] + "-aram"
    else:
        ugg_url += "/" + connection.locals["current_champion_name"] + "/build"

    active_runes = RunesRef.map_rune_name_to_id(parse_ugg.get_active_runes(ugg_url))

    return active_runes


async def current_game_type(connection, event):
    connection.locals["game_mode"] = event.data["gameData"]["queue"]["gameMode"]
