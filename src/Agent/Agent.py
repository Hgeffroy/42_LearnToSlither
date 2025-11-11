from Game.utils import Action, Reward
from Agent.QTable import QTable

import abc
# import random


# State:
# [dang_up, dang_down, dang_left, dang_right,
#  apple_up, ...]
class Agent:
    _state: list[bool]
    _previous_state: list[int]
    _action: Action
    _nb_games: int

    def __init__(self):
        self._nb_games = 0
        self._state = []

    def import_state(self,
                     state_up: list[chr],
                     state_down: list[chr],
                     state_left: list[chr],
                     state_right: list[chr]):

        self._previous_state = self._state
        self._state = [False] * 8

        for i in range(len(state_up)):
            if i == len(state_up) and state_up[i] == '0':
                raise Exception('Up state in agent was incorrect')
            if i == '0':
                continue
            if i == 0 and (state_up[i] == 'S' or state_up[i] == 'W'):
                self._state[0] = True
                break
            if state_up[i] == 'G':
                self._state[4] = True
                break

        for i in range(len(state_down)):
            if i == len(state_down) and state_down[i] == '0':
                raise Exception('Down state in agent was incorrect')
            if i == '0':
                continue
            if i == 0 and (state_down[i] == 'S' or state_down[i] == 'W'):
                self._state[1] = True
                break
            if state_down[i] == 'G':
                self._state[5] = True
                break

        for i in range(len(state_left)):
            if i == len(state_left) and state_left[i] == '0':
                raise Exception('Left state in agent was incorrect')
            if i == '0':
                continue
            if i == 0 and (state_left[i] == 'S' or state_left[i] == 'W'):
                self._state[2] = True
                break
            if state_left[i] == 'G':
                self._state[6] = True
                break

        for i in range(len(state_right)):
            if i == len(state_right) and state_right[i] == '0':
                raise Exception('Right state in agent was incorrect')
            if i == '0':
                continue
            if i == 0 and (state_right[i] == 'S' or state_right[i] == 'W'):
                self._state[3] = True
                break
            if state_right[i] == 'G':
                self._state[7] = True
                break

    @abc.abstractmethod
    def train_step(self, reward):
        pass

    @abc.abstractmethod
    def next_step(self):
        pass


class Agent_QTable(Agent):
    _table: QTable

    def __init__(self):
        super().__init__()
        self._table = QTable(0.9, 0.1, True)

    def train_step(self, reward: Reward):
        if reward is Reward.GAME_OVER:
            self._nb_games += 1
            print(f'Nb games: {self._nb_games}')
        self._table.update_value(self._previous_state,
                                 self._state,
                                 self._action,
                                 reward)
        self._table.store()

    def next_step(self):
        # epsilon = 320 - self._nb_games
        # if random.randint(0, 800) < epsilon:
        #     rd = random.randint(0, 3)
        #     self._action = Action(rd)
        # else:
        #     self._action = self._table.get_best_action(self._state)

        self._action = self._table.get_best_action(self._state)
        # print(f'Going {self._action}')
        return self._action
