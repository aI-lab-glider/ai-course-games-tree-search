from abc import ABC, abstractmethod
from typing import Hashable
from abc import ABC


class State(ABC, Hashable):

    @abstractmethod
    def show(self) -> None:
        ...
