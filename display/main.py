#!/usr/bin/python3

import pygame
import random
import time
import values
import logging

from multiprocessing import Process, Queue


SCREEN_WIDTH = values.WIDTH
SCREEN_HEIGHT = values.HEIGHT
RED = values.RED
BLUE = values.BLUE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formater = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

file_handler = logging.FileHandler("main.log")
file_handler.setFormatter(formater)

logger.addHandler(file_handler)

class Player:

    def __init__(self, color, number, x, y, queue):
        self.x = x
        self.y = y
        self.color = color
        self.number = number
        self.queue = queue
    
    def move(self):
        while True:
            message = self.queue.get()
            if message == "STOP":
                break
            elif message == "MOVE":
                time.sleep(0.2)  # Simulate movement delay
                self.x += random.randint(-1, 1)
                self.y += random.randint(-1, 1)
                self.queue.put((self.color, self.x, self.y))

def player_process(player):
    player.move()

def update_player_position(data, screen):
    print("Received data:", data)
    color, x, y = data
    print("Extracted values:", color, x, y)
    pygame.draw.circle(screen, color, (x, y), 10)


def main():
    pygame.init()
    logger.info("Pygame initialization done")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("Football Game")
    image = pygame.image.load("pitch.png").convert()
    screen.blit(pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
    pygame.display.flip()

     # Define initial positions of players for blue team
    blue_players = [
        (20, SCREEN_HEIGHT // 2),  # Player 1
        (150, SCREEN_HEIGHT // 6),  # Player 2
        # Add more players as needed...
    ]

    # Define initial positions of players for red team
    red_players = [
        (SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2),  # Player 1
        (SCREEN_WIDTH - 150, SCREEN_HEIGHT // 6),  # Player 2
        # Add more players as needed...
    ]

    logger.info("Updating players positions")

    # Create players for blue team
    blue_processes = []
    blue_queues = []
    for i in range(len(blue_players)):
        queue = Queue()
        blue_queues.append(queue)
        blue_player = Player(BLUE, i + 1, blue_players[i][0], blue_players[i][1], queue)
        process = Process(target=player_process, args=(blue_player,))
        process.start()
        blue_processes.append(process)
        print(f"Started process for blue player {i+1}")
    
    # Create processes for red team players
    red_processes = []
    red_queues = []
    for i in range(len(red_players)):
        queue = Queue()
        red_queues.append(queue)
        red_player = Player(RED, i + 1, *red_players[i], queue)
        process = Process(target=player_process, args=(red_player,))
        process.start()
        red_processes.append(process)
        print(f"Started process for red player {i+1}")

    clock = pygame.time.Clock()
    running = True

    while running:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                for queue in blue_queues + red_queues:
                    queue.put("STOP")
                break
        
        # Send MOVE message to all player processes
        for queue in blue_queues + red_queues:
            queue.put("MOVE")
        
        # Get player positions from queues
        for queue in blue_queues + red_queues:
            while not queue.empty():
                data = queue.get()
                if data == "STOP":
                    break
                if data != "MOVE":
                    update_player_position(data, screen)

        # Update player positions on screen
        #screen.blit(pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        # Draw players here
        pygame.display.flip()
        clock.tick(30)  # Limit frame rate to 20 FPS

    logger.info("Exiting game!")
    pygame.quit()

    # Wait for processes to terminate
    for process in blue_processes + red_processes:
        process.join()


if __name__ == "__main__":
    main()
