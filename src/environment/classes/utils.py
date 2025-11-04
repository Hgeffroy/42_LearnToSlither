from enum import Enum
from pygame.math import Vector2


class Directions(Enum):
    UP = Vector2(0, 1)
    DOWN = Vector2(0, -1)
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
