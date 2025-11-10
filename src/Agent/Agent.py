from Game.utils import Action, Tile
from Agent.QTable import QTable

import abc


class Agent:
    _state: list[int]
    _previous_state: list[int]
    _action: Action
    _nb_games: int
    training_mode: bool

    def __init__(self, training_mode):
        self.training_mode = training_mode
        self._nb_games = 0
        self._state = []

    def import_state(self,
                     state_up: list[chr],
                     state_down: list[chr],
                     state_left: list[chr],
                     state_right: list[chr]):

        self._previous_state = self._state
        self._state = []

        for i in range(len(state_up)):
            if i == len(state_up) and state_up[i] == '0':
                raise Exception('Up state in agent was incorrect')
            if state_up[i] != '0':
                self._state.append(
                    Tile.convert_from_char(state_up[i]).value
                )
                self._state.append(i)
                break

        for i in range(len(state_down)):
            if i == len(state_down) and state_down[i] == '0':
                raise Exception('Down state in agent was incorrect')
            if state_down[i] != '0':
                self._state.append(
                    Tile.convert_from_char(state_down[i]).value
                )
                self._state.append(i)
                break

        for i in range(len(state_left)):
            if i == len(state_left) and state_left[i] == '0':
                raise Exception('Left state in agent was incorrect')
            if state_left[i] != '0':
                self._state.append(
                    Tile.convert_from_char(state_left[i]).value
                )
                self._state.append(i)
                break

        for i in range(len(state_right)):
            if i == len(state_right) and state_right[i] == '0':
                raise Exception('Right state in agent was incorrect')
            if state_right[i] != '0':
                self._state.append(
                    Tile.convert_from_char(state_right[i]).value
                )
                self._state.append(i)
                break

        if len(self._state) != 8:
            raise Exception('One of the states was empty.' +
                            f'Found: {len(self._state)}')

    @abc.abstractmethod
    def train_step(self, reward):
        pass

    @abc.abstractmethod
    def next_step(self):
        pass


class Agent_QTable(Agent):
    _table: QTable

    def __init__(self, training_mode):
        super().__init__(training_mode)
        self._table = QTable(0.9, 0.1)

    def train_step(self, reward: Tile):
        if reward is Tile.GAME_OVER:
            self._nb_games += 1
            print(f'Nb games: {self._nb_games}')
        self._table.update_value(self._previous_state,
                                 self._state,
                                 self._action,
                                 reward)

    def next_step(self):
        # epsilon = 10000 - self._nb_games
        # if random.randint(0, 20000) < epsilon:
        #     rd = random.randint(0, 3)
        #     self._action = Action(rd)
        # else:
        #     self._action = self._table.get_best_action(self._state)

        self._action = self._table.get_best_action(self._state)
        print(f'Going {self._action}')
        return self._action
