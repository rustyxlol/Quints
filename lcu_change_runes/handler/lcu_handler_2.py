from lcu_change_runes.handler.lcu_apis import LCU_GET


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

    if not current_champion:
        return

    if connection.locals["champion"] != current_champion:
        connection.locals["champion"] = current_champion
        print("Current Champion:", current_champion.name)


async def get_current_champion(connection, event):
    champions = Champions([Champion(1, "Annie")])
    return champions.from_id(event.data)
