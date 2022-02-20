from typing import Iterable, Literal, Sequence, Tuple
from base.state import State
from games.checkers import EMPTY_SYMBOL
from games.checkers.piece import CheckersPiece, PlayerColor
from numpy.typing import NDArray
import numpy as np


class CheckersState(State):
    def __init__(self, board: NDArray, current_player_color: PlayerColor):
        self.board = board
        self.current_player_color = current_player_color
        self.pieces: Sequence[CheckersPiece] = np.unique(board[board != EMPTY_SYMBOL])

    def __hash__(self):
        return hash(str(self.board))

    def show(self):
        row_range, col_range = tuple(map(range, self.board.shape))
        for r in row_range:
            line = ''
            for c in col_range:
                symbol = self.board[r, c].symbol if self.board[r, c] != EMPTY_SYMBOL else EMPTY_SYMBOL
                line += f'{symbol:^3}|'
            print(line)
            print('-'*len(line))
