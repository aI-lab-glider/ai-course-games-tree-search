from problems.tictactoe.problem import TicTacToeProblem
from algorithms.minimax import Minimax
from game import Game


if __name__ == "__main__":
    problem = TicTacToeProblem()
    game = Game(problem, player_a=Minimax, player_b=Minimax)
    game.play()
