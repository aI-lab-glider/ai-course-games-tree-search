from base.state import State
from dataclasses import dataclass
from numpy.typing import NDArray


@dataclass
class TicTacToeState(State):
    board: NDArray

    def show(self):
        print(self.board)
