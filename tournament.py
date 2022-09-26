from dataclasses import dataclass
from itertools import combinations
import math
import algorithms
from inspect import getmembers
from base.bot import Bot
from base.game import Game
from games.checkers.game import CheckersGame
from match import Match
from collections import defaultdict

@dataclass
class CompetitionParams:
    n_matches: int
    move_timeout: int

@dataclass
class BotResults:
    Bot: Bot
    matches_played: int
    victories: int

@dataclass
class CompetitionResults:
    bot_a: BotResults
    bot_b: BotResults

def run_competition(bot_a: Bot, bot_b: Bot, game: Game, params: CompetitionParams) -> CompetitionResults:
    results = defaultdict[Bot, BotResults](BotResults)    
    for _ in range(params.n_matches):    
        match = Match(game, bot_a, bot_b, params.move_timeout)
        match.play()
        winner = match.winner()
        if winner:
            results[winner].victories += 1 
    for bot in [bot_a, bot_b]:
        results[bot].matches_played = params.n_matches
    return CompetitionResults(results[bot_a], results[bot_b])




def print_summary(results: dict[Bot, list[CompetitionResults]]):
    for bot, bot_results in results.items():
        results = ','.join([f'{r.bot_a.victories / r.bot_a.matches_played}' for r in bot_results])
        print(f'{bot.__name__} w/a')





games: list[Game] = [CheckersGame()]
bots = getmembers(algorithms)
for game in games:
    params = CompetitionParams(1, 1)
    results = [run_competition(bot_a, bot_b, game, params)
        for bot_a, bot_b in combinations(bots)]
    grouped_results = {bot: [r for r in results if r.bot_a == bot]
        for bot in bots
    }
    print_summary(grouped_results)


        
