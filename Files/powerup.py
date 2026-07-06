import random
import pygame
from settings import *

class SpeedPowerUp:
    def __init__(self):
        self.position = None
        self.active = False

    def spawn(self, occupied):
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)

            if (x, y) not in occupied:
                self.position = (x, y)
                self.active = True
                break

    def draw(self, screen):
        if not self.active:
            return

        rect = pygame.Rect(
            self.position[0] * CELL_SIZE,
            self.position[1] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        pygame.draw.rect(screen, YELLOW, rect)

    def check_collect(self, snake):
        if self.active and snake.body[0] == self.position:
            self.active = False
            return True
        return False