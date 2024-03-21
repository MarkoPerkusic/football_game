import random
import asyncio
import pygame

class Player:
    def __init__(self, team_color, number, x, y):
        self.team_color = team_color
        self.number = number
        self.x = x
        self.y = y

    async def move(self):
        #while True:
        await asyncio.sleep(0.1)  # Simulate delay
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

    def draw(self, screen):
        pygame.draw.circle(screen, self.team_color, (self.x, self.y), 10)