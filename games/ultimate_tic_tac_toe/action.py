from games.ultimate_tic_tac_toe.state import UTTTState
from copy import deepcopy
from dataclasses import astuple, dataclass
from base.action import Action


@dataclass
class UTTTAction(Action):
    sign: str
    block: int
    row: int
    col: int

    def apply(self, state: UTTTState) -> UTTTState:
        new_board = deepcopy(state.board)
        new_board[self.block, self.row, self.col] = self.sign
        next_block = 3 * self.row + self.col
        return UTTTState(board=new_board, curr_block_idx=next_block)

    def __hash__(self):
        return hash(astuple(self))

    def __eq__(self, other):
        return astuple(self) == astuple(other)
