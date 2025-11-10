import random

from Game.utils import Action


class QTable:
    def __init__(self, gamma: float, lr: float):
        self._nb_state = pow(3 * 10, 4)
        self._gamma = gamma
        self._lr = lr

        self._table = [0] * self._nb_state * 4
        for idx in range(len(self._table)):
            self._table[idx] = random.uniform(-1, 1)

    def _get_index(self, state: list[int], action: Action):
        idx = action.value * self._nb_state

        for i in range(len(state) // 2):
            div = pow(3 * 10, i)
            idx += state[i * 2] * self._nb_state / (div * 3)
            idx += state[i * 2 + 1] * self._nb_state / (div * 3 * 10)

        return int(idx)

    def get_max_val_for_state(self, state):
        values = []
        for action in Action:
            q_val = self._table[self._get_index(state, action)]
            values.append(self._table[self._get_index(state, action)])
            print(f'qval: {q_val} for action {action}')

        return max(values)

    def get_best_action(self, state):
        max = -10000
        action = Action.UP
        for act in Action:
            q_val = self._table[self._get_index(state, act)]
            if q_val > max:
                max = q_val
                action = act
        return action

    def update_value(self, previous_state, state, last_action, reward):
        print('Previous state')
        self.get_max_val_for_state(previous_state)
        print(f'New state after {last_action}')
        idx = self._get_index(previous_state, last_action)
        exp_qval = self._table[idx]
        obs_qval = reward + self.get_max_val_for_state(state) * self._gamma
        td_error = obs_qval - exp_qval
        self._table[idx] += self._lr * td_error

        print('New value for previous state')
        self.get_max_val_for_state(previous_state)
        print(f'New value for new state after {last_action}')
        self.get_max_val_for_state(state)
