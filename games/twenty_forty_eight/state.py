from base.state import State
from dataclasses import dataclass
from numpy.typing import NDArray


@dataclass
class TwentyFortyEightState(State):
    board: NDArray

    def show(self):
        print(self.board)