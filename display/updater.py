import pygame

class Updater:

    def __init__(self, X, Y):
        self.X = X
        self.Y = Y


    def move_players(self, screen, image, data):
        """
        Function that moves players on the pitch
        """
        screen.blit(pygame.transform.scale(image, (self.X, self.Y)), (0,0))
        print(f"data: {data}")
        for i,j,k in data:
            print(f"i: {i} j: {j} k: {k}")
            pygame.draw.circle(screen, k, [i, j], 10)