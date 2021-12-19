from games.checkers.state import CheckersState
from games.checkers.piece import Figure, CheckersPiece
from base.action import Action
from enum import Enum
from numpy.typing import NDArray
from copy import deepcopy

class Move(Enum):
    WHITE_LEFT = (1, -1)
    WHITE_RIGHT = (1, 1)
    BLACK_LEFT = (-1, -1)
    BLACK_RIGHT = (-1, 1)


class CheckersAction(Action):
    def __init__(self, move: Move, piece: CheckersPiece):
        self.move = move
        self.piece = piece
        

    def apply(self, state: CheckersState) -> CheckersState:
        new_board = self.move(deepcopy(state.board))
        return CheckersState(new_board)


    def move(self, board: NDArray) -> NDArray: 
        board[self.piece.row][self.piece.col] = ' '
        board[self.piece.row + self.move[0]][self.piece.col + self.move[1]] = self.piece.id.value
        return board


    def __hash__(self):
        return hash()
