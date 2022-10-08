from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

from base.bot import Bot
from base.game import Game
from match import Match
from rich.panel import Panel

BotFactory = Callable[[Game], Bot]


@dataclass
class CompetitionParams:
    n_matches: int
    move_timeout: int


@dataclass
class BotResults:
    bot_name: Bot
    victories: int


@dataclass
class CompetitionResults:
    player: BotResults
    opponent: BotResults
    matches_played: int

    def __rich__(self):
        pv, ov = self.player.victories, self.opponent.victories
        border_style = "yellow"
        if pv > ov:
            border_style = "green"
        if ov > pv:
            border_style = "red"
        return Panel(
            f"{self.player.bot_name}: {self.player.victories}\n"
            f"{self.opponent.bot_name}: {self.opponent.victories}\n"
            f"Total matches: {self.matches_played}",
            title=f'{self.player.bot_name} vs {self.opponent.bot_name}',
            border_style=border_style
        )


def run_competition(bot_factory_a: BotFactory, bot_factory_b: BotFactory, game: Game, params: CompetitionParams) -> CompetitionResults:
    bot_names = [type(f(game)).__name__ for f in [
        bot_factory_a, bot_factory_b]]
    victories = defaultdict(int)
    for _ in range(params.n_matches):
        bot_a, bot_b = bot_factory_a(
            game), bot_factory_b(game.switch_players())
        match = Match(game, bot_a, bot_b, move_timeout=params.move_timeout)
        winner = match.play()
        if winner:
            w_name = type(winner).__name__
            victories[w_name] += 1
    return CompetitionResults(*[BotResults(
        name,
        victories[name]
    ) for name in bot_names
    ], matches_played=params.n_matches)
