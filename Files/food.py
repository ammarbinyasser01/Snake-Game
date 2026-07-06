import random
import pygame
from settings import *

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.respawn([])

    def respawn(self, occupied):
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)

            if (x, y) not in occupied:
                self.position = (x, y)
                break

    def draw(self, screen):
        rect = pygame.Rect(
            self.position[0] * CELL_SIZE,
            self.position[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        pygame.draw.rect(screen, RED, rect)