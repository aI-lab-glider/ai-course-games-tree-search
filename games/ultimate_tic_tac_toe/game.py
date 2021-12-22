from base.game import Game
from games.ultimate_tic_tac_toe.state import UTTTState
from games.ultimate_tic_tac_toe.action import UTTTAction
from typing import List, Optional
import numpy as np


class UltimateTicTacToeGame(Game[UTTTState, UTTTAction]):
    def __init__(self, player_sign='X', opponent_sign='O'):
        self.player_sign = player_sign
        self.opponent_sign = opponent_sign
        initial_state = self._initial_game_state()
        super().__init__(initial_state)

    def _initial_game_state(self) -> UTTTState:
        return UTTTState(board=np.full((9, 3, 3), ' '), curr_block=4)

    def actions_for(self, state: UTTTState, is_opponent: bool) -> List[UTTTAction]:
        sign = self._get_sign(is_opponent)
        if ' ' not in state.board[state.curr_block] or self._is_block_terminated(state, state.curr_block):
            return [UTTTAction(sign, block, row, col) for block in range(9) for row in range(3) for col in range(3)
                    if state.board[block, row, col] == ' ' and not self._is_block_terminated(state, block)]
        else:
            return [UTTTAction(sign, state.curr_block, row, col) for row in range(3) for col in range(3)
                    if state.board[state.curr_block, row, col] == ' ']

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
        board = np.reshape([self._check_3x3(state.board[block]) for block in range(9)], (3, 3))
        return ' ' not in board or self._value_for_terminal(state) in [-1, 1]

    def switch_players(self) -> 'UltimateTicTacToeGame':
        return UltimateTicTacToeGame(player_sign=self.opponent_sign, opponent_sign=self.player_sign)

    def _get_sign(self, is_opponent: bool) -> str:
        return self.opponent_sign if is_opponent else self.player_sign

    def _find_winner(self, state: UTTTState) -> str:
        board = np.reshape([self._check_3x3(state.board[block]) for block in range(9)], (3, 3))
        return self._check_3x3(board, False)

    def _is_block_terminated(self, state: UTTTState,  block: int) -> bool:
        return ' ' not in state.board[block] or self._check_3x3(state.board[block]) in ['X', 'O', '_']

    def _check_3x3(self, board, is_block: bool = True) -> str:
        if ' ' not in board and is_block:
            return '_'
        for row in range(3):
            if board[row, 0] not in [' ', '_'] and (board[row, :] == board[row, 0]).all():
                return board[row, 0]

        for col in range(3):
            if board[0, col] not in [' ', '_'] and (board[:, col] == board[0, col]).all():
                return board[0, col]

        if (board.diagonal() == board[1, 1]).all() or (np.fliplr(board).diagonal() == board[1, 1]).all():
            if board[1, 1] not in [' ', '_']:
                return board[1, 1]
        return ' '




