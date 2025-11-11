from Game.utils import Reward as R
from Game.utils import Tile as T
from Game.utils import Action as A
from Interpreter import State


class Rewarder:
    def __init__(self):
        pass

    @staticmethod
    def compute_reward(state: State, last_tile: T, last_move: A):
        match last_tile:
            case T.GAME_OVER:
                return R.GAME_OVER
            case T.BAD_FRUIT:
                return R.BAD_FRUIT
            case T.GOOD_FRUIT:
                return R.GOOD_FRUIT

        match last_move:
            case A.UP:
                if 'G' in state.up:
                    return R.GOOD_DIR
            case A.DOWN:
                if 'G' in state.down:
                    return R.GOOD_DIR
            case A.LEFT:
                if 'G' in state.left:
                    return R.GOOD_DIR
            case A.RIGHT:
                if 'G' in state.right:
                    return R.GOOD_DIR

        return R.IDLE
