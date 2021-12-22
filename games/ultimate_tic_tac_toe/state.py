from base.state import State
from dataclasses import dataclass
from numpy.typing import NDArray


@dataclass
class UTTTState(State):
    board: NDArray
    curr_block: int

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
