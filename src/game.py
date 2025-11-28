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
from Game.StatsDrawer import StatsDrawer

FPS = 60
FramePerSec = pygame.time.Clock()

# Screen information
CELL_SIZE = 40

# Screen update event
SCREEN_UPDATE = pygame.USEREVENT


def init_window(board_size: int = 10):
    pygame.init()

    screen_size = CELL_SIZE * board_size
    display = pygame.display.set_mode((screen_size, screen_size))
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


def launch_game_for_agent_step(display: Surface,
                               board: Board,
                               stats_drawer: StatsDrawer,
                               q_from_agent: Queue,
                               q_to_interpreter: Queue,
                               training_mode: bool):

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

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                q_to_interpreter.put((None,
                                      None,
                                      None,
                                      None,
                                      None,
                                      None,
                                      None,
                                      None))
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
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
                    stats_drawer.update(score=len(board.snake.body))
                    print('Game Over')
                    print(f'Score: {len(board.snake.body)}')
                    return

        display.fill(pygame.Color('black'))
        board.draw(display)

        pygame.display.update()
        FramePerSec.tick(FPS)


def launch_game_for_agent(display: Surface,
                          board: Board,
                          stats_drawer: StatsDrawer,
                          q_from_agent: Queue,
                          q_to_interpreter: Queue,
                          training_mode: bool):

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

    sleep_time = 0
    if training_mode is False:
        sleep_time = 0.3

    while True:
        time.sleep(sleep_time)
        for event in pygame.event.get():
            if event.type == QUIT:
                q_to_interpreter.put((None,
                                      None,
                                      None,
                                      None,
                                      None,
                                      None,
                                      None,
                                      None))
                pygame.quit()
                sys.exit()

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
            stats_drawer.update(score=len(board.snake.body))
            print('Game Over')
            print(f'Score: {len(board.snake.body)}')
            return

        display.fill(pygame.Color('black'))
        board.draw(display)

        pygame.display.update()
        FramePerSec.tick(FPS)


def launch_environment_standalone():
    display = init_window()
    board = Board()
    launch_game_standalone(display, board)


def launch_environment_for_agent(q_from_agent: Queue,
                                 q_to_interpreter: Queue,
                                 training_mode: bool,
                                 step_mode: bool,
                                 num_games: int,
                                 board_size: int):

    display = init_window(board_size)
    stats_drawer = StatsDrawer()

    if step_mode is True:
        game_func = launch_game_for_agent_step
    else:
        game_func = launch_game_for_agent

    for _ in range(num_games):
        board = Board(cell_size=CELL_SIZE,
                      nrows=board_size,
                      ncolumns=board_size)

        game_func(display,
                  board,
                  stats_drawer,
                  q_from_agent,
                  q_to_interpreter,
                  training_mode)

    q_to_interpreter.put((None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None,
                          None))

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    launch_environment_standalone()
