from board import TicTacToeBoard
from minimax import get_best_tictactoe_move
from printing_utils import require_input_and_clear


def get_human_tictactoe_move(board: TicTacToeBoard):
    valid_moves = board.get_possible_moves()

    while True:
        user_row = require_input_and_clear("Enter row to play on: ")
        user_column = require_input_and_clear("Enter column to play on: ")

        # Check integers
        try:
            user_row, user_column = int(user_row), int(user_column)
        except ValueError:
            require_input_and_clear("Invalid entry: enter integers between 1 and 3. Press enter to continue.)")
            continue

        # Check valid moves
        if (user_row - 1, user_column - 1) not in valid_moves:
            require_input_and_clear("Invalid move: ensure the chosen square is empty. Press enter to continue.")
            continue

        return user_row - 1, user_column - 1


class TicTacToeGamePlayer:
    """
    Plays TicTacToe between two opponents. The strategy can be different between X and O.
    """

    def __init__(self, player_X=get_human_tictactoe_move, player_O=get_human_tictactoe_move, silent=False):
        """
        Initialize the player with two players.
        :param player_X: Callable which will receive a TicTacToeBoard as input and should return a tuple
                            (row, column) of the player's chosen move. The board class has a utility to determine
                            valid moves, so the onus is on this method to ensure it returns a valid move.
        :param player_O: Similar to player_X.
        :param silent: If True, will not print anything as the game proceeds; else, will print moves and winning info.
                        After printing something, it will wait for user input (eg, enter) to move on.
        """
        self.player_X = player_X
        self.player_O = player_O
        self.silent = silent
        self.board = TicTacToeBoard()

    def play(self):
        player, next_player = self.player_X, self.player_O
        while not self.board.is_game_over:
            self._maybe_print(self.board)
            move = player(self.board)
            self._maybe_print(f"Player {self.board.next_player.name} chose to play at {move[0] + 1, move[1] + 1}.")
            self.board.play_move(*move)
            player, next_player = next_player, player
        self._maybe_print(f"Player {self.board.winning_player.name} wins!")
        self.board.reset()

    def _maybe_print(self, s):
        if not self.silent:
            require_input_and_clear(s)


if __name__ == "__main__":
    player = TicTacToeGamePlayer(player_O=get_best_tictactoe_move)
    player.play()
