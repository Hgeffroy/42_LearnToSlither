import pygame
import sys
from pygame.locals import QUIT

from classes.Board import Board

FPS = 2
FramePerSec = pygame.time.Clock()

# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


def init_window():
    pygame.init()
    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("LearnToSlither")
    board = Board()

    return display, board


def launch_game(display, board):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        board.draw(display)

        pygame.display.update()
        FramePerSec.tick(FPS)


def main():
    display, board = init_window()
    launch_game(display, board)


if __name__ == "__main__":
    main()
