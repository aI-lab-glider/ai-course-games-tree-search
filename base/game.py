from base.state import State
from base.action import Action
from typing import List, TypeVar, Generic, Optional, Tuple
from abc import ABC, abstractmethod
from PIL.Image import Image

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

    def reward(self, state: S) -> float:
        """Returns reward for a terminal state. Raises exception if state is not terminal"""
        assert self.is_terminal_state(state), "This method should be called only on the terminal states!"
        return self._value_for_terminal(state)

    @abstractmethod
    def _value_for_terminal(self, state: S) -> float:
        """Returns value of a terminal state"""
        raise NotImplementedError

    @abstractmethod
    def is_terminal_state(self, state: S) -> bool:
        """Returns if given state is a terminal state"""
        raise NotImplementedError

    @abstractmethod
    def switch_players(self):
        """Returns game with switched players"""
        raise NotImplementedError

    def to_image(self, state: S, size: Tuple[int, int] = (800, 800)) -> Optional[Image]:
        """Converts state to its image representation."""
