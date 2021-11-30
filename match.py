from base.game import Game
from base.bot import Bot
from base.state import State


class Match:
    def __init__(self, game: Game, player_a: Bot, player_b: Bot):
        self.game = game
        self.current_state = self.game.initial_state
        self.player_a = player_a
        self.player_b = player_b

    def play(self):
        while not self._is_match_end():
            self.current_state.show()
            self.current_state = self._next_move(self.player_a)
            self.current_state.show()
            if not self._is_match_end():
                self.current_state = self._next_move(self.player_b)

    def _next_move(self, player: Bot) -> State:
        return self.game.take_action(self.current_state, player.choose_action(self.current_state))

    def _is_match_end(self) -> bool:
        return self.game.is_terminal_state(self.current_state)
