from base.problem import Problem
from base.bot import Bot
from typing import Type


class Game:
    def __init__(self, problem: Problem, player_a: Type[Bot], player_b: Type[Bot]):
        self.problem = problem
        self.current_state = self.problem.initial_state
        self.player_a = player_a(self.problem)
        self.player_b = player_b(self.problem.switch_players())

    def play(self):
        while not self._is_game_end():
            self.current_state.show()
            self.current_state = self._next_move(self.player_a)
            self.current_state.show()
            if not self._is_game_end():
                self.current_state = self._next_move(self.player_b)

    def _next_move(self, player: Bot):
        return self.problem.take_action(self.current_state, player.choose_action(self.current_state))

    def _is_game_end(self):
        return self.problem.is_terminal_state(self.current_state)


