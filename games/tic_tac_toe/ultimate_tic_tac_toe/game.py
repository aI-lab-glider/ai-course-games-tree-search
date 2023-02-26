from itertools import product
from typing import Callable, List, overload

import numpy as np
from base.game import Game
from games.tic_tac_toe.tic_tac_toe_block_logic import (
    EMPTY_SIGN, TicTacToeBlockLogic, tic_tac_toe_block_logic_factory)
from games.tic_tac_toe.ultimate_tic_tac_toe.action import UTTTAction
from games.tic_tac_toe.ultimate_tic_tac_toe.state import UTTTState
from numpy.typing import NDArray
from PIL import Image


class UltimateTicTacToeGame(Game[UTTTState, UTTTAction]):

    def __init__(
        self, player_sign='X', opponent_sign='O',
        block_logic_factory: Callable[[str, str],
                                      TicTacToeBlockLogic] = tic_tac_toe_block_logic_factory):
        self.player_sign = player_sign
        self.opponent_sign = opponent_sign
        self.block_logic = block_logic_factory(player_sign, opponent_sign)
        initial_state = self._initial_game_state()
        super().__init__(initial_state)
        self.blocks_count = 9

    def _initial_game_state(self) -> UTTTState:
        return UTTTState(
            board=np.full((self.blocks_count,
                           *self.block_shape),
                          EMPTY_SIGN),
            curr_block_idx=4)

    @property
    def block_shape(self):
        return self.block_logic.block_shape()

    def actions_for(self, state: UTTTState, is_opponent: bool) -> List[UTTTAction]:
        sign = self._get_sign(is_opponent)

        row_count, col_count = self.block_shape

        def positions(block_idxs):
            return((block_idx, row, col) for block_idx, row, col in product(block_idxs, range(row_count), range(col_count))
                   if state.board[block_idx, row, col] == EMPTY_SIGN and not self.is_block_terminated(state.board[block_idx]))

        valid_blocks_idxs = range(self.blocks_count) if self.is_block_terminated(
            state.board[state.curr_block_idx]) else [state.curr_block_idx]

        return [UTTTAction(sign, block, row, col) for block, row, col in positions(valid_blocks_idxs)]

    def take_action(self, state: UTTTState, action: UTTTAction) -> UTTTState:
        return action.apply(state)

    def is_terminal_state(self, state: UTTTState) -> bool:
        compressed_board = np.reshape([self._find_winner_sign_in_block(state.board[block])
                                       for block in range(self.blocks_count)], self.block_shape)
        return self.is_block_terminated(compressed_board)

    def _find_winner_sign_in_block(self, block: NDArray):
        return self.block_logic.find_winner(block)

    def is_block_terminated(self, block: NDArray):
        return self.block_logic.is_block_terminated(block)

    def switch_players(self) -> 'UltimateTicTacToeGame':
        return UltimateTicTacToeGame(player_sign=self.opponent_sign, opponent_sign=self.player_sign)

    def value_for_terminal(self, state: UTTTState):
        compressed_board = np.reshape([self._find_winner_sign_in_block(state.board[block])
                                       for block in range(self.blocks_count)], self.block_shape)

        return self.block_logic.value_for_terminal(compressed_board)

    def _get_sign(self, is_opponent: bool) -> str:
        return self.opponent_sign if is_opponent else self.player_sign

    def to_image(self, state: UTTTState):
        img_size = (800, 800)
        img = Image.new("RGB", img_size, (0, 0, 0))
        w, h = block_img_size = tuple(
            map(lambda x: int(x * self.block_shape[0] / self.blocks_count), img_size))
        for block in range(self.blocks_count):
            block_img = self.block_logic.to_image(
                state.board[block], block_img_size)
            block_img_coords = (w * (block % 3), h * (block // 3))
            img.paste(block_img, block_img_coords)
        return img
