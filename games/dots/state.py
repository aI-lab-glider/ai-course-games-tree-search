from base.state import State

from dataclasses import dataclass
from typing import Tuple, List, cast
from numpy.typing import NDArray


@dataclass
class Dot:
    color: str
    is_surrounded: bool
    is_surrounded_by_opponent: bool


@dataclass
class Chain:
    color: str
    dots: List[Tuple[int, int]]

    def __str__(self):
        return f'{self.color} {self.dots}'

    def __getitem__(self, item):
        return self.dots[item]

    def __eq__(self, other):
        return self.color == other.color and (self.dots == other.dots or self.dots == other.dots[::-1])


@dataclass
class DotsState(State):
    board: NDArray
    chains: List[Chain]

    def show(self):
        for row in self.board:
            for col in row:
                sign = col.color if col.color != ' ' else '_'
                print(sign, end='  ')
            print()
        print(self.chains)
        print()

    @property
    def shape(self) -> Tuple[int, int]:
        return cast(Tuple[int, int], self.board.shape)
