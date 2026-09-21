from prcpy import Client

with Client.from_env() as client:
    server = client.get_server(players=True, staff=True)
    print(f"{server.name}: {server.current_players}/{server.max_players}")

    for player in server.players or []:
        print(player.username, player.team)
