from base.problem import Problem
from problems.tictactoe.state import TicTacToeState
from problems.tictactoe.action import TicTacToeAction
from typing import List, Union
import numpy as np


class TicTacToeProblem(Problem[TicTacToeState, TicTacToeAction]):
    def __init__(self, player_sign='X', opponent_sign='O'):
        self.player_sign = player_sign
        self.opponent_sign = opponent_sign
        initial_state = self.initial_game_state()
        super().__init__(initial_state)

    def initial_game_state(self):
        return TicTacToeState(board=np.full((3, 3), ' '))

    def switch_players(self) -> 'TicTacToeProblem':
        return TicTacToeProblem(player_sign=self.opponent_sign, opponent_sign=self.player_sign)

    def _get_sign(self, is_opponent: bool):
        if is_opponent:
            return self.opponent_sign
        else:
            return self.player_sign

    def actions_for(self, state: TicTacToeState, is_opponent: bool) -> List[TicTacToeAction]:
        sign = self._get_sign(is_opponent)
        return [TicTacToeAction(sign, row, col) for row in range(3) for col in range(3)
                if state.board[row, col] == ' ']

    def take_action(self, state: TicTacToeState, action: TicTacToeAction) -> TicTacToeState:
        return action.apply(state)

    def _find_winner(self, state: TicTacToeState) -> Union[str, None]:
        for row in range(3):
            if (state.board[row, :] == state.board[row, 0]).all() and state.board[row, 0] != ' ':
                return state.board[row, 0]
        for col in range(3):
            if (state.board[:, col] == state.board[0, col]).all() and state.board[0, col] != ' ':
                return state.board[0, col]
        if (state.board.diagonal() == state.board[1, 1]).all() or (np.fliplr(state.board).diagonal() == state.board[1, 1]).all():
            if state.board[1, 1] != ' ':
                return state.board[1, 1]
        return None

    def value_for(self, state: TicTacToeState) -> float:
        winner = self._find_winner(state)
        if winner == self.player_sign:
            return 1
        if winner == self.opponent_sign:
            return -1
        return 0

    def is_terminal_state(self, state: TicTacToeState, state_value: float) -> bool:
        if state_value in [-1, 1] or ' ' not in state.board:
            return True
        return False



