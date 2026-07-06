import random
import pygame
from settings import *

class Obstacles:
    def __init__(self, count=12):
        self.positions = []

        while len(self.positions) < count:
            pos = (
                random.randint(0, COLS - 1),
                random.randint(0, ROWS - 1)
            )

            if pos not in self.positions:
                self.positions.append(pos)

    def draw(self, screen):
        for x, y in self.positions:
            rect = pygame.Rect(
                x * CELL_SIZE,
                y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, GRAY, rect)

    def collision(self, snake):
        if snake.body[0] in self.positions:
            snake.alive = False