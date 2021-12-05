from games.tictactoe.state import TicTacToeState
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class TicTacToeAction:
    sign: str
    row: int
    col: int

    def apply(self, state: TicTacToeState) -> TicTacToeState:
        new_board = deepcopy(state.board)
        new_board[self.row, self.col] = self.sign
        return TicTacToeState(board=new_board)

    def __hash__(self):
        return hash((self.sign, self.row, self.col))
