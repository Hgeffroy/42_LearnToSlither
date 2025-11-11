import random
import csv
import os

from Game.utils import Action, Reward


class QTable:
    def __init__(self, gamma: float, lr: float, load: bool):
        self._nb_state = pow(2, 8)
        self._gamma = gamma
        self._lr = lr

        if not load:
            self._table = [0] * self._nb_state * 4
            for idx in range(len(self._table)):
                self._table[idx] = random.uniform(-1, 1)

        else:
            self.load()

    def _get_index(self, state: list[bool], action: Action):
        idx = action.value * self._nb_state

        for i in range(len(state)):
            div = pow(2, i + 1)
            idx += int(state[i]) * self._nb_state / div

        return int(idx)

    def get_max_val_for_state(self, state: list[bool]):
        values = []
        for action in Action:
            values.append(self._table[self._get_index(state, action)])
            # q_val = self._table[self._get_index(state, action)]
            # print(f'qval: {q_val} for action {action}')

        return max(values)

    def get_best_action(self, state: list[bool]):
        max = None
        for act in Action:
            q_val = self._table[self._get_index(state, act)]
            if max is None or q_val > max:
                max = q_val
                action = act
        return action

    def update_value(self,
                     previous_state: list[bool],
                     state: list[bool],
                     last_action: Action,
                     reward: Reward):

        # print('Previous state')
        # self.get_max_val_for_state(previous_state)
        # print(f'New state after {last_action}')
        idx = self._get_index(previous_state, last_action)
        exp_qval = self._table[idx]
        obs_qval = (reward.value +
                    self.get_max_val_for_state(state) * self._gamma)
        td_error = obs_qval - exp_qval
        self._table[idx] += self._lr * td_error

        # print('New value for previous state')
        # self.get_max_val_for_state(previous_state)
        # print(f'New value for new state after {last_action}')
        # self.get_max_val_for_state(state)

    def store(self, model_folder: str = './models'):
        if not os.path.exists(model_folder):
            os.makedirs(model_folder)

        path = os.path.join(model_folder, 'model.csv')

        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(self._table)

    def load(self, model_folder: str = './models'):
        path = os.path.join(model_folder, 'model.csv')

        with open(path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            self._table = list(map(float, next(reader)))
