from base.game import Game
from games.checkers import EMPTY_SYMBOL
from games.checkers.state import CheckersState
from games.checkers.piece import BlackPiece, CheckersPiece, PlayerColor, WhitePiece
from games.checkers.action import CheckersAction
import numpy as np
from typing import Sequence, Tuple
from itertools import product


class CheckersGame(Game[CheckersState, CheckersAction]):
    """
    The following rules are applied https://youtu.be/WD3NTNQElew with the exception, 
    that the starting color is White instead of black.
    """

    def __init__(
            self, board_shape: Tuple[int, int] = (8, 8),
            player_color: PlayerColor = PlayerColor.WHITE, opponent_color: PlayerColor = PlayerColor.BLACK):
        self.board_shape = board_shape
        self._player_color, self._opponent_color = player_color, opponent_color
        initial_state = self.initial_game_state()
        super().__init__(initial_state)

    def initial_game_state(self) -> CheckersState:
        board = np.full(self.board_shape, EMPTY_SYMBOL, dtype=object)
        for row, col in product(*[range(d) for d in self.board_shape]):
            if col % 2 == ((row + 1) % 2):
                if row < self.board_shape[0] / 2 - 1:
                    piece = WhitePiece(row, col)
                    board[row, col] = piece

                elif row > self.board_shape[0] / 2:
                    piece = BlackPiece(row, col)
                    board[row, col] = piece

        return CheckersState(board, self._player_color)

    def actions_for(self, state: CheckersState, is_opponent: bool) -> Sequence[CheckersAction]:
        actions = []
        target_color = self._opponent_color if is_opponent else self._player_color
        movable_pieces = [p for p in state.pieces if p.color == target_color]
        for piece in movable_pieces:
            for chain in self.find_beat_chains_for_piece(state.board, piece):
                actions.append(CheckersAction(piece, chain, state))
        jumps_exists = any(actions)
        if jumps_exists:
            return actions

        for piece in movable_pieces:
            for move in piece.potential_moves(state.board):
                actions.append(CheckersAction(piece, [move], state))
        return actions

    def find_beat_chains_for_piece(self, board: np.ndarray, piece: CheckersPiece) -> Sequence[Sequence[Tuple[int, int]]]:
        """
        Returns possible beat routes for piece.
        """
        jumps = []
        for jump in piece.jumps(board):
            new_board, moved_piece = piece.move_to(board, *jump)
            jumps.extend([jump, *chain] for chain in self.find_beat_chains_for_piece(new_board, moved_piece) or [[]])
        return jumps

    def switch_players(self) -> 'CheckersGame':
        return CheckersGame(self.board_shape, self._opponent_color, self._player_color)

    def take_action(self, state: CheckersState, action: CheckersAction) -> CheckersState:
        new_state = action.apply()
        return new_state

    def _value_for_terminal(self, state: CheckersState) -> float:
        colors_on_board = {p.color for p in np.unique(state.board[state.board != EMPTY_SYMBOL])}
        if len(colors_on_board) == 1:
            return 1 if self._player_color in colors_on_board else -1
        return 0

    def _is_opponent(self, color: PlayerColor) -> bool:
        return color == self._opponent_color

    def is_terminal_state(self, state: CheckersState) -> bool:
        return self._value_for_terminal(state) in [-1, 1] or not any(self.actions_for(
            state, self._is_opponent(state.current_player_color)))
