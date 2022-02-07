import itertools
from copy import deepcopy
from numpy.typing import NDArray
from typing import List, Tuple
from dataclasses import dataclass, astuple

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from base.action import Action
from games.dots.state import DotsState, Chain


@dataclass
class DotsAction(Action):
    color: str
    row: int
    col: int

    def __hash__(self):
        return hash(astuple(self))

    def apply(self, state: DotsState) -> DotsState:
        new_board = deepcopy(state.board)
        new_board[self.row, self.col].color = self.color
        new_chains = deepcopy(state.chains)
        for chain in self._find_new_chains(new_board):
            if chain not in new_chains:
                if self._is_mark_surrounded(new_board, chain):
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

    @staticmethod
    def _is_chain(track):
        return len(track) >= 3 and track[0] == track[-1]

    def _find_new_chains(self, board: NDArray) -> List[Chain]:
        chains = []
        new_open_tracks = [[(self.row, self.col)]]
        used_dots = set(new_open_tracks[0])
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
                    elif self._is_chain([*track, neighbour]):
                        chains.append(Chain(color=self.color, dots=[*track, neighbour]))
                    else:
                        for other_track in itertools.chain(open_tracks, new_open_tracks):
                            if other_track[1] != track[1] and neighbour == other_track[-1]:
                                chains.append(Chain(color=self.color, dots=track + other_track[::-1]))
        return chains

    @staticmethod
    def _is_mark_surrounded(board: NDArray, chain: Chain) -> bool:
        marked_surrounded = False
        polygon = Polygon(chain.dots)
        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                point = Point(x, y)
                if polygon.contains(point):
                    board[x, y].is_surrounded = True
                    if board[x, y].color != chain.color and board[x, y].color != ' ':
                        board[x, y].is_surrounded_by_opponent = True
                        marked_surrounded = True
        return marked_surrounded
