from multiprocessing import Queue

from Interpreter.State import State


def launch_interpreter_for_agent(q_from_game: Queue,
                                 q_to_agent_reward: Queue,
                                 q_to_agent_state: Queue):

    while True:
        (board,
         good_fruits,
         bad_fruits,
         snake,
         snake_body,
         last_tile) = q_from_game.get()
        state = State(board, good_fruits, bad_fruits, snake, snake_body)
        state.display()


def launch_interpreter_standalone():
    pass


if __name__ == "__main__":
    launch_interpreter_standalone()
