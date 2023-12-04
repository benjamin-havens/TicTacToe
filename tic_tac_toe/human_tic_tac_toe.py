from printing_utils import require_input_and_clear
from two_player_game import TwoPlayerGameAgent
from .tic_tac_toe_GUI import TicTacToeGUI
from .tic_tac_toe_game import TicTacToeMove, TicTacToeBoard


class TicTacToeHumanConsoleAgent(TwoPlayerGameAgent):
    def __init__(self, name):
        self.name = name

    def get_move(self, board: TicTacToeBoard):
        valid_moves = board.get_possible_moves()

        while True:
            user_row = require_input_and_clear("Enter row to play on: ")
            user_column = require_input_and_clear("Enter column to play on: ")

            # Check integers
            try:
                user_row, user_column = int(user_row), int(user_column)
            except ValueError:
                require_input_and_clear("Invalid entry: enter integers between 1 and 3. Press enter to continue.")
                continue

            # Check valid moves
            user_move = TicTacToeMove(user_row - 1, user_column - 1)
            if user_move not in valid_moves:
                require_input_and_clear("Invalid move: ensure the chosen square is empty. Press enter to continue.")
                continue

            return user_move


class TicTacToeHumanGUIAgent(TwoPlayerGameAgent):
    def __init__(self, name, gui: TicTacToeGUI):
        self.name = name
        self.gui = gui

    def get_move(self, board: TicTacToeBoard):
        return self.gui.get_user_move()
