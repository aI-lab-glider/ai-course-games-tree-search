from base.game import Game
from base.bot import Bot
from base.state import State
import stopit
import random


class Match:
    def __init__(self, game: Game, player_a: Bot, player_b: Bot, timeout=2):
        self.game = game
        self.current_state = self.game.initial_state
        self.player_a = player_a
        self.player_b = player_b
        self.timeout = timeout


    def play(self):
        self.turn = 1
        players = {0: self.player_a, 1: self.player_b}
        while not self._is_match_end():
            print(f"Player {int(self.turn)} turn")
            self.current_state = self._next_move(players[int(self.turn)])
            self.current_state.show()
            self.turn = not self.turn


    def _next_move(self, player: Bot) -> State:
        with stopit.ThreadingTimeout(self.timeout) as to_ctx_mgr:
            assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
            _ = player.choose_action(self.current_state)
        print("timed out?", to_ctx_mgr.state == to_ctx_mgr.TIMED_OUT)
        action = player.best_action or random.choice(self.game.actions_for(self.current_state, is_opponent=self.turn)) 
        return self.game.take_action(self.current_state,  action)


    def _is_match_end(self) -> bool:
        return self.game.is_terminal_state(self.current_state)
