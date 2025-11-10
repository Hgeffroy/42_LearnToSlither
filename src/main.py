import multiprocessing as mp
from multiprocessing import Queue

from game import launch_environment_for_agent
from interpreter import launch_interpreter_for_agent
from agent import launch_agent_QTable


def main():
    q_agent_to_env = Queue()
    q_env_to_interpreter = Queue()
    q_interpreter_to_agent_reward = Queue()
    q_interpreter_to_agent_state = Queue()

    process_env = mp.Process(target=launch_environment_for_agent,
                             args=(q_agent_to_env, q_env_to_interpreter))

    process_interpreter = mp.Process(target=launch_interpreter_for_agent,
                                     args=(q_env_to_interpreter,
                                           q_interpreter_to_agent_reward,
                                           q_interpreter_to_agent_state))

    process_agent = mp.Process(target=launch_agent_QTable,
                               args=(q_interpreter_to_agent_state,
                                     q_interpreter_to_agent_reward,
                                     q_agent_to_env))

    process_env.start()
    process_interpreter.start()
    process_agent.start()
    process_env.join()
    process_interpreter.join()
    process_agent.join()


if __name__ == "__main__":
    main()
