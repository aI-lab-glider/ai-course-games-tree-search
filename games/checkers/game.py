from base.game import Game
from games.checkers.state import CheckersState
from games.checkers.piece import CheckersPiece
from games.checkers.action import CheckersAction
import numpy as np
from typing import Tuple


class CheckersGame(Game[CheckersState, CheckersAction]):
    def __init__(self, board_shape: Tuple[int, int] = (8,8)):
        self.board_shape = board_shape
        initial_state = self.initial_game_state()
        super().__init__(initial_state)

    def initial_game_state(self) -> CheckersState:
        self.pieces = [] 
        board = np.full(self.board_shape, ' ')
        for row in range(self.board_shape[0]):
            for col in range(self.board_shape[1]):
                if col % 2 == ((row + 1) % 2):
                    if row < self.board_shape[0] / 2 - 1:
                        piece = CheckersPiece('b', row, col)
                        board[row][col] = piece.id
                        self.pieces.append(piece)
                    elif row > self.board_shape[0] / 2:
                        piece = CheckersPiece('w', row, col)
                        board[row][col] = piece.id
                        self.pieces.append(piece)
        state = CheckersState(board)
        return state

    def switch_players(self) -> 'CheckersGame':
        for piece in self.pieces:
            piece.turn = np.logical_not(piece.turn)
        return CheckersGame(self.board_shape)

    def actions_for(self, state, is_opponent: bool):
        """Generates actions to take from the given state"""
        raise NotImplementedError

    def take_action(self, state, action):
        """Returns new state resulting from taking given action"""
        raise NotImplementedError

    def value_for_terminal(self, state) -> float:
        """Returns values of a terminal state"""
        raise NotImplementedError

    def is_terminal_state(self, state) -> bool:
        """Returns if given state is a terminal state"""
        raise NotImplementedError
