import random
import pygame
from pygame.math import Vector2

from classes.Snake import Snake
from classes.Fruit import GoodFruit, BadFruit
from classes.utils import Directions as D


class Board:
    good_fruits: list[GoodFruit] = []
    bad_fruits: list[BadFruit] = []

    def __init__(self,
                 cell_size=40,
                 nrows=10,
                 ncolumns=10,
                 nb_good_fruits=2,
                 nb_bad_fruits=1):

        self.cell_size = cell_size
        self.nrows = nrows
        self.ncolumns = ncolumns
        self.nb_good_fruits = nb_good_fruits
        self.nb_bad_fruits = nb_bad_fruits

        snake_x = random.randint(2, self.ncolumns - 3)
        snake_y = random.randint(2, self.nrows - 3)
        self.snake = Snake(Vector2(snake_x, snake_y), cell_size)

        for _ in range(nb_bad_fruits):
            self._generate_bad_fruit()
        for _ in range(nb_good_fruits):
            self._generate_good_fruit()

    def _generate_good_fruit(self):
        available = False
        while available is False:
            x = random.randint(0, self.ncolumns - 1)
            y = random.randint(0, self.nrows - 1)
            pos = Vector2(x, y)
            available = self._check_tile_empty(pos)

        self.good_fruits.append(GoodFruit(pos, self.cell_size))

    def _generate_bad_fruit(self):
        available = False
        while available is False:
            x = random.randint(0, self.ncolumns - 1)
            y = random.randint(0, self.nrows - 1)
            pos = Vector2(x, y)
            available = self._check_tile_empty(pos)

        self.bad_fruits.append(BadFruit(Vector2(x, y), self.cell_size))

    def _check_tile_empty(self, pos: Vector2):
        empty = True
        for f in self.good_fruits:
            empty = empty and f.check_available(pos)
        for f in self.bad_fruits:
            empty = empty and f.check_available(pos)
        empty = empty and self.snake.check_available(pos)

        return empty

    def on_event_keypressed(self, event):
        match event.key:
            case pygame.K_UP:
                new_dir = D.UP
                if self.snake.dir != new_dir.opposite():
                    self.snake.dir = new_dir
            case pygame.K_DOWN:
                new_dir = D.DOWN
                if self.snake.dir != new_dir.opposite():
                    self.snake.dir = new_dir
            case pygame.K_LEFT:
                new_dir = D.LEFT
                if self.snake.dir != new_dir.opposite():
                    self.snake.dir = new_dir
            case pygame.K_RIGHT:
                new_dir = D.RIGHT
                if self.snake.dir != new_dir.opposite():
                    self.snake.dir = new_dir

    def update(self):
        snake_next_pos = self.snake.head + self.snake.dir.value

        tile = None
        for f in self.good_fruits:
            if not f.check_available(snake_next_pos):
                tile = type(f)
                self.good_fruits.remove(f)

        for f in self.bad_fruits:
            if not f.check_available(snake_next_pos):
                tile = type(f)
                self.bad_fruits.remove(f)

        if not self.snake.move(tile, self.ncolumns - 1, self.nrows - 1):
            return False

        if tile is GoodFruit:
            self._generate_good_fruit()
        if tile is BadFruit:
            self._generate_bad_fruit()

        return True

    def draw(self, display):
        for f in self.good_fruits:
            f.draw(display)
        for f in self.bad_fruits:
            f.draw(display)
        self.snake.draw(display)
