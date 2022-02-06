from dataclasses import dataclass
from base.state import State
from numpy.typing import NDArray


@dataclass
class BaseTicTacToeState(State):
    board: NDArray
