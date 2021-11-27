import operator

from base.bot import Bot, P
from base.state import State
from base.action import Action
import math
from typing import Tuple, Union


class Minimax(Bot):
    def choose_action(self, state: State) -> Union[Action, None]:
        return self._minimax(state, is_opponent=False)[0]

    def _minimax(self, state: State, is_opponent: bool) -> Tuple[Union[Action, None], float]:
        state_value = self.problem.value_for(state)
        if self.problem.is_terminal_state(state):
            return None, state_value
        return self._make_move(state, is_opponent)

    def _make_move(self, from_state, is_opponent):
        if is_opponent:
            best_state_value = math.inf
            selection_condition = operator.lt
        else:
            best_state_value = -math.inf
            selection_condition = operator.gt

        best_action = None
        for action in self.problem.actions_for(from_state, is_opponent):
            new_state = self.problem.take_action(from_state, action)
            state_value = self._minimax(new_state, not is_opponent)[1]
            if selection_condition(state_value, best_state_value):
                best_state_value, best_action = state_value, action
        return best_action, best_state_value
