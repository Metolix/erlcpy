import asyncio

from erlcpy import AsyncClient


async def main() -> None:
    async with AsyncClient.from_env() as client:
        server = await client.get_server(players=True)
        for player in server.players or []:
            print(player.username)


asyncio.run(main())
