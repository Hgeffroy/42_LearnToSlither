import pygame
from pygame import Surface
from pygame.math import Vector2

import random

from Game.utils import Directions as D
from Game.utils import Tile as T


class Snake:
    body: list[D]

    # Need to be init at least 2 away from border
    def __init__(self,
                 pos: Vector2,
                 cell_size: int,
                 size: int = 3):

        self.head = pos
        self.cell_size = cell_size
        self.size = size
        self.body = []

        for _ in range(self.size):
            possible_dir = [d for d in D]
            if len(self.body) > 0:
                possible_dir.remove(self.body[-1].opposite())
            random_dir = random.randint(0, len(possible_dir) - 1)
            self.body.append(D(possible_dir[random_dir]))

        self.dir = self.body[0]

    def move(self, tile_type: T, max_x: int, max_y: int):
        if not self.check_available(self.head + self.dir.value):
            return False

        self.head = self.head + self.dir.value
        self.body.insert(0, self.dir)

        if (self.head.x < 0 or self.head.x > max_x
                or self.head.y < 0 or self.head.y > max_y):
            return False

        if tile_type is not T.GOOD_FRUIT:
            self.body.pop()

        if tile_type is T.BAD_FRUIT:
            if len(self.body) == 0:
                return False
            self.body.pop()

        return True

    def draw(self, display: Surface):
        pos_to_draw = self.head.copy()
        rect = pygame.Rect(pos_to_draw.x * self.cell_size,
                           pos_to_draw.y * self.cell_size,
                           self.cell_size, self.cell_size)
        pygame.draw.rect(display, pygame.Color('orange'), rect)
        i = 0
        for dir in self.body:
            i += 1
            pos_to_draw += dir.opposite().value
            rect = pygame.Rect(pos_to_draw.x * self.cell_size,
                               pos_to_draw.y * self.cell_size,
                               self.cell_size, self.cell_size)
            pygame.draw.rect(display, pygame.Color('yellow'), rect)

    def check_available(self, pos_to_check: Vector2):
        pos_snake = self.head.copy()
        if pos_snake == pos_to_check:
            return False

        for dir in self.body:
            pos_snake += dir.opposite().value
            if pos_snake == pos_to_check:
                return False

        return True

    def debug_display(self):
        print(f'Pos x: {self.head.x}')
        print(f'Pos y: {self.head.y}')
        print(f'Direction: {self.dir}')
        print(f'Body: {self.body}')
