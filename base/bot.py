from base.problem import Problem
from base.state import State
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Union

P = TypeVar('P', bound=Problem)


class Bot(ABC, Generic[P]):
    def __init__(self, problem: Union[P, None]):
        self.problem = problem

    @abstractmethod
    def solve(self, state: State) -> State:
        raise NotImplementedError
