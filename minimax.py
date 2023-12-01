from functools import cache

from board import TicTacToeBoard
from constants import X, O, X_WINNING, O_WINNING


def TicTacToeCriterion(player, current_evaluation, old_best):
    """
    Return true if current_evaluation is a better outcome than old_best for player.
    """
    return current_evaluation > old_best if player == X else current_evaluation < old_best


def get_best_move(board: TicTacToeBoard):
    assert not board.is_game_over, "Attempted to get best move in a finished game."

    best_outcome = float("-inf") if board.next_player == X else float("inf")
    best_row, best_column = None, None

    for row, column in board.get_possible_moves():
        if best_row is None or best_column is None:
            best_row, best_column = row, column

        # Play the move, evaluate, undo the move
        board.play_move(row, column)
        evaluation = evaluate(board)
        board.undo_move()

        # Update best found
        if TicTacToeCriterion(board.next_player, evaluation, best_outcome):
            best_outcome = evaluation
            best_row, best_column = row, column
    return best_row, best_column


@cache
def evaluate(board: TicTacToeBoard):
    if board.is_game_over:
        if board.winning_player is None:
            return 0
        if board.winning_player == X:
            return X_WINNING
        if board.winning_player == O:
            return O_WINNING

    # X is maximizing player by virtue of the above, O is minimizing
    best_outcome = float("-inf") if board.next_player == X else float("inf")
    for row, column in board.get_possible_moves():
        # Play the move, evaluate, undo the move
        board.play_move(row, column)
        evaluation = evaluate(board)
        board.undo_move()

        # Update best found
        if TicTacToeCriterion(board.next_player, evaluation, best_outcome):
            best_outcome = evaluation
    return best_outcome


if __name__ == "__main__":
    board = TicTacToeBoard()
    while not board.is_game_over:
        best_move = get_best_move(board)
        board.play_move(*best_move)
    print(board)
