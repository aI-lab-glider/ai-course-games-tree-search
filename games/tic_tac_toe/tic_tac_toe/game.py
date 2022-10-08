from typing import Callable, List

import numpy as np
from base.game import Game
from games.tic_tac_toe.tic_tac_toe.action import TicTacToeAction
from games.tic_tac_toe.tic_tac_toe.state import TicTacToeState
from games.tic_tac_toe.tic_tac_toe_block_logic import (
    EMPTY_SIGN, TicTacToeBlockLogic, tic_tac_toe_block_logic_factory)


class TicTacToeGame(Game[TicTacToeState, TicTacToeAction]):
    def __init__(
            self, player_sign='X', opponent_sign='O',
            block_logic_factory: Callable[[str, str],
                                          TicTacToeBlockLogic] = tic_tac_toe_block_logic_factory):
        self.player_sign = player_sign
        self.opponent_sign = opponent_sign
        self.block_logic = block_logic_factory(player_sign, opponent_sign)
        initial_state = self._initial_game_state()
        super().__init__(initial_state)

    def _initial_game_state(self) -> TicTacToeState:
        return TicTacToeState(board=np.full(self.block_logic.block_shape(), EMPTY_SIGN))

    def switch_players(self):
        return TicTacToeGame(player_sign=self.opponent_sign, opponent_sign=self.player_sign)

    def value_for_terminal(self, state: TicTacToeState):
        return self.block_logic.value_for_terminal(state.board)

    def actions_for(self, state: TicTacToeState, is_opponent: bool) -> List[TicTacToeAction]:
        sign = self._get_sign(is_opponent)
        return [TicTacToeAction(sign, row, col) for row in range(3) for col in range(3)
                if state.board[row, col] == EMPTY_SIGN]

    def _get_sign(self, is_opponent: bool) -> str:
        return self.opponent_sign if is_opponent else self.player_sign

    def take_action(self, state: TicTacToeState, action: TicTacToeAction) -> TicTacToeState:
        return action.apply(state)

    def is_terminal_state(self, state: TicTacToeState):
        return self.block_logic.is_block_terminated(state.board)

    def to_image(self, state: TicTacToeState):
        return self.block_logic.to_image(state.board)
