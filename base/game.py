from base.state import State
from base.action import Action
from typing import List, TypeVar, Generic
from abc import ABC, abstractmethod

S = TypeVar('S', bound=State)
A = TypeVar('A', bound=Action)


class Game(ABC, Generic[S, A]):
    def __init__(self, initial_state: S):
        self.initial_state = initial_state

    @abstractmethod
    def actions_for(self, state: S, is_opponent: bool) -> List[A]:
        """Generates actions to take from the given state"""
        raise NotImplementedError

    @abstractmethod
    def take_action(self, state: S, action: A) -> S:
        """Returns new state resulting from taking given action"""
        raise NotImplementedError

    @abstractmethod
    def value_for_terminal(self, state: S) -> float:
        """Returns values of a terminal state"""
        raise NotImplementedError

    @abstractmethod
    def is_terminal_state(self, state: S) -> bool:
        """Returns if given state is a terminal state"""
        raise NotImplementedError

    @abstractmethod
    def switch_players(self):
        """Returns game with switched players"""
        raise NotImplementedError

