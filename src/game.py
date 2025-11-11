import sys
import time
from multiprocessing import Queue

import pygame
from pygame import Surface
from pygame.locals import QUIT

from Game.Board import Board
from Game.utils import Directions as D
from Game.utils import Tile as T
from Game.utils import Action as A

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

    return display


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

    # Send to interpreter board + last
    q_to_interpreter.put((board.nrows,
                          board.ncolumns,
                          board.good_fruits,
                          board.bad_fruits,
                          board.snake.head,
                          board.snake.body,
                          None,
                          None))

    display.fill(pygame.Color('black'))
    board.draw(display)
    pygame.display.update()
    sleep_time = 0.001

    while True:
        time.sleep(sleep_time)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        sleep_time = sleep_time / 10000
                    case pygame.K_DOWN:
                        sleep_time = sleep_time * 10000

        move = q_from_agent.get()
        match move:
            case A.UP:
                board.on_event_keypressed(D.UP)
            case A.DOWN:
                board.on_event_keypressed(D.DOWN)
            case A.LEFT:
                board.on_event_keypressed(D.LEFT)
            case A.RIGHT:
                board.on_event_keypressed(D.RIGHT)

        last_tile = board.update()

        # Send to interpreter board + last
        q_to_interpreter.put((board.nrows,
                              board.ncolumns,
                              board.good_fruits,
                              board.bad_fruits,
                              board.snake.head,
                              board.snake.body,
                              move,
                              last_tile))

        if last_tile is T.GAME_OVER:
            print('Game Over')
            print(f'Score: {len(board.snake.body)}')
            break

        display.fill(pygame.Color('black'))
        board.draw(display)

        pygame.display.update()
        FramePerSec.tick(FPS)


def launch_environment_standalone():
    display = init_window()
    board = Board()
    launch_game_standalone(display, board)


def launch_environment_for_agent(q_from_agent: Queue, q_to_interpreter: Queue):
    display = init_window()
    while True:
        board = Board()
        launch_game_for_agent(display, board, q_from_agent, q_to_interpreter)
        del board


if __name__ == "__main__":
    launch_environment_standalone()
