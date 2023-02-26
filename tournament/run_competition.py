from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Iterable

from numpy import iterable

from base.bot import Bot
from base.game import Game
from match import Match
from rich.panel import Panel


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

    def winner_results(self):
        if self.player.victories > self.opponent.victories:
            return self.player
        if self.player.victories < self.opponent.victories:
            return self.opponent

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


def run_competition(
        bot_a: Bot | tuple[Bot, str],
        bot_b: Bot | tuple[Bot, str],
        game: Game, params: CompetitionParams) -> CompetitionResults:
    bots, bot_names = list(zip(*assign_names_to_bots([bot_a, bot_b])))
    victories = defaultdict(int)
    for _ in range(params.n_matches):
        bot_a, bot_b = bots[0].fit(
            game), bots[1].fit(game.switch_players())
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


def assign_names_to_bots(bots: Iterable[Bot | tuple[Bot, str]]) -> tuple[tuple[Bot, str]]:
    return [b if isinstance(b, tuple) else (b, type(b).__name__)
            for b in bots
            ]
