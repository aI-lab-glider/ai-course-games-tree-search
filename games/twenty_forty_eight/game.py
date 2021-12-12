from typing import List, Union
from games.twenty_forty_eight.state import TwentyFortyEightState
from games.twenty_forty_eight.action import TwentyFortyEightPlayerAction, TwentyFortyEightOpponentAction, Direction
from base.game import Game
import numpy as np
import random
from itertools import product


class TwentyFortyEightGame(Game):
    def __init__(self, board_dim=4):
        self.board_dim = board_dim
        initial_state = self.initial_game_state()
        super().__init__(initial_state)

    def initial_game_state(self) -> TwentyFortyEightState:
        state = TwentyFortyEightState(board=np.zeros((self.board_dim, self.board_dim), dtype=int))
        for _ in range(2):
            action = random.choice(self.actions_for(state, is_opponent=True))
            state = self.take_action(state, action)
        return state

    def actions_for(self, from_state: TwentyFortyEightState, is_opponent: bool) -> List[
            Union[TwentyFortyEightPlayerAction, TwentyFortyEightOpponentAction]]:
        if is_opponent:
            return [TwentyFortyEightOpponentAction(row, col, block_value=random.choices([2, 4], weights=[0.9, 0.1])[0])
                    for row in range(self.board_dim) for col in range(self.board_dim)
                    if from_state.board[row, col] == 0]
        else:
            return [TwentyFortyEightPlayerAction(direction) for direction in Direction if self._is_valid_move(direction, from_state)]

    def _is_able_to_merge_row(self, state: TwentyFortyEightState) -> bool:
        return any(state.board[row][col] == state.board[row][col + 1] and state.board[row][col] != 0
                   for col in range(self.board_dim-1) for row in range(self.board_dim))

    def _is_able_to_merge_col(self, state: TwentyFortyEightState) -> bool:
        return any(state.board[row][col] == state.board[row + 1][col] and state.board[row][col] != 0
                   for row in range(self.board_dim-1) for col in range(self.board_dim))

    def _is_able_to_move_in_direction(self, direction: Direction, state: TwentyFortyEightState) -> bool:
        row_offset, col_offset, search_space = {
            Direction.LEFT: (0, -1, product(range(self.board_dim), range(1, self.board_dim))),
            Direction.RIGHT: (0, 1, product(range(self.board_dim), range(self.board_dim-1))),
            Direction.UP: (-1, 0, product(range(1, self.board_dim), range(self.board_dim))),
            Direction.DOWN: (1, 0, product(range(self.board_dim-1), range(self.board_dim)))
        }[direction]
        return any(state.board[row, col] != 0 and state.board[row + row_offset, col + col_offset] == 0 for row, col in
                   search_space)

    def _is_valid_move(self, direction: Direction, state: TwentyFortyEightState) -> bool:
        is_able_to_merge = {
            Direction.LEFT: self._is_able_to_merge_row,
            Direction.RIGHT: self._is_able_to_merge_row,
            Direction.UP: self._is_able_to_merge_col,
            Direction.DOWN: self._is_able_to_merge_col
        }[direction]
        if is_able_to_merge(state):
            return True
        return self._is_able_to_move_in_direction(direction, state)

    def take_action(self, state: TwentyFortyEightState,
                    action: Union[TwentyFortyEightPlayerAction, TwentyFortyEightOpponentAction]) -> TwentyFortyEightState:
        return action.apply(state)

    def value_for_terminal(self, state: TwentyFortyEightState) -> int:
        if 2048 in state.board:
            return 1
        return -1

    def is_terminal_state(self, state: TwentyFortyEightState) -> bool:
        if 2048 in state.board:
            return True
        return not(0 in state.board or self._is_able_to_merge_row(state) or self._is_able_to_merge_col(state))

    def switch_players(self):
        pass
