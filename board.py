import numpy as np
from itertools import product

from constants import EMPTY, X, O, TIC_TAC_TOE_DISPLAY


class TicTacToeBoard:
    def __init__(self):
        self.state = None
        self.next_player = None
        self.next_next_player = None
        self.is_game_over = None
        self.move_history = None
        self.winning_player = None
        self.reset()

    def reset(self):
        self.state = np.full((3, 3), EMPTY.value)
        self.next_player = X
        self.next_next_player = O
        self.is_game_over = False
        self.move_history = []
        self.winning_player = None

    def play_move(self, row, column):
        assert 0 <= row < 3 and 0 <= column < 3, "Attempted move outside board"
        assert not self.is_game_over, "Attempted move after game over without resetting"
        assert self.state[row, column] == EMPTY.value, "Attempted repeat move without resetting"
        self.move_history.append((row, column))
        self.state[row, column] = self.next_player.value
        self._switch_active_player()
        self._check_game_over()

    def undo_move(self):
        assert len(self.move_history), "Attempted to undo move without making any"
        last_row, last_column = self.move_history.pop()
        self.state[last_row, last_column] = EMPTY.value
        self._switch_active_player()
        self._check_game_over()  # Resets winning_player and is_game_over

    def get_possible_moves(self):
        if self.is_game_over:
            return []
        return [(row, column) for row, column in product(range(3), range(3)) if self.state[row, column] == EMPTY.value]

    def _check_game_over(self):
        # Check for player win
        for player in (X, O):
            # Check rows:
            if any(all(square == player.value for square in row) for row in self.state):
                self.is_game_over = True
                self.winning_player = player
                return
            # Check columns
            if any(all(square == player.value for square in column) for column in self.state.T):
                self.is_game_over = True
                self.winning_player = player
                return
            # Check diagonals
            if (all(self.state[i, i] == player.value for i in range(3)) or
                    all(self.state[i, 2 - i] == player.value for i in range(3))):
                self.is_game_over = True
                self.winning_player = player
                return

        # Check for cat's game
        if not self.is_game_over and not any(value == EMPTY.value for value in self.state.flatten()):
            self.is_game_over = True
            self.winning_player = None
            return

        self.is_game_over = False
        self.winning_player = None

    def _switch_active_player(self):
        self.next_player, self.next_next_player = self.next_next_player, self.next_player

    def __str__(self):
        s = "\n|‾‾‾|‾‾‾|‾‾‾|\n"
        for row in range(3):
            for column in range(3):
                s += "| "
                s += TIC_TAC_TOE_DISPLAY[self.state[row, column]]
                s += " "
            s += "|\n"
            s += "|‾‾‾|‾‾‾|‾‾‾|\n" if row < 2 else "‾‾‾‾‾‾‾‾‾‾‾‾‾"
        s += "\n"
        return s

    def __hash__(self):
        base_3_index = "".join(str(value) for value in self.state.flatten())
        return int(base_3_index, 3)

    def __eq__(self, other):
        if not isinstance(other, TicTacToeBoard):
            return False
        return self.state == other.state


if __name__ == "__main__":
    # Run some basic tests to ensure board functionality
    board = TicTacToeBoard()

    # Try to undo a move without making any
    try:
        board.undo_move()
    except AssertionError:
        pass
    else:
        assert False

    # Play X in the center
    board.play_move(1, 1)

    # Try to play O in the center
    try:
        board.play_move(1, 1)
    except AssertionError:
        pass
    else:
        assert False

    # Play O in the bottom center
    board.play_move(2, 1)

    # Try to play X outside the board
    try:
        board.play_move(3, 1)
    except AssertionError:
        pass
    else:
        assert False

    # Play X in the top left
    board.play_move(0, 0)

    # Play O in the top center
    board.play_move(0, 1)

    # Play X in the bottom right (X should win here)
    board.play_move(2, 2)
    assert board.winning_player == X
    print(board)

    # Try to play a move after the game is over
    try:
        board.play_move(0, 0)
    except AssertionError:
        pass
    else:
        assert False

    # Undo a few moves and print
    board.undo_move()
    assert board.winning_player is None
    board.undo_move()
    board.undo_move()
    print(board)

    # Play X in the bottom left
    board.play_move(2, 0)

    # Play O in the right center
    board.play_move(1, 2)

    # Play X in the left center
    board.play_move(1, 0)

    # Play O in the top right
    board.play_move(0, 2)

    # Play X in the top center
    board.play_move(0, 1)

    # Play O in the bottom right (O should win)
    board.play_move(2, 2)
    assert board.winning_player == O
    print(board)

    # Reset and print empty board
    board.reset()
    print(board)
