from lcu_change_runes.game_data.all_game_data import get_all_champions
from lcu_change_runes.handler.lcu_apis import LCU_DELETE, LCU_GET, LCU_POST
from lcu_change_runes.parser.ugg import UGGParser, generate_runes

_ugg = UGGParser()


async def get_summoner_data(connection):
    print("Initiating Connection...\n")
    status, summoner = await LCU_GET(connection, "/lol-summoner/v1/current-summoner")

    if status == 200:
        print_summoner_data(summoner)
    else:
        print("Please run league client first")


def print_summoner_data(summoner):
    print("\tConnected\n")
    print(f"Summoner Name:     {summoner['displayName']}")
    print(f"Summoner Level:    {summoner['summonerLevel']}")
    print(f"Level Completion:  {summoner['percentCompleteForNextLevel']}%")


async def initialize_variables(connection):
    connection.locals["game_mode"] = ""
    connection.locals["champion"] = None


async def update_game_mode(connection, event):
    in_champ_select = await is_champ_select_phase(connection, event)
    if in_champ_select:
        game_mode = event.data["gameData"]["queue"]["gameMode"]
        print("Joined:", game_mode)
        connection.locals["game_mode"] = game_mode


async def is_champ_select_phase(_, event):
    if event.data["phase"] == "ChampSelect":
        return True
    return False


#############################################################
#               CHAMPION SELECT CHAMPION LISTENER           #
#############################################################


async def update_current_champion(connection, event):
    current_champion = await get_current_champion(connection, event)

    if current_champion:
        if connection.locals["champion"] != current_champion:
            connection.locals["champion"] = current_champion
            print("Current Champion:", current_champion.name)


async def get_current_champion(_, event):
    champions = get_all_champions()
    return champions.from_id(event.data)


#################################################################
#                         RUNES                                 #
#################################################################
async def update_rune_page(connection):
    await delete_current_rune_page(connection)
    await create_new_rune_page(connection)


async def delete_current_rune_page(connection):
    status, current_page = await LCU_GET(connection, "/lol-perks/v1/currentpage")
    await LCU_DELETE(connection, "/lol-perks/v1/pages/" + str(current_page["id"]))


async def create_new_rune_page(connection):
    ugg_runes = generate_runes(
        _ugg, connection.locals["champion"], connection.locals["game_mode"]
    )
    runes = ugg_runes.runes
    payload = {
        "name": connection.locals["champion"].name + " Runes",
        "primaryStyleId": runes[0].id,
        "subStyleId": runes[1].id,
        "selectedPerkIds": ugg_runes.all_rune_ids()[2:],
    }
    await LCU_POST(connection, "/lol-perks/v1/pages", payload)
