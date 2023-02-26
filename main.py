from games.checkers.game import CheckersGame
from games.tic_tac_toe.tic_tac_toe.game import TicTacToeGame
from games.twenty_forty_eight.game import TwentyFortyEightGame
from algorithms.minimax import Minimax
from algorithms.minimax_alpha_beta import MinimaxAlphaBeta
from algorithms.monte_carlo import MonteCarlo
from algorithms.random_player import RandomPlayer
from algorithms.monte_carlo_tree_search import MCTS
from games.tic_tac_toe.ultimate_tic_tac_toe.game import UltimateTicTacToeGame
from match import Match

if __name__ == "__main__":
    game = CheckersGame()
    player_a = RandomPlayer().fit(game)
    # player_b = MonteCarlo(game.switch_players(), 100)
    # game = TwentyFortyEightGame()
    player_b = MCTS(n_rollouts=20).fit(game.switch_players())
    # player_b = RandomPlayer(game, is_opponent=True)
    match = Match(game, player_a, player_b)
    match.play()
    match.to_gif()
