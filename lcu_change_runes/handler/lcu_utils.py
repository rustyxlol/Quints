def summoner_greeting(summoner_details):
    print(summoner_details["displayName"], "Connected")
    print(
        f"Summoner Level Completion: {summoner_details['percentCompleteForNextLevel']}% "
        f"({summoner_details['summonerLevel']})"
    )
