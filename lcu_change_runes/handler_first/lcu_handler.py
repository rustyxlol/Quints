from lcu_driver import Connector

from lcu_change_runes.handler_first.lcu_utils import (
    champions,
    change_runes,
    current_game_type,
    summoner_greeting,
)

connector = Connector()


@connector.ready
async def connect(connection):
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


@connector.ws.register("/lol-gameflow/v1/session", event_types=("UPDATE",))
async def entered_champ_select(connection, event):
    if event.data["phase"] == "ChampSelect":
        await current_game_type(connection, event)


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


@connector.close
async def disconnect(_):
    print("The client has been closed!")
    await connector.stop()


connector.start()
