import pygame
from settings import *

class Snake:
    def __init__(self, x, y, color):
        self.body = [(x, y)]
        self.direction = (1, 0)
        self.color = color
        self.grow = False
        self.alive = True

    def move(self):
        if not self.alive:
            return

        head_x, head_y = self.body[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, dx, dy):
        if (-dx, -dy) != self.direction:
            self.direction = (dx, dy)

    def check_wall_collision(self):
        x, y = self.body[0]

        if x < 0 or x >= COLS or y < 0 or y >= ROWS:
            self.alive = False

    def check_self_collision(self):
        if self.body[0] in self.body[1:]:
            self.alive = False

    def eat_food(self, food_pos):
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False

    def draw(self, screen):
        for segment in self.body:
            rect = pygame.Rect(
                segment[0] * CELL_SIZE,
                segment[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)