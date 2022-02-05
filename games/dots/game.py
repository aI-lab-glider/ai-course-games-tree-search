from base.game import Game
from games.dots.state import DotsState, Dot
from games.dots.action import DotsAction
from typing import List, Tuple
import numpy as np
from PIL import Image
from utils.pil_utils import GridDrawer


class DotsGame(Game[DotsState, DotsAction]):
    def __init__(self, player_color='r', opponent_color='b'):
        self.player_color = player_color
        self.opponent_color = opponent_color
        self.board_dim = 10
        initial_state = self.initial_game_state()
        super().__init__(initial_state)

    def initial_game_state(self) -> DotsState:
        board = [[Dot(color=' ', is_surrounded=False, is_surrounded_by_opponent=False)
                  for _ in range(self.board_dim)] for _ in range(self.board_dim)]
        return DotsState(
            board=np.array(board),
            chains=[]
        )

    def switch_players(self) -> 'DotsGame':
        return DotsGame(player_color=self.opponent_color, opponent_color=self.player_color)

    def _get_color(self, is_opponent: bool) -> str:
        if is_opponent:
            return self.opponent_color
        else:
            return self.player_color

    def actions_for(self, state: DotsState, is_opponent: bool) -> List[DotsAction]:
        color = self._get_color(is_opponent)
        return [DotsAction(color, row, col) for row in range(self.board_dim) for col in range(self.board_dim)
                if state.board[row, col].color == ' ' and not state.board[row, col].is_surrounded]

    def take_action(self, state: DotsState, action: DotsAction) -> DotsState:
        return action.apply(state)

    def _calculate_surrounded(self, state: DotsState, color: str) -> int:
        return sum(1 for col in range(self.board_dim) for row in range(self.board_dim)
                   if state.board[row, col].color == color
                   and state.board[row, col].is_surrounded_by_opponent)

    def _value_for_terminal(self, state: DotsState) -> int:
        player_result = self._calculate_surrounded(state, self.opponent_color)
        opponent_result = self._calculate_surrounded(state, self.player_color)
        if player_result > opponent_result:
            return 1
        if player_result < opponent_result:
            return -1
        return 0

    def is_terminal_state(self, state: DotsState) -> bool:
        return all(state.board[row, col].color != ' ' or state.board[row, col].is_surrounded
                   for row in range(self.board_dim) for col in range(self.board_dim))

    def to_image(self, state: DotsState, size: Tuple[int, int] = (800, 800)) -> Image.Image:
        background_color = (255, 233, 208)
        image = Image.new("RGB", size, background_color)
        grid_drawer = GridDrawer(image, state)
        grid_drawer.draw_grid()
        colors = {'r': (229, 68, 109), 'b': (46, 134, 171)}

        for y, row in enumerate(state.board):
            for x, cell in enumerate(row):
                if cell.color != ' ':
                    grid_drawer.draw_dot(x, y, fill=colors[cell.color])

        for chain in state.chains:
            for i in range(len(chain.dots) - 1):
                x_start, y_start = grid_drawer.get_cell_coords(0, chain[i][1], chain[i][0], have_border=False)[0:2]
                x_stop, y_stop = grid_drawer.get_cell_coords(0, chain[i+1][1], chain[i+1][0], have_border=False)[0:2]
                grid_drawer.draw.line((x_start, y_start, x_stop, y_stop), fill=colors[chain.color], width=5)

        return image

