from base.game import Game
from base.bot import Bot
from base.state import State


class Match:
    def __init__(self, game: Game, player_a: Bot, player_b: Bot):
        self.game = game
        self.current_state = self.game.initial_state
        self.player_a = player_a
        self.player_b = player_b
        self.states = [self.current_state]

    def play(self):
        while not self._is_match_end():
            self.current_state.show()
            self.current_state = self._next_move(self.player_a)
            self.current_state.show()
            self.states.append(self.current_state)
            if not self._is_match_end():
                self.current_state = self._next_move(self.player_b)
                self.states.append(self.current_state)

    def _next_move(self, player: Bot) -> State:
        return self.game.take_action(self.current_state, player.choose_action(self.current_state))

    def _is_match_end(self) -> bool:
        return self.game.is_terminal_state(self.current_state)

    def to_gif(self):
        img_name = f"{self.game.__class__.__name__}_{self.player_a.__class__.__name__}_{self.player_b.__class__.__name__}.gif"
        imgs = [self.game.to_image(state) for state in self.states]
        imgs[0].save(img_name, save_all=True, append_images=imgs[1:], format='GIF', optimize=False, duration=500, loop=1)
