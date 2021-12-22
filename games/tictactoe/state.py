from base.state import State
from dataclasses import dataclass
from numpy.typing import NDArray


@dataclass
class TicTacToeState(State):
    board: NDArray

    def show(self):
        for row in self.board:
            for col in row:
                sign = col if col != ' ' else '_'
                print(sign, end='  ')
            print()
        print()
