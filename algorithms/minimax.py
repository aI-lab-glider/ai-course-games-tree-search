from base.bot import Bot, P
from base.state import State
import math
from typing import Union


class Minimax(Bot):
    def __init__(self, problem: Union[P, None] = None):
        super().__init__(problem)

    def solve(self, state: State) -> Union[State, None]:
        if self.problem.is_terminal_state(state, self.problem.value_for(state)):
            return None
        best_action_value = -math.inf
        best_action = None
        for action in self.problem.actions_for(state, is_opponent=False):
            new_state = self.problem.take_action(state, action)
            action_value = self._minimax(new_state, is_opponent=True)
            if action_value > best_action_value:
                best_action = action
                best_action_value = action_value
        return self.problem.take_action(state, best_action)

    def _minimax(self, state: State, is_opponent: bool) -> float:
        state_value = self.problem.value_for(state)
        if self.problem.is_terminal_state(state, state_value):
            return state_value

        if is_opponent:
            best_state_value = math.inf
            for action in self.problem.actions_for(state, is_opponent):
                new_state = self.problem.take_action(state, action)
                best_state_value = min(best_state_value, self._minimax(new_state, not is_opponent))
            return best_state_value

        else:
            best_state_value = -math.inf
            for action in self.problem.actions_for(state, is_opponent):
                new_state = self.problem.take_action(state, action)
                best_state_value = max(best_state_value, self._minimax(new_state, not is_opponent))
            return best_state_value
