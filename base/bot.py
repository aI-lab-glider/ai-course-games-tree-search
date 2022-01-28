from base.game import Game
from base.heuristic import Heuristic
from base.state import State
from base.action import Action
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

G = TypeVar('G', bound=Game)
H = TypeVar('H', bound=Heuristic)
A = TypeVar('A', bound=Action)


class Bot(ABC, Generic[G, A]):
    def __init__(self, game: G):
        self.game = game
        self._best_action: Optional[A] = None

    @property
    def best_action(self) -> Optional[A]:
        return self._best_action

    @best_action.setter
    def best_action(self, a: A | None) -> None:
        assert not a or isinstance(a, Action), f"Invalid action type '{type(a)}'"
        self._best_action = a

    @abstractmethod
    def choose_action(self, state: State) -> None:
        """
        Finds the optimal action for the state and assigns it to the `best_action` property.
        """


class HeuristicBot(Bot[G, A], ABC, Generic[A, G, H]):
    def __init__(self, game: G, heuristic: H):
        super().__init__(game)
        self.heuristic = heuristic
