from abc import ABC, abstractmethod
from base.state import State
from base.game import Game

from typing import TypeVar, Generic, Any, cast

S = TypeVar('S', bound=State)
G = TypeVar('G', bound=Game)


class Heuristic(ABC, Generic[S]):

    @abstractmethod
    def __init__(self, game: Game[S, Any]) -> None:
        """Creates a heuristic for the given game"""

    @abstractmethod
    def __call__(self, state: S) -> float:
        """Calculates value for a given state depending on the chances to win from that state"""
