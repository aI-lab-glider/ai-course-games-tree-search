from games.tictactoe.game import TicTacToeGame
from games.twenty_forty_eight.game import TwentyFortyEightGame
from algorithms.minimax import Minimax
from algorithms.minimax_alpha_beta import MinimaxAlphaBeta
from algorithms.monte_carlo import MonteCarlo
from algorithms.random_player import RandomPlayer
from algorithms.monte_carlo_tree_search import MCTS
from games.ultimate_tic_tac_toe.game import UltimateTicTacToeGame
from match import Match
from games.checkers.game import CheckersGame


if __name__ == "__main__":
    # game = UltimateTicTacToeGame()
    # player_a = RandomPlayer(game)
    # player_b = MonteCarlo(game.switch_players(), 100)
    # game = TwentyFortyEightGame()
    # player_b = MCTS(game.switch_players(), n_rollouts=20)
    # player_b = RandomPlayer(game, is_opponent=True)
    # match = Match(game, player_a, player_b)
    # match.play()
    # match.to_gif()
    # game = TicTacToeGame()
    # player_a = Minimax(game)
    # player_b = Minimax(game.switch_players())
    # match = Match(game, player_a, player_b)
    # match.play()
    game = CheckersGame()
    player_a = MCTS(game, n_rollouts=30)
    player_b = MCTS(game.switch_players(), n_rollouts=30)
    match = Match(game, player_a, player_b)
    match.play()
    # game.initial_state.show()


