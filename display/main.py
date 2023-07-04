#!/usr/bin/python3

import pygame, random
import values
from updater import Updater
import logging


X = values.X
Y = values.Y
RED = values.RED
BLUE = values.BLUE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formater = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

file_handler = logging.FileHandler("main.log")
file_handler.setFormatter(formater)

logger.addHandler(file_handler)

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


def main():
    pygame.init()
    logger.info("Pygame initialization done")

    screen = pygame.display.set_mode((X, Y))

    pygame.display.set_caption("GAME")
    image = pygame.image.load("pitch.png").convert()
    screen.blit(pygame.transform.scale(image, (X,Y)), (0,0))
    pygame.display.flip()

    logger.info("Updating players positions")
    players = [(300, 100, BLUE), (300, 500, BLUE), (100, 300, RED), (500, 300, RED),
                (300, 200, BLUE), (300, 600, BLUE), (200, 300, RED), (600, 300, RED)]


    running = True
    update = Updater(X, Y)
    while running:
        pygame.time.delay(300)
        positions = elixir_mock(players)
        logger.info(f"{positions}")

        update.move_players(screen, image, positions)
        pygame.display.flip()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    logger.info("Exiting game!")
    pygame.quit()


if __name__ == "__main__":
    main()
