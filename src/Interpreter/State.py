from pygame.math import Vector2

from Game.Board import Board
from Game.Snake import Snake
from Game.Fruit import Fruit
from Game.utils import Directions


class State:
    up: list[chr]
    down: list[chr]
    left: list[chr]
    right: list[chr]
    _head: Vector2

    def __init__(self,
                 board: Board,
                 good_fruits: list[Fruit],
                 bad_fruits: list[Fruit],
                 snake: Snake,
                 snake_body: list[Directions]):

        self._head = board.snake.head
        self._get_walls(board)
        self._get_fruits(good_fruits, bad_fruits)
        self._get_snake(snake_body)

    def _get_walls(self, board: Board):
        self.up = ['0'] * int(self._head.y) + ['W']
        self.down = ['0'] * int(board.nrows - 1 - self._head.y) + ['W']
        self.left = ['0'] * int(self._head.x) + ['W']
        self.right = ['0'] * int(board.ncolumns - 1 - self._head.x) + ['W']

    def _get_fruits(self, good_fruits: list[Fruit], bad_fruits: list[Fruit]):
        for f in bad_fruits:
            if f.pos.x == self._head.x:
                row_diff = int(f.pos.y - self._head.y)
                if row_diff == 0:
                    raise Exception('Head and fruit on the' +
                                    ' same tile in interpreter')
                elif row_diff > 0:
                    self.down[row_diff - 1] = 'R'
                else:
                    self.up[(row_diff + 1) * -1] = 'R'

            if f.pos.y == self._head.y:
                col_diff = int(f.pos.x - self._head.x)
                if col_diff == 0:
                    raise Exception('Head and fruit on the' +
                                    ' same tile in interpreter')
                elif col_diff > 0:
                    self.right[col_diff - 1] = 'R'
                else:
                    self.left[(col_diff + 1) * -1] = 'R'

        for f in good_fruits:
            if f.pos.x == self._head.x:
                row_diff = int(f.pos.y - self._head.y)
                if row_diff == 0:
                    raise Exception('Head and fruit on the' +
                                    ' same tile in interpreter')
                elif row_diff > 0:
                    self.down[row_diff - 1] = 'G'
                else:
                    self.up[(row_diff + 1) * -1] = 'G'

            if f.pos.y == self._head.y:
                col_diff = int(f.pos.x - self._head.x)
                if col_diff == 0:
                    raise Exception('Head and fruit on the' +
                                    ' same tile in interpreter')
                elif col_diff > 0:
                    self.right[col_diff - 1] = 'G'
                else:
                    self.left[(col_diff + 1) * -1] = 'G'

    def _get_snake(self, snake_body: list[Directions]):
        pos = self._head.copy()
        for dir in snake_body:
            pos += dir.opposite().value
            if pos.x == self._head.x:
                row_diff = int(pos.y - self._head.y)
                if row_diff == 0:
                    raise Exception('Snake head and body on the' +
                                    ' same tile in interpreter')
                elif row_diff > 0:
                    self.down[row_diff - 1] = 'S'
                else:
                    self.up[(row_diff + 1) * -1] = 'S'

            if pos.y == self._head.y:
                col_diff = int(pos.x - self._head.x)
                if col_diff == 0:
                    raise Exception('Snake head and body on the' +
                                    ' same tile in interpreter')
                elif col_diff > 0:
                    self.right[col_diff - 1] = 'S'
                else:
                    self.left[(col_diff + 1) * -1]

    def display(self):
        print(f'Up: {self.up}')
        print(f'Down: {self.down}')
        print(f'Left: {self.left}')
        print(f'Right: {self.right}')
