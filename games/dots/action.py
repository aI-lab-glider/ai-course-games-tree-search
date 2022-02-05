import copy

from base.action import Action
from games.dots.state import DotsState, Chain
from dataclasses import dataclass
from copy import deepcopy
from numpy.typing import NDArray
from typing import List, Tuple


@dataclass
class DotsAction(Action):
    color: str
    row: int
    col: int

    def __hash__(self):
        return hash((self.color, self.row, self.col))

    def apply(self, state: DotsState) -> DotsState:
        new_board = deepcopy(state.board)
        new_board[self.row, self.col].color = self.color
        new_chains = deepcopy(state.chains)
        for chain in self._find_new_chains(new_board):
            if chain not in new_chains:
                new_chains.append(chain)
                self._mark_surrounded(new_board, chain)

        return DotsState(board=new_board, chains=new_chains)

    def _neighbours(self, board: NDArray, vertex: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbours = []
        for x_offset in [-1, 0, 1]:
            for y_offset in [-1, 0, 1]:
                if not (x_offset == 0 and y_offset == 0):
                    x = vertex[0] + x_offset
                    y = vertex[1] + y_offset
                    if (0 <= x < board.shape[0]) and (0 <= y < board.shape[1]):
                        if board[x, y].color == self.color and not board[x, y].is_surrounded:
                            neighbours.append((x, y))
        return neighbours

    def _find_new_chains(self, board: NDArray) -> List[Chain]:
        chains = []
        open_tracks = [[(self.row, self.col)]]
        used_dots = {(self.row, self.col)}
        while open_tracks:
            open_tracks_copy = copy.deepcopy(open_tracks)
            open_tracks = []
            for track in open_tracks_copy:
                for neighbour in self._neighbours(board, track[-1]):
                    if neighbour not in used_dots:
                        new_track = copy.deepcopy(track)
                        new_track.append(neighbour)
                        open_tracks.append(new_track)
                        used_dots.add(neighbour)
                    elif len(track) >= 3 and neighbour == (self.row, self.col):
                        chains.append(Chain(color=self.color, dots=track + [(self.row, self.col)]))
                    elif neighbour != (self.row, self.col):
                        for other_track in open_tracks_copy:
                            if other_track[1] != track[1] and neighbour == other_track[-1]:
                                chains.append(Chain(color=self.color, dots=track + other_track[::-1]))
                        for other_track in open_tracks:
                            if other_track[1] != track[1] and neighbour == other_track[-1]:
                                chains.append(Chain(color=self.color, dots=track + other_track[::-1]))
        return chains

    def _mark_surrounded(self, board: NDArray, chain: Chain):
        min_x = min(chain.dots, key=lambda dot: dot[0])[0]
        max_x = max(chain.dots, key=lambda dot: dot[0])[0]
        min_y = min(chain.dots, key=lambda dot: dot[1])[1]
        max_y = max(chain.dots, key=lambda dot: dot[1])[1]
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if any(dot[0] < x and dot[1] == y for dot in chain.dots) and any(
                        dot[0] > x and dot[1] == y for dot in chain.dots) and any(
                        dot[1] < y and dot[0] == x for dot in chain.dots) and any(
                        dot[1] > y and dot[0] == x for dot in chain.dots):
                    board[x, y].is_surrounded = True
                    if board[x, y].color != chain.color:
                        board[x, y].is_surrounded_by_opponent = True