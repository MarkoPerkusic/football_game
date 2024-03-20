import pygame
import random
import asyncio
import values

# Define colors
BLUE = values.BLUE
RED = values.RED

# Define screen dimensions
SCREEN_WIDTH = values.WIDTH
SCREEN_HEIGHT = values.HEIGHT

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


async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Football Game")
    image = pygame.image.load("pitch.png").convert()
    screen.blit(pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
    pygame.display.flip()

    # Create players for blue team
    blue_players = [
        Player(BLUE, 1, 20, SCREEN_HEIGHT // 2),  # Golman
        Player(BLUE, 2, 150, SCREEN_HEIGHT // 6),  # Obrambena linija
        Player(BLUE, 3, 150, SCREEN_HEIGHT // 3 + 40),
        Player(BLUE, 4, 150, (SCREEN_HEIGHT // 2) + SCREEN_HEIGHT // 6 - 40),
        Player(BLUE, 5, 150, (SCREEN_HEIGHT // 2) + (SCREEN_HEIGHT // 3)),
        Player(BLUE, 6, 300, SCREEN_HEIGHT // 6),  # Srednja linija
        Player(BLUE, 7, 300, (SCREEN_HEIGHT // 2) + (SCREEN_HEIGHT // 6) - 40),
        Player(BLUE, 8, 300, SCREEN_HEIGHT // 3 + 40),
        Player(BLUE, 9, 300, (SCREEN_HEIGHT // 2) + (SCREEN_HEIGHT // 3)),
        Player(BLUE, 10, 450, SCREEN_HEIGHT // 3 + 40),  # Napad
        Player(BLUE, 11, 450, (SCREEN_HEIGHT // 2) + (SCREEN_HEIGHT // 6) - 40)
    ]

    # Create players for red team
    red_players = [
        Player(RED, 1, SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2),  # Golman
        Player(RED, 2, SCREEN_WIDTH - 150, SCREEN_HEIGHT // 6),  # Obrambena linija
        Player(RED, 3, SCREEN_WIDTH - 150, SCREEN_HEIGHT // 3 + 40),
        Player(RED, 4, SCREEN_WIDTH - 150, (SCREEN_HEIGHT // 2) + SCREEN_HEIGHT // 6 - 40),
        Player(RED, 5, SCREEN_WIDTH - 150, (SCREEN_HEIGHT // 2) + (SCREEN_HEIGHT // 3)),
        Player(RED, 6, SCREEN_WIDTH - 300, SCREEN_HEIGHT // 6),  # Srednja linija
        Player(RED, 7, SCREEN_WIDTH - 300, (SCREEN_HEIGHT // 2) + (SCREEN_HEIGHT // 6) - 40),
        Player(RED, 8, SCREEN_WIDTH - 300, SCREEN_HEIGHT // 3 + 40),
        Player(RED, 9, SCREEN_WIDTH - 300, (SCREEN_HEIGHT // 2) + (SCREEN_HEIGHT // 3)),
        Player(RED, 10, SCREEN_WIDTH - 450, SCREEN_HEIGHT // 3 + 40),  # Napad
        Player(RED, 11, SCREEN_WIDTH - 450, (SCREEN_HEIGHT // 2) + (SCREEN_HEIGHT // 6) - 40)
    ]

    clock = pygame.time.Clock()
    running = True

    # Start player movement coroutines and collect tasks in lists
    blue_tasks = [asyncio.create_task(player.move()) for player in blue_players]
    red_tasks = [asyncio.create_task(player.move()) for player in red_players]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Start player movement coroutines and collect tasks in lists
        blue_tasks = [asyncio.create_task(player.move()) for player in blue_players]
        red_tasks = [asyncio.create_task(player.move()) for player in red_players]

        # Update player positions
        for player in blue_players + red_players:
            player.draw(screen)

        pygame.display.flip()
        clock.tick(20)  # Limit frame rate to 60 FPS

        # Await tasks to ensure concurrent player movements
        await asyncio.gather(*blue_tasks, *red_tasks)

        # Update pitch image so there is not treaces of previus positions
        screen.blit(pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))


    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
