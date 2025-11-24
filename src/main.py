import multiprocessing as mp
from multiprocessing import Queue
import argparse

from game import launch_environment_for_agent
from interpreter import launch_interpreter_for_agent
from agent import launch_agent_QTable


def main(training_mode: bool,
         explore_mode: bool,
         num_games: int,
         model_path: str):

    q_agent_to_env = Queue()
    q_env_to_interpreter = Queue()
    q_interpreter_to_agent_reward = Queue()
    q_interpreter_to_agent_state = Queue()

    process_env = mp.Process(target=launch_environment_for_agent,
                             args=(q_agent_to_env,
                                   q_env_to_interpreter,
                                   training_mode,
                                   num_games))

    process_interpreter = mp.Process(target=launch_interpreter_for_agent,
                                     args=(q_env_to_interpreter,
                                           q_interpreter_to_agent_reward,
                                           q_interpreter_to_agent_state))

    process_agent = mp.Process(target=launch_agent_QTable,
                               args=(q_interpreter_to_agent_state,
                                     q_interpreter_to_agent_reward,
                                     q_agent_to_env,
                                     training_mode,
                                     explore_mode,
                                     model_path))

    process_env.start()
    process_interpreter.start()
    process_agent.start()
    process_env.join()
    process_interpreter.join()
    process_agent.join()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t", "--training",
        type=bool,
        default=False,
        help="Model training on/off."
    )
    parser.add_argument(
        "-e", "--explore",
        type=bool,
        default=False,
        help="Exploratory mode on/off."
    )
    parser.add_argument(
        "-n", "--num-games",
        type=int,
        default=10,
        help="The number of games you want to play."
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="./models/model.csv",
        help="The model you want to use."
    )

    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()

    main(args.training, args.explore, args.num_games, args.model)
