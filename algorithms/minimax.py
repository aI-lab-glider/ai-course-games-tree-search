import operator

from base.bot import Bot
from base.state import State
from base.action import Action
import math
from typing import Tuple, Optional


class Minimax(Bot):
    def choose_action(self, state: State) -> Optional[Action]:
        return self._minimax(state, is_opponent=False)[0]

    def _minimax(self, state: State, is_opponent: bool) -> Tuple[Optional[Action], float]:
        state_value = self.game.value_for_terminal(state)
        if self.game.is_terminal_state(state):
            return None, state_value
        return self._make_move(state, is_opponent)

    def _make_move(self, from_state, is_opponent) -> Tuple[Optional[Action], float]:
        if is_opponent:
            best_state_value = math.inf
            selection_condition = operator.lt
        else:
            best_state_value = -math.inf
            selection_condition = operator.gt

        best_action = None
        for action in self.game.actions_for(from_state, is_opponent):
            new_state = self.game.take_action(from_state, action)
            state_value = self._minimax(new_state, not is_opponent)[1]
            if selection_condition(state_value, best_state_value):
                best_state_value, best_action = state_value, action
        return best_action, best_state_value
