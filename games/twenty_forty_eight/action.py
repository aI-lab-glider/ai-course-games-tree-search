from enum import Enum, auto
from dataclasses import dataclass
from base.action import Action
from copy import deepcopy
from games.twenty_forty_eight.state import TwentyFortyEightState
import numpy as np
from numpy.typing import NDArray


class Direction(Enum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()


@dataclass
class TwentyFortyEightPlayerAction(Action):
    direction: Direction

    def apply(self, state: TwentyFortyEightState) -> TwentyFortyEightState:
        moves = {
            Direction.LEFT: self._move_left,
            Direction.RIGHT: self._move_right,
            Direction.UP: self._move_up,
            Direction.DOWN: self._move_down
        }
        new_board = moves[self.direction](deepcopy(state.board))
        return TwentyFortyEightState(board=new_board)

    def _move_left(self, board: NDArray) -> NDArray:
        board = self._compress(board)
        board = self._merge(board)
        return self._compress(board)

    def _move_right(self, board: NDArray) -> NDArray:
        board = self._move_left(np.flip(board, axis=1))
        return np.flip(board, axis=1)

    def _move_up(self, board: NDArray) -> NDArray:
        new_board = self._move_left(board.transpose()).transpose()
        return new_board

    def _move_down(self, board: NDArray) -> NDArray:
        new_board = self._move_right(board.transpose()).transpose()
        return new_board

    def _compress(self, board: NDArray) -> NDArray:
        compressed_board = np.zeros(board.shape, dtype=int)
        for row in range(board.shape[0]):
            compressed_row = board[row][board[row] != 0]
            compressed_board[row, 0:compressed_row.size] = compressed_row
        return compressed_board

    def _merge(self, board: NDArray) -> NDArray:
        for row in range(board.shape[0]):
            for col in range(board.shape[0]-1):
                if board[row][col] == board[row][col + 1] and board[row][col] != 0:
                    board[row][col] *= 2
                    board[row][col + 1] = 0
        return board

    def __hash__(self):
        return hash(self.direction)

    def __eq__(self, other):
        if type(other) is type(self):
            return hash(self) == hash(other)
        return False


@dataclass
class TwentyFortyEightOpponentAction(Action):
    row: int
    col: int
    block_value: int

    def apply(self, state: TwentyFortyEightState) -> TwentyFortyEightState:
        new_board = deepcopy(state.board)
        new_board[self.row, self.col] = self.block_value
        return TwentyFortyEightState(board=new_board)

    def __hash__(self):
        return hash((self.row, self.col, self.block_value))
