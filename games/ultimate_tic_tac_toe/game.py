from base.game import Game
from games.ultimate_tic_tac_toe.state import UTTTState
from games.ultimate_tic_tac_toe.action import UTTTAction
from typing import List, Optional
import numpy as np
from itertools import product

EMPTY_SIGN = ' '
TIE_SIGN = '_'


class UltimateTicTacToeGame(Game[UTTTState, UTTTAction]):
    def __init__(self, player_sign='X', opponent_sign='O'):
        self.player_sign = player_sign
        self.opponent_sign = opponent_sign
        initial_state = self._initial_game_state()
        super().__init__(initial_state)

    def _initial_game_state(self) -> UTTTState:
        return UTTTState(board=np.full((9, 3, 3), EMPTY_SIGN), curr_block_idx=4)

    def actions_for(self, state: UTTTState, is_opponent: bool) -> List[UTTTAction]:
        sign = self._get_sign(is_opponent)

        row_count, col_count = self.block_shape(state.board)

        def positions(block_idxs):
            return((block_idx, row, col) for block_idx, row, col in product(block_idxs, range(row_count), range(col_count))
                   if state.board[block_idx, row, col] == EMPTY_SIGN and not self._is_block_terminated(state.board[block_idx]))

        valid_blocks_idxs = range(self.blocks_count(state.board)) if self._is_block_terminated(
            state.board[state.curr_block_idx]) else [state.curr_block_idx]

        return [UTTTAction(sign, block, row, col) for block, row, col in positions(valid_blocks_idxs)]

    def block_shape(self, board: np.ndarray):
        return board.shape[1:] if board.ndim == 3 else board.shape

    def blocks_count(self, board: np.ndarray):
        return board.shape[0] if board.ndim == 3 else 1

    def take_action(self, state: UTTTState, action: UTTTAction) -> UTTTState:
        return action.apply(state)

    def _value_for_terminal(self, state: UTTTState) -> float:
        winner = self._find_winner(state)
        if winner == self.player_sign:
            return 1
        if winner == self.opponent_sign:
            return -1
        return 0

    def is_terminal_state(self, state: UTTTState) -> bool:
        board = np.reshape([self._find_winner_sign(state.board[block])
                           for block in range(self.blocks_count(state.board))], self.block_shape(state.board))
        return EMPTY_SIGN not in board or self._find_winner_sign(board) in [self.opponent_sign, self.player_sign, TIE_SIGN]

    def switch_players(self) -> 'UltimateTicTacToeGame':
        return UltimateTicTacToeGame(player_sign=self.opponent_sign, opponent_sign=self.player_sign)

    def _get_sign(self, is_opponent: bool) -> str:
        return self.opponent_sign if is_opponent else self.player_sign

    def _find_winner(self, state: UTTTState) -> str:
        board = np.reshape([self._find_winner_sign(state.board[block])
                           for block in range(self.blocks_count(state.board))], self.block_shape(state.board))
        return self._find_winner_sign(board)

    def _is_block_terminated(self, block: np.array) -> bool:
        return EMPTY_SIGN not in block or self._find_winner_sign(block) in [self.player_sign, self.opponent_sign, TIE_SIGN]

    def _find_winner_sign(self, board) -> str:
        row_count, col_count = self.block_shape(board)
        for row in range(row_count):
            if board[row, 0] in [EMPTY_SIGN, TIE_SIGN] and (board[row, :] == board[row, 0]).all():
                return board[row, 0]

        for col in range(col_count):
            if board[0, col] in [EMPTY_SIGN, TIE_SIGN] and (board[:, col] == board[0, col]).all():
                return board[0, col]

        if (board.diagonal() == board[1, 1]).all() or (np.fliplr(board).diagonal() == board[1, 1]).all():
            if board[1, 1] in [EMPTY_SIGN, TIE_SIGN]:
                return board[1, 1]
        return TIE_SIGN if EMPTY_SIGN not in board else EMPTY_SIGN
