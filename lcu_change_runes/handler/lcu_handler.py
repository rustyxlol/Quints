from lcu_driver import Connector

from lcu_change_runes.handler.lcu_utils import summoner_greeting
from lcu_change_runes.parser.champions import Champions
from lcu_change_runes.parser.runes_reforged import RunesReforged
from lcu_change_runes.parser.ugg import UGGParser

RunesRef = RunesReforged()
RunesRef.cache_rune_data()

champions = Champions()
champions.load_champ_data_source()
champions.cache_champ_data()

parse_ugg = UGGParser()

connector = Connector()

# Fired when LCU API is ready to be used
@connector.ready
async def connect(connection):
    """Estbalish connection with league client"""
    connection.locals["game_mode"] = "CLASSIC"
    connection.locals["current_champion_name"] = None
    connection.locals["current_champion_key"] = 1
    connection.locals["last_game_id"] = 999999

    req_summoner_details = await connection.request(
        "get", "/lol-summoner/v1/current-summoner"
    )

    print("\nSuccesfully Initiated Connection!\n")
    if req_summoner_details.status != 200:
        print("Please login into your account")
    else:
        summoner_details = await req_summoner_details.json()
        summoner_greeting(summoner_details)
    print("\n")


# Obtain game type first(classic/aram)
@connector.ws.register("/lol-gameflow/v1/session", event_types=("UPDATE",))
async def entered_champ_select(connection, event):
    if event.data["phase"] == "ChampSelect":
        # if event.data["gameData"]["gameId"] != connection.locals["last_game_id"]:
        # connection.locals["last_game_id"] = event.data["gameData"]["gameId"]
        await current_game_type(connection, event)


async def current_game_type(connection, event):
    connection.locals["game_mode"] = event.data["gameData"]["queue"]["gameMode"]
    # print(f"Joined {connection.locals['game_mode']} game type")


# Obtain currently selected champion
@connector.ws.register(
    "/lol-champ-select/v1/current-champion",
    event_types=(
        "CREATE",
        "UPDATE",
        "DELETE",
    ),
)
async def locked_champion(connection, event):
    champion_key = event.data
    current_champion = champions.get_champ_name_by_key(champion_key)
    if current_champion is not None:
        if current_champion != connection.locals["current_champion_name"]:
            connection.locals["current_champion_key"] = champion_key
            connection.locals["current_champion_name"] = current_champion
            print("Locked in:", current_champion, "\n")
            await change_runes(connection)


async def change_runes(connection):
    current_rune_page_id = await get_current_rune_page(connection)
    await delete_current_rune_page(connection, current_rune_page_id)
    ugg_runes = await get_ugg_runes(connection)
    await create_new_rune_page(connection, ugg_runes)


# Change runes
# Get current rune page
# Delete it
# Create a new rune page and put runes there
async def get_current_rune_page(connection):
    req_current_rune_page = await connection.request("get", "/lol-perks/v1/currentpage")
    current_rune_page_source = await req_current_rune_page.json()
    current_rune_page_name = current_rune_page_source["name"]
    current_rune_page_id = current_rune_page_source["id"]
    print("Current rune page:", current_rune_page_name)
    return current_rune_page_id


# {8437: 'Grasp of the Undying',
# 8401: 'Shield Bash', 8444: 'Second Wind', # 8242: 'Unflinching',
# 9111: # 'Triumph', 9104: 'Legend: Alacrity',
# 5005: 'The # Attack Speed Shard', 5003: 'The Magic Resist Shard', 5001: 'The Scaling Bonus Health Shard'}
async def delete_current_rune_page(connection, id):
    print("Deleting current rune page...")
    await connection.request("delete", "/lol-perks/v1/pages/" + str(id))


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


# Fired when League Client is closed (or disconnected from websocket)
@connector.close
async def disconnect(_):
    print("The client has been closed!")
    await connector.stop()


# Start the connector
connector.start()
