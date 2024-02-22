import asyncio
from player import Player


async def main():
    width = 100  # Field width
    height = 50  # Field height

    blue_team_name = "Blue"
    red_team_name = "Red"

    # Initialization of Blue Team players
    blue_players = [Player("Blue", i, 0, (i - 1) * 200 / 5) for i in range(1, 12)]

    # Initialization of Red Team players
    red_players = [Player("Red", i, 400, (i - 1) * 200 / 5) for i in range(1, 12)]

    # Start moving players
    blue_player_tasks = [player.move() for player in blue_players]
    red_player_tasks = [player.move() for player in red_players]

    await asyncio.gather(*blue_player_tasks, *red_player_tasks)


if __name__ == "__main__":
    asyncio.run(main())
