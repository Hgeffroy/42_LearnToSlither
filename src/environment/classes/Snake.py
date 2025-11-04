import pygame
from pygame.math import Vector2
from classes.utils import Directions as D
import random


class Snake:
    body: list[D] = []

    # Need to be init at least 2 away from border
    def __init__(self,
                 pos: Vector2,
                 cell_size: int,
                 size: int = 3):

        self.head = pos
        self.cell_size = cell_size
        self.size = size

        for _ in range(self.size):
            possible_dir = [d for d in D]
            if len(self.body) > 0:
                possible_dir.remove(self.body[-1].opposite())
            random_dir = random.randint(0, len(possible_dir) - 1)
            self.body.append(D(possible_dir[random_dir]))

        self.dir = self.body[0]

    def draw(self, display):
        pos_to_draw = self.head.copy()
        rect = pygame.Rect(pos_to_draw.x * self.cell_size,
                           pos_to_draw.y * self.cell_size,
                           self.cell_size, self.cell_size)
        pygame.draw.rect(display, pygame.Color('yellow'), rect)
        for dir in self.body:
            pos_to_draw += dir.value
            rect = pygame.Rect(pos_to_draw.x * self.cell_size,
                               pos_to_draw.y * self.cell_size,
                               self.cell_size, self.cell_size)
            pygame.draw.rect(display, pygame.Color('yellow'), rect)

    def check_available(self, pos_to_check: Vector2):
        pos_snake = self.head.copy()
        if pos_snake == pos_to_check:
            return False

        for dir in self.body:
            pos_snake += dir.value
            if pos_snake == pos_to_check:
                return False

        return True
