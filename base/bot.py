import inspect
from base.game import Game
from base.heuristic import Heuristic
from base.state import State
from base.action import Action
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

G = TypeVar('G', bound=Game)
H = TypeVar('H', bound=Heuristic)
A = TypeVar('A', bound=Action)
B = TypeVar('B', bound='Bot')


class Bot(ABC, Generic[G, A]):
    def __init__(self):
        self.game = None
        self._best_action: Optional[A] = None

    @property
    def best_action(self) -> Optional[A]:
        return self._best_action

    @best_action.setter
    def best_action(self, a: A | None) -> None:
        assert not a or isinstance(
            a, Action), f"Invalid action type '{type(a)}'"
        self._best_action = a

    def choose_action(self, state: State) -> None:
        assert self.game is not None, "Bot is not fitted to game. Call `fit` method first."
        self._choose_action(state)

    @abstractmethod
    def _choose_action(self, state: State) -> None:
        """
        Finds the optimal action for the state and assigns it to the `best_action` property.
        """

    def fit(self: B, game: G) -> B:
        """
        Configures Bot so it would be possible to use it in game.        
        """
        self.game = game
        return self


class HeuristicBot(Bot[G, A], ABC, Generic[A, G, H]):
    def __init__(self, heuristic: H):
        super().__init__()
        self.heuristic = heuristic
