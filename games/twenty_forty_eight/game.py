from typing import List, Tuple
from games.twenty_forty_eight.state import TwentyFortyEightState
from games.twenty_forty_eight.action import TwentyFortyEightPlayerAction, TwentyFortyEightOpponentAction, Direction
from base.game import Game
from PIL import Image, ImageFont
from utils.pil_utils import GridDrawer
import numpy as np
import random
from itertools import product


class TwentyFortyEightGame(Game):
    def __init__(self):
        self.board_dim = 4
        initial_state = self.initial_game_state()
        super().__init__(initial_state)

    def initial_game_state(self) -> TwentyFortyEightState:
        state = TwentyFortyEightState(board=np.zeros(
            (self.board_dim, self.board_dim), dtype=int))
        for _ in range(2):
            action = random.choice(self.actions_for(state, is_opponent=True))
            state = self.take_action(state, action)
        return state

    def actions_for(self, from_state: TwentyFortyEightState, is_opponent: bool) -> List[
            TwentyFortyEightPlayerAction | TwentyFortyEightOpponentAction]:
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
            Direction.DOWN: (1, 0, product(
                range(self.board_dim-1), range(self.board_dim)))
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
                    action: TwentyFortyEightPlayerAction | TwentyFortyEightOpponentAction) -> TwentyFortyEightState:
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

    def to_image(self, state: TwentyFortyEightState, size: Tuple[int, int] = (800, 800)) -> Image.Image:
        background_color = (255, 233, 208)
        image = Image.new("RGB", size, background_color)
        grid_drawer = GridDrawer(image, state)
        grid_drawer.draw_grid()

        def font(block):
            return ImageFont.truetype("assets/arial.ttf", size=int(grid_drawer.cell_height * (7-len(str(block)))/10))

        block_color = {
            2: (252, 191, 73), 4: (247, 127, 0), 8: (214, 40, 40), 16: (226, 109, 92), 32: (165, 1, 4),
            64: (216, 87, 42), 128: (179, 106, 94), 256: (163, 50, 11), 512: (107, 5, 4), 1024: (245, 105, 96),
            2048: (156, 246, 246)}

        for y, row in enumerate(state.board):
            for x, cell in enumerate(row):
                if cell != 0:
                    grid_drawer.draw_rectangle((x, y), block_color[cell])
                    grid_drawer.draw_text(str(cell), (x, y), fill=(
                        51, 44, 35), font=font(cell))

        return image
