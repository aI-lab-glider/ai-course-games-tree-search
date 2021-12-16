from base.state import State
from dataclasses import dataclass
from typing import Tuple, cast
from numpy.typing import NDArray


@dataclass
class TwentyFortyEightState(State):
    board: NDArray

    @property
    def shape(self) -> Tuple[int, int]:
        return cast(Tuple[int, int], self.board.shape)

    def show(self):
        print(self.board)
