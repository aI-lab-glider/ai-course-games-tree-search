from random import choice
from typing import Optional
# from time impoer sleep

from base.action import Action
from base.bot import Bot, G
from base.state import State


class RandomPlayer(Bot):
    def __init__(self, game: G, is_opponent: bool = False):
        self.is_opponent = is_opponent
        super().__init__(game)

    def choose_action(self, state: State) -> Optional[Action]:
        self.best_action = choice(self.game.actions_for(state, self.is_opponent))
        return self.best_action