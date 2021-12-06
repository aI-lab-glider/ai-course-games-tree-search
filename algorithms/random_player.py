from random import choice
from typing import Optional

from base.action import Action
from base.bot import Bot
from base.state import State


class RandomPlayer(Bot):

    def choose_action(self, state: State) -> Optional[Action]:
        return choice(self.game.actions_for(state, is_opponent=False))
