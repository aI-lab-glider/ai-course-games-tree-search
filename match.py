from base.action import Action
from base.game import Game
from base.bot import Bot
from base.state import State
import stopit
import random
from typing import Generic, TypeVar

TPlayer = TypeVar('TPlayer', bound=Bot)
TOpponent = TypeVar('TOpponent', bound=Bot)
TState = TypeVar('TState', bound=State)
TAction = TypeVar('TAction', bound=Action)


class Match(Generic[TPlayer, TOpponent]):
    def __init__(self, game: Game[TState, TAction], player_a: TPlayer, player_b: TOpponent, move_timeout=1):
        self.game = game
        self.current_state = self.game.initial_state
        self._players = [player_a, player_b]
        self._move_timeout = move_timeout
        self.states = [self.current_state]

    def play(self) -> TPlayer | TOpponent | None:
        self.turn = 0
        while not self._is_match_end():
            print(
                f"Player {int(self.turn)} turn. ({type(self._players[int(self.turn)]).__name__})")
            self.current_state = self._next_move(self._players[int(self.turn)])
            self.current_state.show()
            self.turn = not self.turn
            self.states.append(self.current_state)
        return self.winner()

    def _next_move(self, player: TPlayer | TOpponent) -> TState:
        with stopit.ThreadingTimeout(self._move_timeout) as to_ctx_mgr:
            assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
            _ = player.choose_action(self.current_state)
        print("timed out?", to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT)
        action = player.best_action or random.choice(
            self.game.actions_for(self.current_state, is_opponent=self.turn))
        return self.game.take_action(self.current_state,  action)

    def _is_match_end(self) -> bool:
        return self.game.is_terminal_state(self.current_state)

    def _is_tie(self) -> bool:
        return self.game.is_tie(self.current_state)

    def to_gif(self):
        object_names = [o.__class__.__name__ for o in [
            self.game, *self._players]]
        img_name = f"{'_'.join(object_names)}.gif"
        imgs = [self.game.to_image(state) for state in self.states]
        if all(imgs):
            imgs[0].save(img_name, save_all=True, append_images=imgs[1:],
                         format='GIF', optimize=False, duration=500, loop=1)

    def winner(self) -> TPlayer | TOpponent | None:
        if self._is_match_end() and not self._is_tie():
            last_turn = not self.turn
            return self._players[last_turn]
