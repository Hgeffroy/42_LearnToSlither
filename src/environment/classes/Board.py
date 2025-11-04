import random
from pygame.math import Vector2

from classes.Snake import Snake
from classes.Fruit import GoodFruit, BadFruit


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
        # Verifier qu'il n'y a rien d'autre sur la case
        available = False
        while available is False:
            x = random.randint(0, self.ncolumns - 1)
            y = random.randint(0, self.nrows - 1)
            pos = Vector2(x, y)
            available = True
            for f in self.good_fruits:
                available = available and f.check_available(pos)
            for f in self.bad_fruits:
                available = available and f.check_available(pos)
            available = self.snake.check_available(pos)

        self.good_fruits.append(GoodFruit(pos, self.cell_size))

    def _generate_bad_fruit(self):
        # Verifier qu'il n'y a rien d'autre sur la case
        x = random.randint(0, self.ncolumns - 1)
        y = random.randint(0, self.nrows - 1)
        self.bad_fruits.append(BadFruit(Vector2(x, y), self.cell_size))

    def draw(self, display):
        for f in self.good_fruits:
            f.draw(display)
        for f in self.bad_fruits:
            f.draw(display)
        self.snake.draw(display)
