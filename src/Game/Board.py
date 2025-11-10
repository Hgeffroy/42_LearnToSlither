import random

from pygame import Surface
from pygame.math import Vector2

from Game.Snake import Snake
from Game.Fruit import GoodFruit, BadFruit
from Game.utils import Directions as D
from Game.utils import Tile as T


class Board:
    good_fruits: list[GoodFruit]
    bad_fruits: list[BadFruit]

    def __init__(self,
                 cell_size: int = 40,
                 nrows: int = 10,
                 ncolumns: int = 10,
                 nb_good_fruits: int = 2,
                 nb_bad_fruits: int = 1):

        self.cell_size = cell_size
        self.nrows = nrows
        self.ncolumns = ncolumns
        self.nb_good_fruits = nb_good_fruits
        self.nb_bad_fruits = nb_bad_fruits
        self.good_fruits = []
        self.bad_fruits = []
        self.best_score = 0

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

    def on_event_keypressed(self, dir: D):
        self.snake.dir = dir

    def update(self):
        snake_next_pos = self.snake.head + self.snake.dir.value

        tile = T.IDLE
        for f in self.good_fruits:
            if not f.check_available(snake_next_pos):
                tile = T.GOOD_FRUIT
                self.good_fruits.remove(f)

        for f in self.bad_fruits:
            if not f.check_available(snake_next_pos):
                tile = T.BAD_FRUIT
                self.bad_fruits.remove(f)

        if not self.snake.move(tile, self.ncolumns - 1, self.nrows - 1):
            score = len(self.snake.body) + 1
            if score > self.best_score:
                self.best_score = score
            print(f'Best score: {self.best_score}')
            return T.GAME_OVER

        if tile is T.GOOD_FRUIT:
            self._generate_good_fruit()
        if tile is T.BAD_FRUIT:
            self._generate_bad_fruit()

        return tile

    def draw(self, display: Surface):
        for f in self.good_fruits:
            f.draw(display)
        for f in self.bad_fruits:
            f.draw(display)
        self.snake.draw(display)

    def debug_display(self):
        print('Snake')
        self.snake.debug_display()
        for f in self.good_fruits:
            print('Good fruit:')
            f.debug_display()
        for f in self.bad_fruits:
            print('Bad fruit:')
            f.debug_display()
