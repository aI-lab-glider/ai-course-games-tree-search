from games.checkers.state import CheckersState
from games.checkers.piece import CheckersPiece
from base.action import Action
from enum import Enum
from numpy.typing import NDArray
from copy import deepcopy
from typing import List, Union


class Move(Enum):
    WHITE_LEFT = (1, -1)
    WHITE_RIGHT = (1, 1)
    BLACK_LEFT = (-1, -1)
    BLACK_RIGHT = (-1, 1)


class CheckersAction(Action):
    def __init__(self, moves: Union[Move, List[Move]], piece: CheckersPiece, pieces: List[CheckersPiece], is_jump: bool):
        self.moves = moves
        self.piece = piece
        self.pieces = pieces
        self.is_jump = is_jump
        

    def apply(self, state: CheckersState) -> CheckersState:
        if self.is_jump:
            new_board = self.piece_jump(deepcopy(state.board))
        else:
            new_board = self.piece_move(deepcopy(state.board))
        return CheckersState(board=new_board)


    def piece_move(self, board: NDArray) -> NDArray: 
        board[self.piece.row][self.piece.col] = ' '
        self.piece.row += self.moves.value[0]
        self.piece.col += self.moves.value[1]
        board[self.piece.row][self.piece.col] = self.piece.id.value
        return board


    def piece_jump(self, board: NDArray) -> NDArray: 
        for move in self.moves:
            board[self.piece.row][self.piece.col] = ' '  
            for piece in self.pieces:
                if piece.row == self.piece.row + move.value[0] and piece.col == self.piece.col + move.value[1]:
                    board[piece.row][piece.col] = ' '
                    self.pieces.remove(piece)
            self.piece.row += move.value[0] * 2
            self.piece.col += move.value[1] * 2  
            board[self.piece.row][self.piece.col] = self.piece.id.value
        return board


    def __hash__(self):
        return hash(self.moves)
