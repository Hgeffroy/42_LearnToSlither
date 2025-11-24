from multiprocessing import Queue

from Interpreter.State import State
from Interpreter.Rewarder import Rewarder


def launch_interpreter_for_agent(q_from_game: Queue,
                                 q_to_agent_reward: Queue,
                                 q_to_agent_state: Queue):

    rewarder = Rewarder()

    while True:
        (nrows,
         ncolumns,
         good_fruits,
         bad_fruits,
         snake_head,
         snake_body,
         last_move,
         last_tile) = q_from_game.get()

        if nrows is None:
            q_to_agent_state.put((None, None, None, None))
            break

        state = State(nrows,
                      ncolumns,
                      good_fruits,
                      bad_fruits,
                      snake_head,
                      snake_body)

        # state.display()
        q_to_agent_state.put((state.up, state.down, state.left, state.right))

        if last_move is None:
            q_to_agent_reward.put(None)
        else:
            reward = rewarder.compute_reward(state, last_tile, last_move)
            q_to_agent_reward.put(reward)


def launch_interpreter_standalone():
    pass


if __name__ == "__main__":
    launch_interpreter_standalone()
