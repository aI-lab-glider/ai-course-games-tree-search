from base.game import Game
from base.state import State
from base.action import Action
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

G = TypeVar('G', bound=Game)


class Bot(ABC, Generic[G]):
    def __init__(self, game: G):
        self.game = game
        self._best_action = None 
    

    @property 
    def best_action(self) -> Action:
        return self._best_action
    

    @best_action.setter 
    def best_action(self, a: Action) -> None:
        if not isinstance(a, Action):
            raise TypeError(f"Invalid action type '{type(a)}'")
        self._best_action = a 


    @abstractmethod
    def choose_action(self, state: State) -> None:
        raise NotImplementedError
