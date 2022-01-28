from games.tictactoe.game import TicTacToeGame
from games.twenty_forty_eight.game import TwentyFortyEightGame
from algorithms.minimax import Minimax
from algorithms.minimax_alpha_beta import MinimaxAlphaBeta
from algorithms.monte_carlo import MonteCarlo
from algorithms.random_player import RandomPlayer
from algorithms.montec_carlo_tree_search import MCTS
from match import Match


if __name__ == "__main__":
    game = TicTacToeGame()
    player_a = RandomPlayer(game)
    player_b = MonteCarlo(game.switch_players(), 100)
    # game = TwentyFortyEightGame()
    # player_a = MCTS(game, n_rollouts=20)
    # player_b = RandomPlayer(game, is_opponent=True)
    match = Match(game, player_a, player_b)
    match.play()
    match.to_gif()
