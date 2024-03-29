from typing import Dict
from base.action import Action
from base.bot import Bot, G
from base.state import State
import random


class MonteCarlo(Bot):
    def __init__(self, n_rollouts: int):
        self.n_rollouts = n_rollouts
        super().__init__()

    def _choose_action(self, from_state: State) -> None:
        action_values = self._evaluate_actions(from_state)
        self.best_action = max(action_values, key=action_values.get)

    def _evaluate_actions(self, from_state: State) -> Dict[Action, float]:
        action_values = {}
        for _ in range(self.n_rollouts):
            action = random.choice(self.game.actions_for(
                from_state, is_opponent=False))
            result_state = self._rollout(
                self.game.take_action(from_state, action))
            action_value = self.game.reward(result_state)
            if action in action_values:
                action_values[action] += action_value
            else:
                action_values[action] = action_value
            self.best_action = max(action_values, key=action_values.get)
        return action_values

    def _rollout(self, from_state: State) -> State:
        current_state = from_state
        is_opponent = True
        while not self.game.is_terminal_state(current_state):
            actions = self.game.actions_for(current_state, is_opponent)
            if not actions:
                break
            action = random.choice(actions)
            current_state = self.game.take_action(current_state, action)
            is_opponent = not is_opponent
        return current_state
