from base.game import Game
from base.bot import Bot
from base.state import State
import stopit
import random


class Match:
    def __init__(self, game: Game, player_a: Bot, player_b: Bot, timeout=1):
        self.game = game
        self.current_state = self.game.initial_state
        self.player_a = player_a
        self.player_b = player_b
        self.timeout = timeout
        self.states = [self.current_state]

    def play(self):
        self.turn = 0
        players = [self.player_a, self.player_b]
        while not self._is_match_end():
            print(
                f"Player {int(self.turn)} turn. ({type(players[int(self.turn)]).__name__})")
            self.current_state = self._next_move(players[int(self.turn)])
            self.current_state.show()
            self.turn = not self.turn
            self.states.append(self.current_state)

    def _next_move(self, player: Bot) -> State:
        with stopit.ThreadingTimeout(self.timeout) as to_ctx_mgr:
            assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
            _ = player.choose_action(self.current_state)
        print("timed out?", to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT)
        action = player.best_action or random.choice(self.game.actions_for(self.current_state, is_opponent=self.turn))
        return self.game.take_action(self.current_state,  action)

    def _is_match_end(self) -> bool:
        return self.game.is_terminal_state(self.current_state)

    def to_gif(self):
        img_name = f"{self.game.__class__.__name__}_{self.player_a.__class__.__name__}_{self.player_b.__class__.__name__}.gif"
        imgs = [self.game.to_image(state) for state in self.states]
        imgs[0].save(img_name, save_all=True, append_images=imgs[1:],
                     format='GIF', optimize=False, duration=500, loop=1)
