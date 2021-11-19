from base.state import State
from typing import List, TypeVar, Generic
from abc import ABC, abstractmethod

S = TypeVar('S', bound=State)
A = TypeVar('A')


class Problem(ABC, Generic[S, A]):
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
    def value_for(self, state: S) -> float:
        """Returns values of a state"""
        raise NotImplementedError

    @abstractmethod
    def is_terminal_state(self, state: S) -> bool:
        """Returns is given state is a terminal state"""
        raise NotImplementedError

    @abstractmethod
    def switch_players(self):
        """Returns problem with switched players"""
        raise NotImplementedError

