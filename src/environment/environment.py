import pygame
import sys
from pygame.locals import QUIT

from classes.Board import Board

FPS = 60
FramePerSec = pygame.time.Clock()

# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

# Screen update event
SCREEN_UPDATE = pygame.USEREVENT


def init_window():
    pygame.init()

    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("LearnToSlither")
    pygame.time.set_timer(SCREEN_UPDATE, 300)

    board = Board()

    return display, board


def launch_game(display, board):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                if not board.update():
                    print('Game Over')
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                board.on_event_keypressed(event)

        display.fill(pygame.Color('black'))
        board.draw(display)

        pygame.display.update()
        FramePerSec.tick(FPS)


def main():
    display, board = init_window()
    launch_game(display, board)


if __name__ == "__main__":
    main()
