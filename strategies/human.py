from printing_utils import require_input_and_clear

def get_human_tictactoe_move(board):
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
