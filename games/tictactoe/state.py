from base.state import State
from dataclasses import dataclass
from typing import Tuple, cast
from numpy.typing import NDArray


@dataclass
class TicTacToeState(State):
    board: NDArray

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
        if type(other) is type(self):
            return hash(self) == hash(other)
        return False
