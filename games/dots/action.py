import itertools
from copy import deepcopy
from numpy.typing import NDArray
from typing import List, Tuple
from dataclasses import dataclass

from base.action import Action
from games.dots.state import DotsState, Chain


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
                if self._mark_surrounded(new_board, chain):
                    new_chains.append(chain)
        return DotsState(board=new_board, chains=new_chains)

    def _neighbours(self, board: NDArray, vertex: Tuple[int, int]) -> List[Tuple[int, int]]:
        neighbours = []
        for x in range(vertex[0] - 1, vertex[0] + 2):
            for y in range(vertex[1] - 1, vertex[1] + 2):
                if (x, y) != vertex and (0 <= x < board.shape[0]) and (0 <= y < board.shape[1]):
                    if board[x, y].color == self.color and not board[x, y].is_surrounded:
                        neighbours.append((x, y))
        return neighbours

    def _find_new_chains(self, board: NDArray) -> List[Chain]:
        chains = []
        new_open_tracks = [[(self.row, self.col)]]
        used_dots = {(self.row, self.col)}
        while new_open_tracks:
            open_tracks = new_open_tracks
            new_open_tracks = []
            for track in open_tracks:
                for neighbour in self._neighbours(board, track[-1]):
                    if neighbour not in used_dots:
                        new_track = deepcopy(track)
                        new_track.append(neighbour)
                        new_open_tracks.append(new_track)
                        used_dots.add(neighbour)
                    elif len(track) >= 3 and neighbour == (self.row, self.col):
                        chains.append(Chain(color=self.color, dots=track + [(self.row, self.col)]))
                    elif neighbour != (self.row, self.col):
                        for other_track in itertools.chain(open_tracks, new_open_tracks):
                            if other_track[1] != track[1] and neighbour == other_track[-1]:
                                chains.append(Chain(color=self.color, dots=track + other_track[::-1]))
        return chains

    @staticmethod
    def _mark_surrounded(board: NDArray, chain: Chain) -> bool:
        marked_surrounded = False
        min_x = min(chain.dots, key=lambda dot: dot[0])[0]
        max_x = max(chain.dots, key=lambda dot: dot[0])[0]
        min_y = min(chain.dots, key=lambda dot: dot[1])[1]
        max_y = max(chain.dots, key=lambda dot: dot[1])[1]
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if board[x, y].color != ' ':
                    if any(dot[0] < x and dot[1] == y for dot in chain.dots) and any(
                            dot[0] > x and dot[1] == y for dot in chain.dots) and any(
                            dot[1] < y and dot[0] == x for dot in chain.dots) and any(
                            dot[1] > y and dot[0] == x for dot in chain.dots):
                        board[x, y].is_surrounded = True
                        if board[x, y].color != chain.color:
                            board[x, y].is_surrounded_by_opponent = True
                            marked_surrounded = True
        return marked_surrounded
