from base.state import State
from dataclasses import dataclass
from typing import Tuple, cast
from games.tic_tac_toe.base_tic_tac_toe_state import BaseTicTacToeState
from numpy.typing import NDArray


@dataclass
class TicTacToeState(BaseTicTacToeState):

    @property
    def shape(self) -> Tuple[int, int]:
        return cast(Tuple[int, int], self.board.shape)

    def show(self):
        for row in self.board:
            for col in row:
                sign = col if col != ' ' else '_'
                print(sign, end='  ')
            print()
        print()

    def __hash__(self):
        return hash(self.board.data.tobytes())

    def __eq__(self, other):
        return type(other) is type(self) and hash(self) == hash(other)
