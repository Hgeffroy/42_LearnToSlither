from multiprocessing import Queue

from Interpreter.State import State
from Game.utils import Tile as T


REWARD = {
    T.GAME_OVER: -10,
    T.BAD_FRUIT: -3,
    T.IDLE: 1,
    T.GOOD_FRUIT: 3
}


def launch_interpreter_for_agent(q_from_game: Queue,
                                 q_to_agent_reward: Queue,
                                 q_to_agent_state: Queue):

    while True:
        (nrows,
         ncolumns,
         good_fruits,
         bad_fruits,
         snake_head,
         snake_body,
         last_tile) = q_from_game.get()

        state = State(nrows,
                      ncolumns,
                      good_fruits,
                      bad_fruits,
                      snake_head,
                      snake_body)

        state.display()
        q_to_agent_state.put((state.up, state.down, state.left, state.right))

        if last_tile is None:
            q_to_agent_reward.put(None)
        else:
            q_to_agent_reward.put(REWARD[last_tile])


def launch_interpreter_standalone():
    pass


if __name__ == "__main__":
    launch_interpreter_standalone()
