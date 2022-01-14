from base.game import Game
from base.heuristic import Heuristic
from base.state import State
from base.action import Action
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

G = TypeVar('G', bound=Game)
H = TypeVar('H', bound=Heuristic)


class Bot(ABC, Generic[G]):
    def __init__(self, game: G):
        self.game = game
        self._best_action = None 

    @property 
    def best_action(self) -> Action:
        return self._best_action

    @best_action.setter 
    def best_action(self, a: Optional[Action]) -> None:
        if not isinstance(a, Action or None):
            raise TypeError(f"Invalid action type '{type(a)}'")
        self._best_action = a 

    @abstractmethod
    def choose_action(self, state: State) -> None:
        raise NotImplementedError


class HeuristicBot(Bot[G], ABC, Generic[G, H]):
    def __init__(self, game: G, heuristic: H):
        super().__init__(game)
        self.heuristic = heuristic
