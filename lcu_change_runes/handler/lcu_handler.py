from lcu_change_runes.game_data.all_game_data import get_all_champions
from lcu_change_runes.handler.lcu_apis import LCU_DELETE, LCU_GET, LCU_POST
from lcu_change_runes.parser.ugg import UGGParser

ugg = UGGParser()


async def get_summoner_data(connection):
    print("\nInitiating Connection...\n")
    status, summoner = await LCU_GET(connection, "/lol-summoner/v1/current-summoner")

    if status == 200:
        print_summoner_data(summoner)
    else:
        print("Please run league client first")


async def initialize_variables(connection):
    connection.locals["game_mode"] = ""
    connection.locals["champion"] = None


async def update_game_mode(connection, event):
    in_champ_select = await is_champ_select_phase(connection, event)
    if in_champ_select:
        game_mode = event.data["gameData"]["queue"]["gameMode"]
        connection.locals["game_mode"] = game_mode


async def is_champ_select_phase(_, event):
    if event.data["phase"] == "ChampSelect":
        return True
    return False


#############################################################
#               CHAMPION SELECT CHAMPION LISTENER           #
#############################################################


async def get_current_champion(_, event):
    champions = get_all_champions()
    return champions.from_id(event.data)


async def update_current_champion_and_runes(connection, event):
    current_champion = await get_current_champion(connection, event)

    if not current_champion:
        return
    if connection.locals["champion"] == current_champion:
        return

    connection.locals["champion"] = current_champion
    print_game_details(connection)

    await update_rune_page(connection)


#############################################################
#                           RUNES                           #
#############################################################


async def update_rune_page(connection):
    await delete_current_rune_page(connection)
    await create_new_rune_page(connection)


async def delete_current_rune_page(connection):
    status, current_page = await LCU_GET(connection, "/lol-perks/v1/currentpage")
    if status == 200:
        await LCU_DELETE(connection, "/lol-perks/v1/pages/" + str(current_page["id"]))
    else:
        print("Rune page did not exist 🤔", status, current_page)


async def create_new_rune_page(connection):
    ugg_runes = ugg.generate_runes(
        connection.locals["champion"], connection.locals["game_mode"]
    )
    runes = ugg_runes.runes
    payload = {
        "name": connection.locals["champion"].name + " Runes",
        "primaryStyleId": runes[0].id,
        "subStyleId": runes[1].id,
        "selectedPerkIds": ugg_runes.all_rune_ids()[2:],
    }

    await LCU_POST(connection, "/lol-perks/v1/pages", payload)


def print_summoner_data(summoner):
    print("Connected\n")
    print(f"Summoner Name:     {summoner['displayName']}")
    print(f"Summoner Level:    {summoner['summonerLevel']}")
    print(f"Level Completion:  {summoner['percentCompleteForNextLevel']}%")


def print_game_details(connection):
    print()
    print("Entered Champion Select")
    print("Locked in:", connection.locals["champion"].name)
    print()
