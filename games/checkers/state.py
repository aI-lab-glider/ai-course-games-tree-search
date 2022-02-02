from base.state import State
from numpy.typing import NDArray
  
  
class CheckersState(State):
    def __init__(self, board: NDArray):
        self.board = board
    
    def show(self):
        print(self.board)

