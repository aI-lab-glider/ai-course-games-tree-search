from games.checkers.state import CheckersState
from games.checkers.piece import CheckersPiece, Figure
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
    def __init__(
            self, moves: Union[Move, List[Move]],
            piece: CheckersPiece, pieces: List[CheckersPiece],
            is_jump: bool):
        self.moves = moves if isinstance(moves, list) else [moves]
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
        self.piece.row += self.moves[0].value[0]
        self.piece.col += self.moves[0].value[1]
        # if self.piece.row in [0, board.shape[0]-1]:
        #     self.make_king(board)
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
            # if self.piece.row in [0, board.shape[0]-1]:
            #     self.make_king(board)
            board[self.piece.row][self.piece.col] = self.piece.id.value
        return board

    def make_king(self, board: NDArray):
        if self.piece.id == Figure.WHITE_PIECE:
            if self.piece.row == board.shape[0]-1:
                self.piece.id = Figure.WHITE_KING
                self.piece.king = True
        else:
            if self.piece.row == 0:
                self.piece.id == Figure.BLACK_KING
                self.piece.king = True
        return None

    def king_move(self, board: NDArray):
        pass

    def __hash__(self):
        return hash(self.moves)

    def __eq__(self, other):
        return type(other) == type(self) and other.moves == self.moves\
            and other.pieces == self.pieces\
            and other.pieces == self.piece\
            and self.is_jump == other.is_jump
