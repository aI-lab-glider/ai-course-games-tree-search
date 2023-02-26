from games.checkers import EMPTY_SYMBOL
from games.checkers.state import CheckersState
from games.checkers.piece import CheckersPiece, PlayerColor, get_opposite_color, upgrade_piece
from base.action import Action
from enum import Enum
from numpy.typing import NDArray
from copy import deepcopy
from typing import List, Sequence, Tuple, Union
import numpy as np


class CheckersAction(Action):
    def __init__(self, piece: CheckersPiece, positions_chain: Sequence[Tuple[int, int]], state):
        self._piece = piece
        self.position_chain = positions_chain
        self.state = state

    def apply(self) -> CheckersState:
        return self.jump_through_chain(self.position_chain)

    def jump_through_chain(self, position_chain: Sequence[Tuple[int, int]]) -> CheckersState:
        result_board = self.state.board
        piece = self._piece
        for position in position_chain:
            result_board, piece = piece.move_to(result_board, *position)
            if self._is_on_the_board_edge(piece):
                piece = upgrade_piece(piece)
                result_board[position] = piece
        return CheckersState(result_board, get_opposite_color(self._piece.color))

    def _is_on_the_board_edge(self, piece: CheckersPiece):
        board_edge_row = 0 if piece.color == PlayerColor.BLACK else self.state.board.shape[
            0] - 1
        return piece.row == board_edge_row

    def __hash__(self):
        return hash((frozenset(self.position_chain), self._piece))

    def __eq__(self, other):
        return type(other) == type(self) and other.position_chain == self.position_chain\
            and other._piece == self._piece

    def __str__(self):
        return f'[{self._piece.color.name}] Move from ({self._piece.row}, {self._piece.col}) through {self.position_chain}'
