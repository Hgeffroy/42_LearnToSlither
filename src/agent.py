from multiprocessing import Queue

from Agent.Agent import Agent_QTable


def launch_agent_QTable(q_from_interpreter_state: Queue,
                        q_from_interpreter_reward: Queue,
                        q_to_game: Queue):

    agent = Agent_QTable(True)

    while True:
        reward = q_from_interpreter_reward.get()
        (state_up,
         state_down,
         state_left,
         state_right) = q_from_interpreter_state.get()

        if reward is not None:
            agent.train_step(reward)

        agent.import_state(state_up, state_down, state_left, state_right)
        q_to_game.put(agent.next_step())


def launch_agent_standalone():
    pass


if __name__ == "__main__":
    launch_agent_standalone()
