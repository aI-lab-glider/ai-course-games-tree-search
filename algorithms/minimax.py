from base.bot import Bot, P
from base.state import State
from base.action import Action
import math
from typing import Tuple, Union


class Minimax(Bot):
    def __init__(self, problem: P):
        super().__init__(problem)

    def choose_action(self, state: State) -> Union[Action, None]:
        return self._minimax(state, is_opponent=False)[0]

    def _minimax(self, state: State, is_opponent: bool) -> Tuple[Union[Action, None], float]:
        state_value = self.problem.value_for(state)
        if self.problem.is_terminal_state(state):
            return None, state_value

        if is_opponent:
            best_state_value = math.inf
            best_action = None
            for action in self.problem.actions_for(state, is_opponent):
                new_state = self.problem.take_action(state, action)
                state_value = self._minimax(new_state, not is_opponent)[1]
                if state_value < best_state_value:
                    best_state_value, best_action = state_value, action
            return best_action, best_state_value

        else:
            best_state_value = -math.inf
            best_action = None
            for action in self.problem.actions_for(state, is_opponent):
                new_state = self.problem.take_action(state, action)
                state_value = self._minimax(new_state, not is_opponent)[1]
                if state_value > best_state_value:
                    best_state_value, best_action = state_value, action
            return best_action, best_state_value
