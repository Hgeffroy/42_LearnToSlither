from multiprocessing import Queue

from Agent.Agent import Agent_QTable
from Game.utils import Reward as R


def launch_agent_QTable(q_from_interpreter_state: Queue,
                        q_from_interpreter_reward: Queue,
                        q_to_game: Queue):

    agent = Agent_QTable()

    while True:
        reward = q_from_interpreter_reward.get()
        (state_up,
         state_down,
         state_left,
         state_right) = q_from_interpreter_state.get()

        agent.import_state(state_up, state_down, state_left, state_right)

        if reward is not None:
            agent.train_step(reward)

        if reward is not R.GAME_OVER:
            q_to_game.put(agent.next_step())

        else:
            print("Reward Game over")


def launch_agent_standalone():
    pass


if __name__ == "__main__":
    launch_agent_standalone()
