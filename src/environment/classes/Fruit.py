import pygame
from pygame.math import Vector2


class Fruit:
    def __init__(self, pos: Vector2, size: int):
        self.pos = pos
        self.size = size
        self.color = None

    def draw(self, display):
        rect = pygame.Rect(self.pos.x * self.size,
                           self.pos.y * self.size,
                           self.size, self.size)
        pygame.draw.rect(display, self.color, rect)

    def check_available(self, pos_to_check: Vector2):
        return pos_to_check != self.pos


class BadFruit(Fruit):
    def __init__(self, pos: Vector2, size: int):
        super().__init__(pos, size)
        self.color = pygame.Color('red')

    def draw(self, display):
        super().draw(display)


class GoodFruit(Fruit):
    def __init__(self, pos: Vector2, size: int):
        super().__init__(pos, size)
        self.color = pygame.Color('green')

    def draw(self, display):
        super().draw(display)
