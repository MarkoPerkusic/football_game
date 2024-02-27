#!/usr/bin/python3

import pygame, random, asyncio
import values
from updater import Updater
import logging
import queue  # Import Queue for shared data structure

# Define a global queue for shared data
data_queue = queue.Queue()

X = 800
Y = 500
RED = values.RED
BLUE = values.BLUE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formater = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

file_handler = logging.FileHandler("main.log")
file_handler.setFormatter(formater)

logger.addHandler(file_handler)


class Player:
    def __init__(self, team_name, number, x, y):
        self.team_name = team_name
        self.number = number
        self.x = x
        self.y = y
        self.running = False

    async def move(self):
        await asyncio.sleep(1)  # Simulate time between moves
        self.x += random.choice([-5, 0, 5])
        self.y += random.choice([-1, 0, 1])
        print(f"Player {self.number} from {self.team_name} team moved to ({self.x}, {self.y})")
        data_queue.put((self.x, self.y, self.team_name))
        print("Player movement stopped.")


def elixir_mock(players):
    """
    Function that mocks data provided from elixir part
    """

    logger.info("Mocking elixir values")
    res = []
    for i in players:
        (x, y, c) = i
        x = x + random.randrange(-50, 60, 5)
        y = y + random.randrange(-50, 60, 5)
        res.append((x, y, c))

    return res

def update(screen, image, data):
    screen.blit(pygame.transform.scale(image, (X, Y)), (0,0))
    print(f"data: {data}")
    for i,j,k in data:
        print(f"i: {i} j: {j} k: {k}")
        pygame.draw.circle(screen, k, [i, j], 10)


async def main():
    pygame.init()
    logger.info("Pygame initialization done")

    screen = pygame.display.set_mode((X, Y))

    pygame.display.set_caption("GAME")
    image = pygame.image.load("pitch.png").convert()
    screen.blit(pygame.transform.scale(image, (X,Y)), (0,0))
    pygame.display.flip()

    logger.info("Updating players positions")
    #players = [(300, 100, BLUE), (300, 500, BLUE), (100, 300, RED), (500, 300, RED),
    #            (300, 200, BLUE), (300, 600, BLUE), (200, 300, RED), (600, 300, RED)]

    #player = [Player("Blue", 2, 100, 100)]
    player = Player("Blue", 2, 100, 100)
    player_task = asyncio.create_task(player.move())


    running = True
    while running:
        pygame.time.delay(100)
        player_task = asyncio.create_task(player.move())

        # Read from the shared data queue to obtain the latest position data
        try:
            data = data_queue.get_nowait()
            print(f"{data=}")
        except queue.Empty:
            pass
        else:
            update(screen, image, [data])  # Update screen with latest position data
            pygame.display.flip()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                player.running = running

        await player_task 

    logger.info("Exiting game!")
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
