from base.game import Game
from games.checkers.state import CheckersState
from games.checkers.piece import CheckersPiece, Figure
from games.checkers.action import CheckersAction, Move
import numpy as np
from typing import Tuple


class CheckersGame(Game[CheckersState, CheckersAction]):
    def __init__(self, board_shape: Tuple[int, int] = (8,8)):
        self.board_shape = board_shape
        self.pieces = [] 
        initial_state = self.initial_game_state()
        super().__init__(initial_state)


    def initial_game_state(self) -> CheckersState:
        board = np.full(self.board_shape, ' ')
        for row in range(self.board_shape[0]):
            for col in range(self.board_shape[1]):
                if col % 2 == ((row + 1) % 2):
                    if row < self.board_shape[0] / 2 - 1:
                        piece = CheckersPiece(Figure.WHITE_PIECE, row, col)
                        board[row][col] = piece.id.value
                        self.pieces.append(piece)
                    elif row > self.board_shape[0] / 2:
                        piece = CheckersPiece(Figure.BLACK_PIECE, row, col)
                        board[row][col] = piece.id.value
                        self.pieces.append(piece)
        state = CheckersState(board)
        return state


    def actions_for(self, state, is_opponent: bool) -> CheckersAction:
        moves = {
            Figure.WHITE_PIECE: [Move.WHITE_LEFT, Move.WHITE_RIGHT],
            Figure.BLACK_PIECE: [Move.BLACK_LEFT, Move.BLACK_RIGHT]
        }
        actions = [CheckersAction(move, piece)
                    for piece in self.pieces
                    for move in moves[piece.id]
                    if self.is_valid_move(state, piece, move)]
        return actions


    def is_valid_move(self, state: CheckersState, piece: CheckersPiece, move: Move) -> bool:
        new_row = piece.row + move.value[0]
        new_col = piece.col + move.value[1]
        if self.on_board(new_row, new_col):
            if state.board[new_row, new_col] == ' ':
                return True
        return False


    def is_valid_jump(self):
        pass


    def on_board(self, row: int, col: int) -> bool:
        return 0 <= row < self.board_shape[0] and 0 <= col < self.board_shape[1]


    def switch_players(self) -> 'CheckersGame':
        for piece in self.pieces:
            piece.turn = np.logical_not(piece.turn)
        return CheckersGame(self.board_shape)


    def take_action(self, state, action):
        """Returns new state resulting from taking given action"""
        raise NotImplementedError

    def _value_for_terminal(self, state) -> float:
        """Returns values of a terminal state"""
        raise NotImplementedError

    def is_terminal_state(self, state) -> bool:
        """Returns if given state is a terminal state"""
        raise NotImplementedError
