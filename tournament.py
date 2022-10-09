from itertools import combinations
from algorithms.monte_carlo import MonteCarlo
from algorithms.monte_carlo_tree_search import MCTS
from algorithms.nearsighted_player import NearSighted
from algorithms.random_player import RandomPlayer
from base.game import Game
from games.tic_tac_toe.tic_tac_toe.game import TicTacToeGame
from tournament.run_competition import CompetitionParams, CompetitionResults, run_competition
from rich.columns import Columns
from rich.console import Console


def print_summary(competitions_results: list[CompetitionResults]):
    console = Console()
    console.print(Columns(competitions_results))


if __name__ == '__main__':
    games: list[Game] = [TicTacToeGame()]
    bots = [
        MCTS(),
        (MonteCarlo(10), 'MonetCarlo(n_rollouts=10)'),
        (MonteCarlo(10), 'MonetCarlo(n_rollouts=50)'),
        RandomPlayer(),
        NearSighted()
    ]
    params = CompetitionParams(1, 1)
    for game in games:
        results = [run_competition(bot_a_type, bot_b_type, game, params)
                   for bot_a_type, bot_b_type in combinations(bots, 2)]
        print_summary(results)
