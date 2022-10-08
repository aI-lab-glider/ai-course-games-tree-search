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
    bot_factories = [
        lambda game: MCTS(game),
        lambda game: MonteCarlo(game, 10),
        lambda game: RandomPlayer(game),
        lambda game: NearSighted(game)
    ]
    params = CompetitionParams(1, 1)
    for game in games:
        results = [run_competition(bot_a_type, bot_b_type, game, params)
                   for bot_a_type, bot_b_type in combinations(bot_factories, 2)]
        print_summary(results)
