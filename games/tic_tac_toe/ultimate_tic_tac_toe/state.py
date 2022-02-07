from base.state import State
from dataclasses import astuple, dataclass
from games.tic_tac_toe.base_tic_tac_toe_state import BaseTicTacToeState
from numpy.typing import NDArray


@dataclass
class UTTTState(BaseTicTacToeState):
    curr_block_idx: int

    def show(self):
        for i in range(3):
            for p in range(3):
                s = ""
                for j in range(3):
                    for k in range(3):
                        # if 3 * i + j == self.curr_block:
                        s += str(self.board[3 * i + j, p, k])
                        if k != 2:
                            s += "|"
                        if k == 2:
                            s += "\t"
                print(s, end="\n")
            print()
        print("=====================")

    def __hash__(self):
        return hash(astuple(self))

    def __eq__(self, other):
        return (self.board == other.board).all() and self.curr_block_idx == other.curr_block_idx
