from enum import Enum
from pygame.math import Vector2


class Directions(Enum):
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)

    def opposite(self):
        if self is Directions.UP:
            return Directions.DOWN
        if self is Directions.DOWN:
            return Directions.UP
        if self is Directions.LEFT:
            return Directions.RIGHT
        if self is Directions.RIGHT:
            return Directions.LEFT


class Tile(Enum):
    GAME_OVER = 0
    GOOD_FRUIT = 1
    BAD_FRUIT = 2
    IDLE = 3

    def convert_from_char(c: chr):
        match c:
            case 'S':
                return Tile.GAME_OVER
            case 'W':
                return Tile.GAME_OVER
            case 'G':
                return Tile.GOOD_FRUIT
            case 'R':
                return Tile.BAD_FRUIT

        raise Exception(f'Could not convert character {c} into tile')


class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
