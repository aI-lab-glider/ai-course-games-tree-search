from base.game import Game
from games.checkers.state import CheckersState
from games.checkers.piece import CheckersPiece, Figure
from games.checkers.action import CheckersAction, Move
import numpy as np
from typing import Tuple, List


class CheckersGame(Game[CheckersState, CheckersAction]):
    def __init__(self, board_shape: Tuple[int, int] = (8, 8)):
        self.board_shape = board_shape
        self.pieces = []
        initial_state = self.initial_game_state()
        self.no_actions = False
        super().__init__(initial_state)

    def initial_game_state(self) -> CheckersState:
        board = np.full(self.board_shape, ' ')
        for row in range(self.board_shape[0]):
            for col in range(self.board_shape[1]):
                if col % 2 == ((row + 1) % 2):
                    if row < self.board_shape[0] / 2 - 1:
                        piece = CheckersPiece(Figure.WHITE_PIECE, row, col)
                        board[row][col] = piece.id.value
                        self.pieces.append(piece)
                    elif row > self.board_shape[0] / 2:
                        piece = CheckersPiece(Figure.BLACK_PIECE, row, col)
                        board[row][col] = piece.id.value
                        self.pieces.append(piece)
        return CheckersState(board)

    def actions_for(self, state: CheckersState, is_opponent: bool) -> List[CheckersAction]:
        actions = []
        for piece in self.pieces:
            if piece.turn != is_opponent:
                for move in Move:
                    if piece.king == True:
                        is_valid, moves = self.is_valid_king_move(state, piece, move, [])
                        if is_valid:
                            actions.append(CheckersAction(moves, piece, self.pieces, False))
                    else:
                        is_valid, moves = self.is_valid_jump(state, piece, move, [])
                        if is_valid:
                            actions.append(CheckersAction(moves, piece, self.pieces, True))
                        elif self.is_valid_move(state, piece, move):
                            actions.append(CheckersAction(move, piece, self.pieces, False))
        if len(actions) == 0:
            self.no_actions = True
        return actions

    def is_valid_move(self, state: CheckersState, piece: CheckersPiece, move: Move) -> bool:
        piece_moves = {
            Figure.WHITE_PIECE: [Move.WHITE_LEFT, Move.WHITE_RIGHT],
            Figure.BLACK_PIECE: [Move.BLACK_LEFT, Move.BLACK_RIGHT]
        }
        if move in piece_moves[piece.id]:
            new_row = piece.row + move.value[0]
            new_col = piece.col + move.value[1]
            if self.on_board(new_row, new_col):
                if state.board[new_row, new_col] == ' ':
                    return True
        return False

    def is_valid_jump(self, state: CheckersState, piece: CheckersPiece, move: Move, moves: List = []) -> Tuple[bool, List[Move]]:
        new_row = piece.row + move.value[0] * 2
        new_col = piece.col + move.value[1] * 2
        if self.on_board(new_row, new_col):
            if state.board[piece.row + move.value[0],
                           piece.col + move.value[1]] not in [piece.id.value, piece.id.value.capitalize(),
                                                              ' ']:
                if state.board[new_row, new_col] == ' ':
                    moves.append(move)
                    for next_move in Move:
                        if (next_move.value[0], next_move.value[1]) != (-move.value[0], -move.value[1]):
                            self.is_valid_jump(state, CheckersPiece(piece.id, new_row, new_col), next_move, moves)
                    return True, moves
        return False, moves

    def is_valid_king_move(self, state: CheckersState, piece: CheckersPiece, move: Move, moves: List = []) -> Tuple[bool, List[Move]]:
        new_row = piece.row + move.value[0]
        new_col = piece.col + move.value[1]
        if self.on_board(new_row, new_col):
            if state.board[new_row, new_col] == ' ':
                moves.append(move)
                for next_move in Move:
                    if (next_move.value[0], next_move.value[1]) != (-move.value[0], -move.value[1]):
                        self.is_valid_king_move(state, CheckersPiece(piece.id, new_row, new_col), next_move, moves)
                return True, moves
            elif state.board[new_row, new_col] not in [piece.id.value, piece.id.value.capitalize(), ' ']:  # opposite piece
                pass  # jump and in this case king can make a second move if it can kill opposite piece
            else:     # team piece
                return False, moves
        return False, moves

    def on_board(self, row: int, col: int) -> bool:
        return 0 <= row < self.board_shape[0] and 0 <= col < self.board_shape[1]

    def switch_players(self) -> 'CheckersGame':
        for piece in self.pieces:
            piece.turn = np.logical_not(piece.turn)
        return CheckersGame(self.board_shape)

    def take_action(self, state: CheckersState, action: CheckersAction) -> CheckersState:
        new_state = action.apply(state)
        print(new_state.show())
        return new_state

    def reward(self, state: CheckersState) -> float:
        assert self.is_terminal_state(state)
        return self._value_for_terminal(state)

    def _value_for_terminal(self, state: CheckersState) -> float:
        #unique, counts = np.unique(state.board, return_counts=True)
        if (Figure.WHITE_PIECE.value or Figure.WHITE_PIECE.value.capitalize()) not in state.board:
            return 1
        if (Figure.BLACK_PIECE.value or Figure.BLACK_PIECE.value.capitalize()) not in state.board:
            return -1
        return 0

    def is_terminal_state(self, state: CheckersState) -> bool:
        return self.no_actions or self._value_for_terminal(state) in [-1, 1]
