from base.problem import Problem
from base.state import State
from base.action import Action
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Union

P = TypeVar('P', bound=Problem)


class Bot(ABC, Generic[P]):
    def __init__(self, problem: P):
        self.problem = problem

    @abstractmethod
    def choose_action(self, state: State) -> Union[Action, None]:
        raise NotImplementedError
