import operator

from base.bot import HeuristicBot, A, G, H
from base.state import State
from base.action import Action
import math
from typing import Tuple


class MinimaxDepth(HeuristicBot[A, G, H]):
    def __init__(self, max_depth: int, heuristic: H):
        super().__init__(heuristic)
        self.max_depth = max_depth

    def _choose_action(self, state: State) -> None:
        self.best_action, _ = self._minimax(state, is_opponent=False, depth=0)

    def _minimax(self, state: State, is_opponent: bool, depth: int) -> Tuple[A | None, float]:
        if depth == self.max_depth or self.game.is_terminal_state(state):
            return None, self.heuristic(state)
        return self._make_move(state, is_opponent, depth)

    def _make_move(self, from_state: State, is_opponent: bool, depth: int) -> Tuple[A | None, float]:
        if is_opponent:
            best_state_value = math.inf
            selection_condition = operator.lt
        else:
            best_state_value = -math.inf
            selection_condition = operator.gt

        best_action = None
        for action in self.game.actions_for(from_state, is_opponent):
            new_state = self.game.take_action(from_state, action)
            state_value = self._minimax(
                new_state, not is_opponent, depth + 1)[1]
            if selection_condition(state_value, best_state_value):
                best_state_value, best_action = state_value, action
        return best_action, best_state_value
