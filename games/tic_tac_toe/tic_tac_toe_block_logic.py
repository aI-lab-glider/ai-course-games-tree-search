from typing import Tuple
from utils.pil_utils import GridDrawer
import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageFont
from utils.pil_utils import GridDrawer


EMPTY_SIGN = ' '
TIE_SIGN = '_'


class TicTacToeBlockLogic:

    def __init__(self, player_sign='X', opponent_sign='O'):
        self.player_sign = player_sign
        self.opponent_sign = opponent_sign

    @staticmethod
    def block_shape():
        return 3, 3

    def value_for_terminal(self, block: NDArray):
        winner = self.find_winner(block)
        if winner == self.player_sign:
            return 1
        if winner == self.opponent_sign:
            return -1
        return 0

    def find_winner(self, block: NDArray) -> str:
        row_count, col_count = self.block_shape()
        for row in range(row_count):
            if block[row, 0] in [self.player_sign, self.opponent_sign] and (block[row, :] == block[row, 0]).all():
                return block[row, 0]

        for col in range(col_count):
            if block[0, col] in [self.player_sign, self.opponent_sign] and (block[:, col] == block[0, col]).all():
                return block[0, col]

        if (block.diagonal() == block[1, 1]).all() or (np.fliplr(block).diagonal() == block[1, 1]).all():
            if block[1, 1] in [self.player_sign, self.opponent_sign]:
                return block[1, 1]
        return TIE_SIGN if EMPTY_SIGN not in block else EMPTY_SIGN

    def is_block_terminated(self,  board: NDArray) -> bool:
        return (EMPTY_SIGN not in board) or (self.find_winner(board) in [
            self.opponent_sign, self.player_sign, TIE_SIGN])

    def to_image(self, board: NDArray, size: Tuple[int, int] = (800, 800)) -> Image.Image:
        background_color = (255, 233, 208)
        image = Image.new("RGB", size, background_color)
        grid_drawer = GridDrawer(image, board)
        grid_drawer.draw_grid()
        font = ImageFont.truetype("assets/arial.ttf", size=int(grid_drawer.cell_height * 0.8))
        colors = {'X': (229, 68, 109), 'O': (46, 134, 171)}

        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if cell != ' ':
                    grid_drawer.draw_text(cell, (x, y), fill=colors[cell], font=font)
        return image


def tic_tac_toe_block_logic_factory(player_sign: str, opponent_sign: str):
    return TicTacToeBlockLogic(player_sign, opponent_sign)
