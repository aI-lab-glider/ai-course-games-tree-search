from base.problem import Problem
from base.bot import Bot
from algorithms.minimax import Minimax


class Game:
    def __init__(self, problem: Problem, player_a: Bot, player_b: Bot):
        self.problem = problem
        self.current_state = self.problem.initial_state
        self.player_a = player_a
        self.player_b = player_b
        self.player_a.problem = self.problem
        self.player_b.problem = self.problem.switch_players()

    def play(self):
        while self.current_state:
            self.current_state.show()
            self.current_state = self.player_a.solve(self.current_state)
            if self.current_state is not None:
                self.current_state.show()
                self.current_state = self.player_b.solve(self.current_state)
