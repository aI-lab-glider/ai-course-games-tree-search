from games.checkers.state import CheckersState
from base.action import Action


class CheckersAction(Action):
    def __init__(self):
        pass

    def apply(self, state: CheckersState) -> CheckersState:
        pass

    def __hash__(self):
        return hash()
