from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def __hash__(self):
        pass
