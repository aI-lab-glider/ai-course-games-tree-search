from operator import eq
from games.tictactoe.state import TicTacToeState
from copy import deepcopy
from dataclasses import dataclass
from base.action import Action


@dataclass(frozen=True, eq=True)
class TicTacToeAction(Action):
    sign: str
    row: int
    col: int

    def apply(self, state: TicTacToeState) -> TicTacToeState:
        new_board = deepcopy(state.board)
        new_board[self.row, self.col] = self.sign
        return TicTacToeState(board=new_board)

    def __hash__(self):
        return hash((self.sign, self.row, self.col))

    def __eq__(self, other):
        if type(other) is type(self):
            return hash(self) == hash(other)
        return False
