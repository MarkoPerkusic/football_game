import asyncio
import random


class Player:
    def __init__(self, team_name, number, x, y):
        self.team_name = team_name
        self.number = number
        self.x = x
        self.y = y

    async def move(self):
        while True:
            await asyncio.sleep(1)  # Simulate time between moves
            self.x += random.choice([-1, 0, 1])
            self.y += random.choice([-1, 0, 1])
            print(f"Player {self.number} from {self.team_name} team moved to ({self.x}, {self.y})")
