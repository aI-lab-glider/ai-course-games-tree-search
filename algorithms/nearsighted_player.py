from typing import Optional, List, Tuple

from base.action import Action
from base.bot import Bot
from base.state import State
from random import choice


class NearSighted(Bot):
    def choose_action(self, state: State) -> Optional[Action]:

        reasonable_actions, winning_action = self.get_actions(state)

        if winning_action is not None:
            return winning_action
        if len(reasonable_actions) > 0:
            return choice(reasonable_actions)

        # every action leads to the defeat
        return choice(self.game.actions_for(state, is_opponent=False))

    def get_actions(self, state: State) -> Tuple[List[Optional[Action]], Optional[Action]]:
        reasonable_actions = []
        winning_actions = None
        for player_action in self.game.actions_for(state, is_opponent=False):
            next_state = self.game.take_action(state, player_action)
            if not self.game.is_terminal_state(next_state):
                is_valid = True
                for opponent_action in self.game.actions_for(next_state, is_opponent=True):
                    second_state = self.game.take_action(next_state, opponent_action)
                    is_terminal = self.game.is_terminal_state(second_state)

                    # there's a wining opportunity for opponent
                    if is_terminal and self.game.value_for_terminal(second_state) < 0:
                        is_valid = False
                        break

                if is_valid:
                    reasonable_actions.append(player_action)

            else:
                if self.game.value_for_terminal(next_state) > 0:
                    winning_actions = player_action

        return reasonable_actions, winning_actions
