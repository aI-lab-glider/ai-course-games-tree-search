from base.game import Game
from base.bot import Bot
from base.state import State
import stopit
import random
from typing import Generic, TypeVar

TBot = TypeVar('TBot', bound=Bot)


class Match(Generic[TBot]):
    def __init__(self, game: Game, player_a: TBot, player_b: TBot, move_timeout=1):
        self.game = game
        self.current_state = self.game.initial_state
        self.player_a = player_a
        self.player_b = player_b
        self._move_timeout = move_timeout
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

    def _next_move(self, player: TBot) -> State:
        with stopit.ThreadingTimeout(self._move_timeout) as to_ctx_mgr:
            assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
            _ = player.choose_action(self.current_state)
        print("timed out?", to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT)
        action = player.best_action or random.choice(
            self.game.actions_for(self.current_state, is_opponent=self.turn))
        return self.game.take_action(self.current_state,  action)

    def _is_match_end(self) -> bool:
        return self.game.is_terminal_state(self.current_state)

    def to_gif(self):
        img_name = f"{self.game.__class__.__name__}_{self.player_a.__class__.__name__}_{self.player_b.__class__.__name__}.gif"
        imgs = [self.game.to_image(state) for state in self.states]
        if all(imgs):
            imgs[0].save(img_name, save_all=True, append_images=imgs[1:],
                         format='GIF', optimize=False, duration=500, loop=1)

    def winner(self) -> TBot | None:
        if self._is_match_end():
            return self.game.select_winner(self.player_a, self.player_b)
