import multiprocessing as mp
from multiprocessing import Queue

from game import launch_environment_for_agent
from interpreter import launch_interpreter_for_agent


def test(q: Queue):
    q.put('UP')


def main():
    q_agent_to_env = Queue()
    q_env_to_interpreter = Queue()
    q_interpreter_to_agent_reward = Queue()
    q_interpreter_to_agent_action = Queue()

    process_env = mp.Process(target=launch_environment_for_agent,
                             args=(q_agent_to_env, q_env_to_interpreter))

    process_interpreter = mp.Process(target=launch_interpreter_for_agent,
                                     args=(q_env_to_interpreter,
                                           q_interpreter_to_agent_reward,
                                           q_interpreter_to_agent_action))

    process_env.start()
    process_interpreter.start()
    process_env.join()
    process_interpreter.join()


if __name__ == "__main__":
    main()
