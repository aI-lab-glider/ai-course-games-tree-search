from typing import List, Tuple

from base.action import Action
from base.bot import Bot, G
from base.state import State
from random import choice


class NearSighted(Bot):
    def __init__(self, game: G, is_opponent: bool = False):
        self.is_opponent = is_opponent
        super().__init__(game)

    def choose_action(self, state: State) -> None:

        reasonable_actions, winning_action = self.get_actions(state, 1)

        if winning_action is not None:
            self.best_action = winning_action
        elif len(reasonable_actions) > 0:
            self.best_action = choice(reasonable_actions)

        # every action leads to the defeat
        else:
            self.best_action = choice(self.game.actions_for(state, is_opponent=self.is_opponent))

    def is_action_reasonable(self, curr_state: State, look_forward: int, is_opponent: bool) -> bool:
        if look_forward == 0:
            return not (self.game.is_terminal_state(curr_state) and self.game.value_for_terminal(curr_state) < 0)
        return all(self.is_action_reasonable(self.game.take_action(curr_state, action), look_forward - 1, is_opponent=not is_opponent)
                   for action in self.game.actions_for(curr_state, is_opponent=not is_opponent))

    def get_actions(self, state: State, look_forward: int) -> Tuple[List[Action | None], Action | None]:

        reasonable_actions = [action for action in self.game.actions_for(state, is_opponent=self.is_opponent) if
                              self.is_action_reasonable(self.game.take_action(state, action), look_forward, is_opponent=self.is_opponent)]

        winning_action = next((action for action in reasonable_actions if
                               self.game.value_for_terminal(self.game.take_action(state, action)) > 0), None)

        return reasonable_actions, winning_action
