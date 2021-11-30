from games.tictactoe.game import TicTacToeGame
from algorithms.minimax import Minimax
from match import Match


if __name__ == "__main__":
    game = TicTacToeGame()
    player_a = Minimax(game)
    player_b = Minimax(game.switch_players())
    match = Match(game, player_a, player_b)
    match.play()
