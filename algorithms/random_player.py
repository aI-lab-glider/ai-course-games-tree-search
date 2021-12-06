
from base.bot import Bot
from base.state import State
from base.action import Action
from typing import Optional
from random import choice


class RandomPlayer(Bot):

    def choose_action(self, state: State) -> Optional[Action]:
        return choice(self.game.actions_for(state, is_opponent=False))

