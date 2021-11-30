from base.game import Game
from base.state import State
from base.action import Action
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional

G = TypeVar('G', bound=Game)


class Bot(ABC, Generic[G]):
    def __init__(self, game: G):
        self.game = game

    @abstractmethod
    def choose_action(self, state: State) -> Optional[Action]:
        raise NotImplementedError
