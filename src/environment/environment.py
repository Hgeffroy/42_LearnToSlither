import pygame
import sys
from pygame.locals import QUIT

from classes.Board import Board
from classes.utils import Directions as D

FPS = 60
FramePerSec = pygame.time.Clock()

# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Screen update event
SCREEN_UPDATE = pygame.USEREVENT


def init_window():
    pygame.init()

    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("LearnToSlither")
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    board = Board()

    return display, board


def launch_game(display, board):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                board.update()
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        board.change_snake_direction(D.UP)
                        break
                    case pygame.K_DOWN:
                        board.change_snake_direction(D.DOWN)
                        break
                    case pygame.K_LEFT:
                        board.change_snake_direction(D.LEFT)
                        break
                    case pygame.K_RIGHT:
                        board.change_snake_direction(D.RIGHT)
                        break

        display.fill(pygame.Color('black'))
        board.draw(display)

        pygame.display.update()
        FramePerSec.tick(FPS)


def main():
    display, board = init_window()
    launch_game(display, board)


if __name__ == "__main__":
    main()
