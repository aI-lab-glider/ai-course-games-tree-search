import operator

from base.bot import Bot
from base.state import State
from base.action import Action
import math
from typing import Tuple, Optional


class MinimaxAlphaBeta(Bot):
    def choose_action(self, state: State) -> Optional[Action]:
        return self._minimax(state, -math.inf, math.inf, is_opponent=False)[0]

    def _minimax(self, state: State, alpha: float, beta: float, is_opponent: bool) -> Tuple[Optional[Action], float]:
        if self.game.is_terminal_state(state):
            return None, self.game.reward(state)
        return self._make_move(state, alpha, beta, is_opponent)

    def _make_move(self, from_state: State, alpha: float, beta: float, is_opponent: bool) -> Tuple[Optional[Action], float]:
        if is_opponent:
            best_state_value = math.inf
            selection_condition = operator.lt
            letter = beta
        else:
            best_state_value = -math.inf
            selection_condition = operator.gt
            letter = alpha

        best_action = None
        for action in self.game.actions_for(from_state, is_opponent):
            new_state = self.game.take_action(from_state, action)
            state_value = self._minimax(new_state, alpha, beta, not is_opponent)[1]
            if selection_condition(state_value, best_state_value):
                best_state_value, best_action = state_value, action
            if selection_condition(state_value, letter):
                letter = state_value
            if beta <= alpha:
                break

        return best_action, best_state_value
