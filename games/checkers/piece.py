from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Iterable, Protocol, Sequence, Tuple, Type, TypeVar
from games.checkers import EMPTY_SYMBOL
import numpy as np


class PlayerColor(Enum):
    WHITE = auto()
    BLACK = auto()


TPiece = TypeVar('TPiece', bound='CheckersPiece')


class CheckersPiece(ABC):

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    @property
    @abstractmethod
    def color(self) -> PlayerColor:
        ...

    @property
    @abstractmethod
    def symbol(self) -> str:
        ...

    def move_to(self: TPiece, board: np.ndarray, row, col) -> Tuple[np.ndarray, 'TPiece']:
        board = board.copy()
        board[self.row, self.col] = EMPTY_SYMBOL
        if self._is_jump(board, row, col):
            self._jump(board, row, col)
        else:
            self._move(board, row, col)
        return board, board[row, col]

    def _is_jump(self, board: np.ndarray, new_row, new_col) -> bool:
        return manhattan_distance((new_row, new_col), (self.row, self.col)) != 2

    def _jump(self, board: np.ndarray, new_row, new_col):
        r, c = self._get_jump_direction(new_row, new_col)
        beaten_cell = self.row + r, self.col + c
        board[beaten_cell] = EMPTY_SYMBOL
        self._move(board, new_row, new_col)

    def _get_jump_direction(self, new_row: int, new_col: int):
        delta_row, delta_col = new_row - self.row, new_col - self.col
        delta_row = np.sign(delta_row) * (delta_row // delta_row) if delta_row != 0 else 0
        delta_col = np.sign(delta_col) * (delta_col // delta_col) if delta_col != 0 else 0
        return delta_row, delta_col

    @classmethod
    def _move(cls, board: np.ndarray, new_row, new_col):
        board[new_row, new_col] = cls(row=new_row, col=new_col)

    def __hash__(self):
        return hash(str(self))

    def __str__(self) -> str:
        return "Piece: {}, {}, {}".format(self.symbol, self.row, self.col)

    def __eq__(self, other):
        return isinstance(
            other, CheckersPiece) and (
            self.color, self.row, self.col) == (
            other.color, other.row, other.col)

    def __lt__(self, other):
        return isinstance(
            other, CheckersPiece) and (self.row, other.col) < (other.row, other.col)

    def __gt__(self, other):
        return isinstance(
            other, CheckersPiece) and (self.row, other.col) < (other.row, other.col)

    def potential_moves(self, board: np.ndarray):
        for move_forward in self.moves_forward():
            if self._is_in_board(board, move_forward) and board[move_forward] == EMPTY_SYMBOL:
                yield move_forward

    def jumps(self, board: np.ndarray) -> Iterable[Tuple[int, int]]:
        for opponent_figure_position in [
            (self.row + 1, self.col + 1),
            (self.row + 1, self.col - 1),
            (self.row - 1, self.col + 1),
                (self.row - 1, self.col - 1)]:

            if not self._is_in_board(
                    board, opponent_figure_position) or not self._is_in_board(
                    board, self._position_after_jump(opponent_figure_position)):
                continue
            if self.is_opponent(board[opponent_figure_position]) and board[self._position_after_jump(
                    opponent_figure_position)] == EMPTY_SYMBOL:

                yield self._position_after_jump(opponent_figure_position)

    def _is_in_board(self, board: np.ndarray, position: Tuple[int, int]):
        return position[0] in range(board.shape[0]) and position[1] in range(board.shape[1])

    def _position_after_jump(self, over_position: Tuple[int, int]) -> Tuple[int, int]:
        r, c = self._get_jump_direction(*over_position)
        return (self.row + r * 2, self.col + c * 2)

    def is_opponent(self, piece: 'CheckersPiece') -> bool:
        return piece != EMPTY_SYMBOL and self.color != piece.color

    @abstractmethod
    def moves_forward(self) -> Iterable[Tuple[int, int]]:
        ...


class WhitePiece(CheckersPiece):

    @property
    def color(self) -> PlayerColor:
        return PlayerColor.WHITE

    @property
    def symbol(self):
        return 'w'

    def moves_forward(self):
        return [(self.row + 1, self.col + 1), (self.row + 1, self.col - 1)]


class BlackPiece(CheckersPiece):

    @property
    def color(self) -> PlayerColor:
        return PlayerColor.BLACK

    @property
    def symbol(self):
        return 'b'

    def moves_forward(self):
        next_row = self.row - 1
        return (next_row, self.col + 1), (next_row, self.col - 1)


class King(CheckersPiece):
    def moves_forward(self):
        return [(self.row + y_shift, self.col + x_shift) for x_shift, y_shift in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]


class WhiteKing(King):
    @property
    def color(self) -> PlayerColor:
        return PlayerColor.WHITE

    @property
    def symbol(self):
        return 'W'


class BlackKing(King):

    @property
    def color(self) -> PlayerColor:
        return PlayerColor.BLACK

    @property
    def symbol(self):
        return 'B'


def upgrade_piece(piece: CheckersPiece):
    match piece:
        case WhitePiece(): return WhiteKing(piece.row, piece.col)
        case BlackPiece(): return BlackKing(piece.row, piece.col)
        case _: return piece


def get_opposite_color(color: PlayerColor):
    return PlayerColor.WHITE if color == PlayerColor.BLACK else PlayerColor.BLACK


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
