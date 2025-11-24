from multiprocessing import Queue

from Agent.Agent import Agent_QTable
from Game.utils import Reward as R


def launch_agent_QTable(q_from_interpreter_state: Queue,
                        q_from_interpreter_reward: Queue,
                        q_to_game: Queue,
                        training_mode: bool,
                        explore_mode: bool,
                        model_path: str):

    agent = Agent_QTable(model_path)

    while True:
        (state_up,
         state_down,
         state_left,
         state_right) = q_from_interpreter_state.get()

        if state_up is None:
            break

        reward = q_from_interpreter_reward.get()

        agent.import_state(state_up, state_down, state_left, state_right)

        if training_mode is True and reward is not None:
            agent.train_step(reward)

        if reward is not R.GAME_OVER:
            q_to_game.put(agent.next_step(explore_mode))

        else:
            agent.nb_games += 1


def launch_agent_standalone():
    pass


if __name__ == "__main__":
    launch_agent_standalone()
