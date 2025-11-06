import sys
from multiprocessing import Queue

import pygame
from pygame import Surface
from pygame.locals import QUIT

from Game.Board import Board
from Game.utils import Directions as D
from Game.utils import Tile as T

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


def launch_game_standalone(display: Surface, board: Board):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                if board.update() is T.GAME_OVER:
                    print('Game Over')
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        board.on_event_keypressed(D.UP)
                    case pygame.K_DOWN:
                        board.on_event_keypressed(D.DOWN)
                    case pygame.K_LEFT:
                        board.on_event_keypressed(D.LEFT)
                    case pygame.K_RIGHT:
                        board.on_event_keypressed(D.RIGHT)

        display.fill(pygame.Color('black'))
        board.draw(display)

        pygame.display.update()
        FramePerSec.tick(FPS)


def launch_game_for_agent(display: Surface,
                          board: Board,
                          q_from_agent: Queue,
                          q_to_interpreter: Queue):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        move = q_from_agent.get()
        match move:
            case 'UP':
                board.on_event_keypressed(D.UP)
            case 'DOWN':
                board.on_event_keypressed(D.DOWN)
            case 'LEFT':
                board.on_event_keypressed(D.LEFT)
            case 'RIGHT':
                board.on_event_keypressed(D.RIGHT)

        last_tile = board.update()
        if last_tile is T.GAME_OVER:
            print('Game Over')
            board.debug_display()
            pygame.quit()
            sys.exit()

        # Send to interpreter board + last
        q_to_interpreter.put((board.nrows,
                              board.ncolumns,
                              board.good_fruits,
                              board.bad_fruits,
                              board.snake.head,
                              board.snake.body,
                              last_tile))

        display.fill(pygame.Color('black'))
        board.draw(display)

        pygame.display.update()
        FramePerSec.tick(FPS)


def launch_environment_standalone():
    display, board = init_window()
    launch_game_standalone(display, board)


def launch_environment_for_agent(q_from_agent: Queue, q_to_interpreter: Queue):
    display, board = init_window()
    launch_game_for_agent(display, board, q_from_agent, q_to_interpreter)


if __name__ == "__main__":
    launch_environment_standalone()
